"""
performance_baseline_collector.py — 三場景效能基線收集器

對 <PRODUCT> React 三場景各自 cold-start：
- lobby：cold-start 進大廳，量純 Web Vitals
- baccarat_room / sicbo_room：cold-start 進大廳 → 點 tab → 點房卡 → 進房 ready，
  Web Vitals 只算大廳那段，**進房成本另列為「操作 + 載入」wall-clock + delta 指標**
  （不混進 Web Vitals — 操作時間不算網頁效能）

每場景獨立 browser context + 新 PerformanceObserver，從 0 開始量，互不污染。

設計依據
--------
- Lighthouse / web-vitals.js 標準：Web Vitals 只量單一 URL navigation，**不含使用者互動**
- <PRODUCT> 不支援 entry URL 帶 hash 進房（redirect 過程吃掉 hash，已實測）
- 因此進房必須走完整路徑，並把「操作 + 進房載入」wall-clock 獨立出來不混 Web Vitals

收集內容
--------
- 大廳 cold-start：Web Vitals (LCP/CLS/INP/FCP)、Long Tasks、Navigation Timing、
  Resource、Memory、console errors、4xx-5xx
- 進房：操作 wall-clock 拆 (tab click / room click / room ready)
  + 進房後 delta（long tasks / TBT / resource count / resource bytes / DOM / memory）

Usage
-----
    # 跑 1 trial（預設）
    python performance_baseline_collector.py

    # 跑 2 trials 比對一致性（推薦）
    python performance_baseline_collector.py --trials 2

    # headless
    python performance_baseline_collector.py --headless --trials 2

    # 自帶 URL（不重取）
    python performance_baseline_collector.py --url "https://example.internal/pa/pc/?...&tss=..."

Output
------
    <repo>/react/report/performance/browser/performance_baseline_<YYYYmmdd_HHMMSS>/
        trial_1/
            lobby.json
            baccarat_room.json
            sicbo_room.json
            *.png
        trial_2/
            ...
        summary.json   # 每場景跨 trial 的指標總覽
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any
from playwright.sync_api import BrowserContext, Page, sync_playwright

# Windows console cp950 編不了 emoji（⏱ ⚠️）— 強制 utf-8（對齊 Egret collector）
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

from react_client_autobet import click_lobby_tab, enter_room
from react_client_selectors import GAME_CARD_READY, LOBBY_MENU
from performance_baseline_shared import (
    INIT_OBSERVER_JS,
    SNAPSHOT_JS,
    _summarize_console,
    _summarize_network,
    _delta,
    _extract_lobby_metrics,
)


# ── 三場景定義 ────────────────────────────────────────────────────────────────
# union selector 涵蓋百家樂 (PcMainGame_timer / PlayTypeText) 與骰寶 (bet-item-gr)
GAME_ROOM_READY_UNION = (
    '[class*="PcMainGame_timer"],[class*="PlayTypeText"],'
    '[class*="bet-item-gr"],[class*="timer_container"],'
    '[class*="GameInfo"],[class*="RoadMap"]'
)

# scenario.type:
#   "lobby_only"       → 純 cold-start 大廳，量 Web Vitals
#   "lobby_then_room"  → cold-start 大廳 + 拍 snapshot_A + 切 tab + 進房 + 拍 snapshot_B + 算 delta
SCENARIOS: list[dict[str, Any]] = [
    {
        "name": "lobby",
        "label_zh": "大廳",
        "type": "lobby_only",
    },
    {
        "name": "baccarat_room",
        "label_zh": "百家樂房間 N006",
        "type": "lobby_then_room",
        "tab": "百家樂",
        "room": "N006",
    },
    {
        "name": "sicbo_room",
        "label_zh": "骰寶房間 N026",
        "type": "lobby_then_room",
        "tab": "骰寶",
        "room": "N026",
    },
]

STABLE_WAIT_MS = 8000  # ready 後再等 8 秒讓 LCP/CLS 穩定（<PRODUCT> loading 偏慢）


# INIT_OBSERVER_JS / SNAPSHOT_JS 已移到 performance_baseline_shared.py（top-level import）


def _get_url_from_login_link() -> str | None:
    """跑 get_login_link.py 取得 fresh URL。"""
    here = Path(__file__).parent
    script = here / "get_login_link.py"
    proc = subprocess.run(
        [sys.executable, str(script), "--env", "uat", "--pid", "<ACCOUNT>"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    out = (proc.stdout or "") + "\n" + (proc.stderr or "")
    for line in out.splitlines():
        line = line.strip()
        if line.startswith("https://") and "tss=" in line:
            return line
    return None


def _new_context_with_observer(pw, headless: bool) -> tuple[Any, BrowserContext, Page,
                                                              list, list, list]:
    """建立 fresh browser/context/page，注入 PerformanceObserver，掛 listener。"""
    console_msgs: list[dict[str, Any]] = []
    bad_responses: list[dict[str, Any]] = []
    request_failures: list[dict[str, Any]] = []

    browser = pw.chromium.launch(headless=headless)
    ctx: BrowserContext = browser.new_context(
        viewport={"width": 1366, "height": 900},
        ignore_https_errors=True,
    )
    ctx.add_init_script(INIT_OBSERVER_JS)
    page: Page = ctx.new_page()

    page.on("console", lambda msg: console_msgs.append({
        "type": msg.type, "text": msg.text[:500],
    }))
    page.on("response", lambda r: bad_responses.append({
        "url": r.url, "status": r.status,
    }) if r.status >= 400 else None)
    page.on("requestfailed", lambda req: request_failures.append({
        "url": req.url, "failure": req.failure or "unknown",
        "method": req.method, "resourceType": req.resource_type,
    }))
    return browser, ctx, page, console_msgs, bad_responses, request_failures


# _summarize_console / _summarize_network 已移到 performance_baseline_shared.py


def _collect_lobby_only(
    pw, base_url: str, scenario: dict[str, Any], headless: bool, out_dir: Path
) -> dict[str, Any]:
    """場景 1：純 cold-start 進大廳，量 Web Vitals。"""
    name = scenario["name"]
    browser, ctx, page, console_msgs, bad_responses, request_failures = (
        _new_context_with_observer(pw, headless)
    )

    error_msg = None
    snap: dict[str, Any] | None = None
    nav_wall_clock_ms = 0
    ready_wall_clock_ms = 0

    try:
        t0 = time.time()
        page.goto(base_url, wait_until="load", timeout=60000)
        nav_wall_clock_ms = int((time.time() - t0) * 1000)
        try:
            page.wait_for_selector(LOBBY_MENU, timeout=60000)
            ready_wall_clock_ms = int((time.time() - t0) * 1000)
        except Exception as e:
            error_msg = f"LOBBY_MENU timeout: {e}"
        page.wait_for_timeout(STABLE_WAIT_MS)
        snap = page.evaluate(SNAPSHOT_JS)
        try:
            page.screenshot(path=str(out_dir / f"{name}.png"), full_page=False)
        except Exception:
            pass
    except Exception as e:
        error_msg = f"navigation failed: {e}"

    ctx.close()
    browser.close()

    return {
        "scenario": name,
        "labelZh": scenario["label_zh"],
        "type": "lobby_only",
        "navWallClockMs": nav_wall_clock_ms,
        "readyWallClockMs": ready_wall_clock_ms,
        "stableWaitMs": STABLE_WAIT_MS,
        "snapshot": snap,
        "error": error_msg,
        "console": _summarize_console(console_msgs),
        "network": _summarize_network(bad_responses, request_failures),
    }


# _delta 已移到 performance_baseline_shared.py


def _collect_lobby_then_room(
    pw, base_url: str, scenario: dict[str, Any], headless: bool, out_dir: Path
) -> dict[str, Any]:
    """場景 2/3：cold-start lobby → tab → room，量大廳 Web Vitals + 進房 wall-clock + delta。"""
    name = scenario["name"]
    tab_kw: str = scenario["tab"]
    room_id: str = scenario["room"]
    browser, ctx, page, console_msgs, bad_responses, request_failures = (
        _new_context_with_observer(pw, headless)
    )

    error_msg = None
    snap_a: dict[str, Any] | None = None  # 大廳 baseline
    snap_b: dict[str, Any] | None = None  # 進房後
    timing = {
        "navWallClockMs": 0,
        "lobbyReadyMs": 0,         # goto → LOBBY_MENU 出現
        "tabClickMs": 0,           # click tab → cards ready
        "roomEnterMs": 0,          # click room card → 遊戲室 ready
        "totalEnterRoomMs": 0,     # tab click 起算 → 遊戲室 ready 共多久
    }

    try:
        t0 = time.time()
        page.goto(base_url, wait_until="load", timeout=60000)
        timing["navWallClockMs"] = int((time.time() - t0) * 1000)

        try:
            page.wait_for_selector(LOBBY_MENU, timeout=60000)
            timing["lobbyReadyMs"] = int((time.time() - t0) * 1000)
        except Exception as e:
            error_msg = f"LOBBY_MENU timeout: {e}"
            raise

        # 大廳穩定 → 拍 baseline
        page.wait_for_timeout(STABLE_WAIT_MS)
        snap_a = page.evaluate(SNAPSHOT_JS)
        try:
            page.screenshot(path=str(out_dir / f"{name}_a_lobby.png"), full_page=False)
        except Exception:
            pass

        # ── 切 tab → 等卡片 ─────────────────────────────────────────────────
        t_tab = time.time()
        if not click_lobby_tab(page, tab_kw):
            error_msg = f"click_lobby_tab failed for {tab_kw}"
            raise RuntimeError(error_msg)
        try:
            page.wait_for_selector(GAME_CARD_READY, timeout=15000)
        except Exception:
            pass  # 部分 tab 卡片載入較慢，best-effort
        timing["tabClickMs"] = int((time.time() - t_tab) * 1000)

        # ── 點房卡 → 等遊戲室 ready ─────────────────────────────────────────
        t_room = time.time()
        room_ok = enter_room(page, room_id)
        if not room_ok:
            error_msg = f"enter_room({room_id}) failed"
            raise RuntimeError(error_msg)
        try:
            page.wait_for_selector(GAME_ROOM_READY_UNION, timeout=30000)
        except Exception as e:
            error_msg = f"game room ready timeout: {e}"
        timing["roomEnterMs"] = int((time.time() - t_room) * 1000)
        timing["totalEnterRoomMs"] = int((time.time() - t_tab) * 1000)

        # 進房穩定 → 拍 after snapshot
        page.wait_for_timeout(STABLE_WAIT_MS)
        snap_b = page.evaluate(SNAPSHOT_JS)
        try:
            page.screenshot(path=str(out_dir / f"{name}_b_room.png"), full_page=False)
        except Exception:
            pass

    except Exception as e:
        if not error_msg:
            error_msg = f"flow failed: {e}"

    ctx.close()
    browser.close()

    return {
        "scenario": name,
        "labelZh": scenario["label_zh"],
        "type": "lobby_then_room",
        "tab": tab_kw,
        "room": room_id,
        "stableWaitMs": STABLE_WAIT_MS,
        "timing": timing,
        "snapshot_a_lobby": snap_a,
        "snapshot_b_room": snap_b,
        "delta_room_vs_lobby": _delta(snap_b, snap_a),
        "error": error_msg,
        "console": _summarize_console(console_msgs),
        "network": _summarize_network(bad_responses, request_failures),
    }


def collect_scenario(
    pw,
    base_url: str,
    scenario: dict[str, Any],
    headless: bool,
    out_dir: Path,
) -> dict[str, Any]:
    """依 scenario.type 分派。"""
    if scenario["type"] == "lobby_only":
        result = _collect_lobby_only(pw, base_url, scenario, headless, out_dir)
    elif scenario["type"] == "lobby_then_room":
        result = _collect_lobby_then_room(pw, base_url, scenario, headless, out_dir)
    else:
        raise ValueError(f"unknown scenario type: {scenario['type']}")
    out_json = out_dir / f"{scenario['name']}.json"
    out_json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def _print_scenario_summary(scenario_result: dict[str, Any]) -> None:
    name = scenario_result["scenario"]
    err = scenario_result.get("error")
    if err:
        print(f"  [{name}] ⚠️ {err}")
    if scenario_result.get("type") == "lobby_only":
        snap = scenario_result.get("snapshot") or {}
        _print_lobby_block(name, snap, scenario_result)
    elif scenario_result.get("type") == "lobby_then_room":
        snap_a = scenario_result.get("snapshot_a_lobby") or {}
        _print_lobby_block(name + "(lobby)", snap_a, scenario_result)
        timing = scenario_result.get("timing", {})
        delta = scenario_result.get("delta_room_vs_lobby", {})
        print(
            f"    enter-room ⏱: tab={timing.get('tabClickMs')}ms "
            f"room={timing.get('roomEnterMs')}ms total={timing.get('totalEnterRoomMs')}ms"
        )
        cls_d = delta.get("clsDelta")
        cls_d_str = f"{cls_d:+.4f}" if isinstance(cls_d, (int, float)) else "N/A"
        mem_d = delta.get("memoryUsedDeltaMB")
        mem_d_str = f"{mem_d:+.2f}" if isinstance(mem_d, (int, float)) else "N/A"
        print(
            f"    Δ room vs lobby: longTasks +{delta.get('longTasksCountDelta')}, "
            f"TBT +{delta.get('totalBlockingMsDelta')}ms, "
            f"resource +{delta.get('resourceCountDelta')}/+"
            f"{(delta.get('resourceTransferBytesDelta') or 0)/1024:.1f}KB, "
            f"CLSΔ={cls_d_str}, "
            f"DOM={delta.get('domNodesAfter')}, "
            f"memΔ={mem_d_str}MB"
        )
    print(
        f"    console err={scenario_result['console']['errorCount']} "
        f"warn={scenario_result['console']['warningCount']}  "
        f"4xx-5xx={scenario_result['network']['badResponseCount']}  "
        f"reqFail={scenario_result['network']['requestFailureCount']}"
    )


def _print_lobby_block(name: str, snap: dict[str, Any], scenario_result: dict[str, Any]) -> None:
    if not snap:
        print(f"  [{name}] (no snapshot)")
        return
    wv = snap.get("webVitals", {}) or {}
    lt = snap.get("longTasks", {}) or {}
    paint = snap.get("paint", {}) or {}
    cls = wv.get("cls")
    cls_str = f"{cls:.4f}" if isinstance(cls, (int, float)) else "N/A"
    tbt = lt.get("totalBlockingMs", 0)
    tbt_str = f"{tbt:.0f}" if isinstance(tbt, (int, float)) else "N/A"
    if scenario_result.get("type") == "lobby_only":
        ready_ms = scenario_result.get("readyWallClockMs")
    else:
        ready_ms = (scenario_result.get("timing") or {}).get("lobbyReadyMs")
    print(
        f"  [{name:22s}] "
        f"LCP={wv.get('lcp')}  CLS={cls_str}  INP={wv.get('inp')}  "
        f"FCP={paint.get('firstContentfulPaint')}  "
        f"longTasks={lt.get('count')}  TBT~{tbt_str}ms  "
        f"DOM={snap.get('domNodes')}  ready={ready_ms}ms"
    )


def run_trial(
    pw, base_url: str, headless: bool, trial_dir: Path
) -> list[dict[str, Any]]:
    trial_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for scenario in SCENARIOS:
        print(f"\n[trial] 場景：{scenario['name']} ({scenario['label_zh']})", flush=True)
        result = collect_scenario(pw, base_url, scenario, headless, trial_dir)
        _print_scenario_summary(result)
        results.append(result)
    return results


# _extract_lobby_metrics 已移到 performance_baseline_shared.py


def build_summary(all_trials: list[list[dict[str, Any]]]) -> dict[str, Any]:
    """跨 trial 對齊：每場景把 N 次的關鍵指標放成 list 供人眼/後續工具比對。"""
    by_scenario: dict[str, dict[str, Any]] = {}
    for s in SCENARIOS:
        by_scenario[s["name"]] = {
            "labelZh": s["label_zh"],
            "type": s["type"],
            "engine": "react",  # 對齊 Egret collector 的 engine field（schema 對稱）
            "trials": [],
        }
    for trial_idx, trial_results in enumerate(all_trials, start=1):
        for r in trial_results:
            sname = r["scenario"]
            common = {
                "trial": trial_idx,
                "consoleErrors": r["console"]["errorCount"],
                "consoleWarnings": r["console"]["warningCount"],
                "badResponses": r["network"]["badResponseCount"],
                "error": r.get("error"),
            }
            if r.get("type") == "lobby_only":
                common.update(_extract_lobby_metrics(r.get("snapshot")))
                common["navWallClockMs"] = r.get("navWallClockMs")
                common["readyWallClockMs"] = r.get("readyWallClockMs")
            else:
                common["lobby"] = _extract_lobby_metrics(r.get("snapshot_a_lobby"))
                common["roomAfter"] = _extract_lobby_metrics(r.get("snapshot_b_room"))
                common["timing"] = r.get("timing", {})
                common["deltaRoomVsLobby"] = r.get("delta_room_vs_lobby", {})
            by_scenario[sname]["trials"].append(common)
    return by_scenario


def main() -> int:
    print(
        "\n[DEPRECATION] performance_baseline_collector.py 已 deprecated。\n"
        "  → 請改用 perf_runner.py：\n"
        "    python perf_runner.py --tier upgrade --adapter product-react --trials N\n"
        "  本檔保留 backward compat 維持舊命令可用，但不再加新功能。\n",
        file=sys.stderr,
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="預先取好的 <PRODUCT> URL（含 tss）；不給就跑 get_login_link")
    parser.add_argument("--trials", type=int, default=1, help="重複跑幾輪做一致性比對")
    parser.add_argument("--headless", action="store_true", help="無頭模式")
    parser.add_argument("--out", help="輸出資料夾（預設 <repo>/react/report/performance/browser/performance_baseline_<ts>）")
    parser.add_argument("--fresh-url-per-trial", action="store_true",
                        help="每 trial 重新跑 get_login_link 取 fresh URL（保險，但慢 ~30s/trial）")
    args = parser.parse_args()

    base_url = args.url
    if not base_url:
        print("[info] 未指定 --url，跑 get_login_link 取 fresh URL...", flush=True)
        base_url = _get_url_from_login_link()
        if not base_url:
            print("[error] get_login_link 沒回傳 URL", file=sys.stderr)
            return 2

    if not args.out:
        ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        out_dir = Path(__file__).resolve().parents[2] / "report" / "performance" / "browser" / f"performance_baseline_{ts}"
    else:
        out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[info] 輸出: {out_dir}", flush=True)
    print(f"[info] 場景數: {len(SCENARIOS)}, trials: {args.trials}", flush=True)

    all_trials: list[list[dict[str, Any]]] = []
    with sync_playwright() as pw:
        for trial_idx in range(1, args.trials + 1):
            print(f"\n=== Trial {trial_idx}/{args.trials} ===", flush=True)
            if args.fresh_url_per_trial and trial_idx > 1:
                print("[info] fresh-url-per-trial 啟用，重取 URL...", flush=True)
                fresh = _get_url_from_login_link()
                if fresh:
                    base_url = fresh
                else:
                    print("[warn] 重取 URL 失敗，沿用原 URL", file=sys.stderr)

            trial_dir = out_dir / f"trial_{trial_idx}"
            trial_results = run_trial(pw, base_url, args.headless, trial_dir)
            all_trials.append(trial_results)

    summary = build_summary(all_trials)
    summary_path = out_dir / "summary.json"
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print("\n=== Cross-trial Summary ===")
    for sname, info in summary.items():
        print(f"\n[{sname}] {info['labelZh']} ({info['type']})")
        for t in info["trials"]:
            if info["type"] == "lobby_only":
                cls = t.get("cls")
                cls_str = f"{cls:.4f}" if isinstance(cls, (int, float)) else "N/A"
                print(
                    f"  trial {t['trial']}: LCP={t.get('lcp')}  CLS={cls_str}  "
                    f"TBT={t.get('totalBlockingMs')}  DOM={t.get('domNodes')}  "
                    f"err={t.get('consoleErrors')}  bad={t.get('badResponses')}  "
                    f"ready={t.get('readyWallClockMs')}ms"
                )
            else:
                lobby = t.get("lobby") or {}
                timing = t.get("timing") or {}
                delta = t.get("deltaRoomVsLobby") or {}
                cls = lobby.get("cls")
                cls_str = f"{cls:.4f}" if isinstance(cls, (int, float)) else "N/A"
                print(
                    f"  trial {t['trial']}: lobby LCP={lobby.get('lcp')} CLS={cls_str} "
                    f"TBT={lobby.get('totalBlockingMs')} | "
                    f"enter-room tab={timing.get('tabClickMs')}ms "
                    f"room={timing.get('roomEnterMs')}ms total={timing.get('totalEnterRoomMs')}ms | "
                    f"Δ longTasks +{delta.get('longTasksCountDelta')} "
                    f"TBT +{delta.get('totalBlockingMsDelta')}ms"
                )
                if t.get("error"):
                    print(f"     ⚠️  {t['error']}")

    print(f"\n[done] summary: {summary_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
