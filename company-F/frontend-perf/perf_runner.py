"""react/performance/browser/perf_runner.py — Performance baseline runner（tier × adapter 兩軸架構）。

取代既有 performance_baseline_collector.py / _egret.py 兩支 collector。
新版以 tier (basic/upgrade/advanced) × adapter (generic-url/product-react/product-egret) 正交組合。

Usage
-----
    # CLI 模式
    python perf_runner.py --tier basic --adapter generic-url --url https://example.com
    python perf_runner.py --tier upgrade --adapter product-react --trials 2
    python perf_runner.py --tier upgrade --adapter product-egret --trials 1

    # Interactive 模式（launcher 呼叫）
    python perf_runner.py
    # 會 prompt: URL / tier / adapter / trials / headless / out

Headed vs Headless（重要）
-------------------------
**預設 headed**（不加 --headless）— 跟 WebPageTest / Speed Insights / RUM 對齊，量出來的數據貼近真實用戶體驗。
加 --headless 給 CI/CD 大量自動化用。但要注意：

實測 product-react × upgrade × 1 trial 對比（2026-05-08 <PRODUCT> UAT）：

| 指標 | Headless | Headed | 差距 | 解讀 |
|---|---|---|---|---|
| lobby LCP | 6344 | 7156 | +13% | headed GPU pipeline 慢一點 |
| lobby CLS | 0.234 | 0.267 | +14% | headed 真實 layout 觸發更多 shift |
| **lobby TBT** | **583** | **1777** | **+205%** | **headed 主執行緒 GPU render 競爭，long tasks 多** |
| baccarat_room LCP | 6764 | 11128 | +65% | 同上 |
| baccarat_room TBT | 915 | 2718 | +197% | 同上 |

→ **Headless 的 TBT 系統性低估真實值 2-3x**。跨期對比 baseline 必須統一模式（headless ↔ headless 或 headed ↔ headed），不能混。
→ 5/7 既有 baseline 用 headless（[perf_comparison §Footer](../../report/performance/browser/perf_comparison_react_vs_egret_20260507_180000.md)）— 跟 5/8 之後 headed 跑的數據比較 TBT 會看似「惡化」，但實為 headed 才是真實值。

Output
------
    <repo>/react/report/performance/browser/perf_<adapter>_<YYYYmmdd_HHMMSS>/
        summary.json
        trial_1/{lobby,baccarat_room,sicbo_room}.json + *.png
        trial_2/...
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import time
from pathlib import Path
from typing import Any

from playwright.sync_api import BrowserContext, Page, sync_playwright

# Windows console cp950 — 強制 utf-8
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

from performance_baseline_shared import (
    INIT_OBSERVER_JS,
    SNAPSHOT_JS,
    _delta,
    _summarize_console,
    _summarize_network,
    validate_snapshot_schema,
    validate_summary_schema,
)
from perf_adapters import get_adapter, AdapterResult
from perf_tiers import get_tier

STABLE_WAIT_MS = 8000
SCHEMA_VERSION = "v2"  # 升級到 v2（含 byMime/byHost/cacheStats/wsStats 等新欄位）


def _new_context_with_observer(pw, headless: bool, viewport: dict[str, int]):
    """建立 fresh browser/context/page，注入 PerformanceObserver，掛 listener。"""
    console_msgs: list[dict[str, Any]] = []
    bad_responses: list[dict[str, Any]] = []
    request_failures: list[dict[str, Any]] = []

    browser = pw.chromium.launch(headless=headless)
    ctx: BrowserContext = browser.new_context(
        viewport=viewport,
        ignore_https_errors=True,
    )
    ctx.add_init_script(INIT_OBSERVER_JS)
    page: Page = ctx.new_page()

    page.on("console", lambda msg: console_msgs.append({"type": msg.type, "text": msg.text[:500]}))
    page.on("response", lambda r: bad_responses.append({"url": r.url, "status": r.status})
            if r.status >= 400 else None)
    page.on("requestfailed", lambda req: request_failures.append({
        "url": req.url, "failure": req.failure or "unknown",
        "method": req.method, "resourceType": req.resource_type,
    }))
    return browser, ctx, page, console_msgs, bad_responses, request_failures


def _attach_listeners_to_page(page: Page, console_msgs, bad_responses, request_failures):
    """新分頁也要裝 listener（Egret entry form 換新分頁時用）。"""
    page.on("console", lambda msg: console_msgs.append({"type": msg.type, "text": msg.text[:500]}))
    page.on("response", lambda r: bad_responses.append({"url": r.url, "status": r.status})
            if r.status >= 400 else None)
    page.on("requestfailed", lambda req: request_failures.append({
        "url": req.url, "failure": req.failure or "unknown",
        "method": req.method, "resourceType": req.resource_type,
    }))


def collect_scenario(
    pw,
    adapter,
    tier,
    scenario: dict[str, Any],
    trial_dir: Path,
    headless: bool,
    viewport: dict[str, int],
    url: str | None,
    nav_kwargs: dict[str, Any],
) -> dict[str, Any]:
    """跑單一 scenario（一個 fresh ctx）。"""
    name = scenario["name"]
    browser, ctx, page, console_msgs, bad_responses, request_failures = (
        _new_context_with_observer(pw, headless, viewport)
    )

    # adapter 註冊額外 listener（升級版 B2/B3 用），page-level
    # 對 Egret swap page 場景，nav 後對 new_page 再 attach 同 buffer（見下方 nav_result.new_page 處理）
    listener_buffer = adapter.attach_listeners(ctx, page)

    error_msg = None
    snap_a: dict[str, Any] | None = None
    snap_b: dict[str, Any] | None = None
    timing: dict[str, int] = {}
    extra_meta: dict[str, Any] = {}

    try:
        # Step 1: navigate to lobby
        nav_result: AdapterResult = adapter.navigate_to_lobby(ctx, page, url=url, **nav_kwargs)
        timing.update(nav_result.timing)
        if nav_result.error:
            error_msg = nav_result.error
        # adapter 可能換 page（Egret entry → new tab）
        if nav_result.new_page is not None:
            page = nav_result.new_page
            _attach_listeners_to_page(page, console_msgs, bad_responses, request_failures)
            # R6: 對新 page 重新 attach B2/B3 listener，共用同個 buffer
            adapter.attach_listeners(ctx, page, buffer=listener_buffer)
        if error_msg:
            raise RuntimeError(error_msg)

        # Step 2: STABLE_WAIT 後拍 snap_a
        page.wait_for_timeout(STABLE_WAIT_MS)
        snap_a = page.evaluate(SNAPSHOT_JS)
        validate_snapshot_schema(snap_a)
        try:
            snap_a_path = trial_dir / (
                f"{name}.png" if scenario["type"] == "lobby_only"
                else f"{name}_a_lobby.png"
            )
            page.screenshot(path=str(snap_a_path), full_page=False)
        except Exception:
            pass

        # Step 3: lobby_then_room 才進房
        if scenario.get("type") == "lobby_then_room":
            enter_result: AdapterResult = adapter.enter_scenario(ctx, page, scenario)
            timing.update(enter_result.timing)
            extra_meta.update(enter_result.extra)
            if enter_result.error:
                error_msg = enter_result.error
                raise RuntimeError(error_msg)

            page.wait_for_timeout(STABLE_WAIT_MS)
            snap_b = page.evaluate(SNAPSHOT_JS)
            validate_snapshot_schema(snap_b)
            try:
                page.screenshot(path=str(trial_dir / f"{name}_b_room.png"), full_page=False)
            except Exception:
                pass
    except Exception as e:
        if not error_msg:
            error_msg = f"flow failed: {e}"

    try:
        ctx.close()
        browser.close()
    except Exception:
        pass

    result = {
        "scenario": name,
        "labelZh": scenario.get("label_zh", name),
        "type": scenario.get("type"),
        "schemaVersion": SCHEMA_VERSION,
        "tier": tier.name,
        "adapter": adapter.name,
        "stableWaitMs": STABLE_WAIT_MS,
        "timing": timing,
        "snapshot": snap_a if scenario.get("type") == "lobby_only" else None,
        "snapshot_a_lobby": snap_a if scenario.get("type") == "lobby_then_room" else None,
        "snapshot_b_room": snap_b if scenario.get("type") == "lobby_then_room" else None,
        "delta_room_vs_lobby": _delta(snap_b, snap_a) if scenario.get("type") == "lobby_then_room" else None,
        "error": error_msg,
        "console": _summarize_console(console_msgs),
        "network": _summarize_network(bad_responses, request_failures),
        "listenerBuffer": listener_buffer if listener_buffer else None,
        "extra": extra_meta,
    }
    out_json = trial_dir / f"{name}.json"
    out_json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def run_trial(pw, adapter, tier, trial_dir: Path, headless, viewport, url, nav_kwargs):
    trial_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for scenario in adapter.list_scenarios():
        print(f"\n[trial] {scenario['name']} ({scenario.get('label_zh', '')})", flush=True)
        result = collect_scenario(
            pw, adapter, tier, scenario, trial_dir, headless, viewport, url, nav_kwargs,
        )
        tier.print_scenario_summary(result)
        results.append(result)
    return results


def build_summary(adapter, tier, all_trials: list[list[dict[str, Any]]]) -> dict[str, Any]:
    """跨 trial 對齊：每場景把 N 次的 tier-extracted 指標放成 list。"""
    by_scenario: dict[str, dict[str, Any]] = {}
    for s in adapter.list_scenarios():
        by_scenario[s["name"]] = {
            "labelZh": s.get("label_zh", s["name"]),
            "type": s.get("type"),
            "tier": tier.name,
            "adapter": adapter.name,
            "schemaVersion": SCHEMA_VERSION,
            "trials": [],
        }
    for trial_idx, trial_results in enumerate(all_trials, start=1):
        for r in trial_results:
            sname = r["scenario"]
            if sname not in by_scenario:
                continue
            common: dict[str, Any] = {
                "trial": trial_idx,
                "consoleErrors": r["console"]["errorCount"],
                "consoleWarnings": r["console"]["warningCount"],
                "badResponses": r["network"]["badResponseCount"],
                "error": r.get("error"),
                "timing": r.get("timing"),
            }
            if r.get("type") == "lobby_only":
                common.update(tier.extract_summary_metrics(r.get("snapshot"), r.get("listenerBuffer")))
            elif r.get("type") == "lobby_then_room":
                common["lobby"] = tier.extract_summary_metrics(r.get("snapshot_a_lobby"), r.get("listenerBuffer"))
                common["roomAfter"] = tier.extract_summary_metrics(r.get("snapshot_b_room"), r.get("listenerBuffer"))
                common["deltaRoomVsLobby"] = r.get("delta_room_vs_lobby")
            common["extra"] = r.get("extra") or {}
            by_scenario[sname]["trials"].append(common)

    # E4 memoryGrowthMB — 跨 trial diff（trial N usedJSHeapSize - trial 1）
    if tier.name in ("upgrade", "advanced"):
        for sname, scen in by_scenario.items():
            trials = scen.get("trials", [])
            if len(trials) < 2:
                continue
            t1_mem = (trials[0].get("memoryUsedMB")
                      or (trials[0].get("lobby") or {}).get("memoryUsedMB"))
            for t in trials[1:]:
                tn_mem = t.get("memoryUsedMB") or (t.get("lobby") or {}).get("memoryUsedMB")
                if isinstance(t1_mem, (int, float)) and isinstance(tn_mem, (int, float)):
                    t["memoryGrowthMB"] = round(tn_mem - t1_mem, 2)
    return by_scenario


# ── CLI / Interactive ──────────────────────────────────────────────────────

def _interactive_prompt() -> argparse.Namespace:
    print("\n=== Performance Runner — Interactive Mode ===\n")
    tier = input("  Tier (basic / upgrade / advanced) [upgrade]: ").strip() or "upgrade"
    adapter = input("  Adapter (generic-url / product-react / product-egret) [product-react]: ").strip() or "product-react"
    url = input("  URL (空白用 adapter 預設): ").strip() or None
    trials = input("  Trials [1]: ").strip() or "1"
    headless_in = input("  Headless? (y/N): ").strip().lower()
    default_out = str(Path(__file__).resolve().parents[2] / "report" / "performance" / "browser")
    out = input(f"  Output dir [{default_out}]: ").strip() or default_out
    return argparse.Namespace(
        tier=tier,
        adapter=adapter,
        url=url,
        trials=int(trials),
        headless=headless_in == "y",
        out=out,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Perf baseline runner (tier × adapter)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Tier 範圍：
  basic     Web Vitals 5 + DOM/resource count + memory + console + 4xx-5xx + nav wall clock
  upgrade   Basic + 進房Δ + byMime/byHost/dup/compression + cacheStats/wsStats + preloadHitRate + memoryGrowth + SW
  advanced  Upgrade + 互動延遲 + CDP coverage（stub，下個 deliverable）

Adapter：
  generic-url    純 navigate，無進房（任何 URL）
  product-react  <PRODUCT> UAT React (tss URL → click_lobby_tab → enter_room)
  product-egret  <PRODUCT> UAT Egret (entry form → RootPageStore.enterGameByVid)
""",
    )
    parser.add_argument("--tier", choices=["basic", "upgrade", "advanced"], default=None)
    parser.add_argument("--adapter",
                        choices=["generic-url", "product-react", "product-egret"],
                        default=None)
    parser.add_argument("--url", default=None,
                        help="目標 URL（generic-url 必填；product-* 可選不給走預設 login flow）")
    parser.add_argument("--trials", type=int, default=1)
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--out", default=str(Path(__file__).resolve().parents[2] / "report" / "performance" / "browser"))
    parser.add_argument("--user", default=None, help="Egret 帳號（預設 <ACCOUNT>）")
    parser.add_argument("--pid", default=None, help="PID（React 預設 <ACCOUNT> / Egret 預設 <ACCOUNT>）")
    parser.add_argument("--ready-selector", default=None,
                        help="generic-url 額外 ready selector")
    args = parser.parse_args(argv)

    # 沒給 tier/adapter 進 interactive
    if args.tier is None or args.adapter is None:
        ns = _interactive_prompt()
        args.tier = ns.tier
        args.adapter = ns.adapter
        if ns.url:
            args.url = ns.url
        args.trials = ns.trials
        args.headless = ns.headless
        args.out = ns.out

    try:
        adapter = get_adapter(args.adapter)
        tier = get_tier(args.tier)
    except ValueError as e:
        print(f"[error] {e}", file=sys.stderr)
        return 2

    # 預設 viewport 看 adapter
    viewport = {"width": 1920, "height": 1080} if args.adapter == "product-egret" else {"width": 1366, "height": 900}

    # adapter 額外 nav kwargs
    nav_kwargs: dict[str, Any] = {}
    if args.user:
        nav_kwargs["user"] = args.user
    if args.pid:
        nav_kwargs["pid"] = args.pid
    if args.ready_selector and args.adapter == "generic-url":
        nav_kwargs["ready_selector"] = args.ready_selector

    # advanced tier 早爆
    if args.tier == "advanced":
        try:
            tier.extract_summary_metrics(None)
        except NotImplementedError as e:
            print(f"[advanced not ready] {e}", file=sys.stderr)
            return 3

    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_root = Path(args.out) / f"perf_{args.adapter.replace('-', '_')}_{timestamp}"
    out_root.mkdir(parents=True, exist_ok=True)
    print(f"[info] tier={args.tier}, adapter={args.adapter}, trials={args.trials}, headless={args.headless}")
    print(f"[info] output: {out_root.absolute()}")

    all_trials: list[list[dict[str, Any]]] = []
    with sync_playwright() as pw:
        for trial_idx in range(1, args.trials + 1):
            trial_dir = out_root / f"trial_{trial_idx}"
            print(f"\n=== Trial {trial_idx}/{args.trials} ===")
            t0 = time.time()
            trial_results = run_trial(pw, adapter, tier, trial_dir, args.headless, viewport,
                                      args.url, nav_kwargs)
            elapsed = int(time.time() - t0)
            print(f"  trial {trial_idx} 耗時 {elapsed}s")
            all_trials.append(trial_results)

    summary = build_summary(adapter, tier, all_trials)
    validate_summary_schema(summary)
    summary_path = out_root / "summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[done] summary: {summary_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
