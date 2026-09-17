"""performance_baseline_collector_egret.py — Egret 三場景效能基線收集器

對齊 React 版範式（performance_baseline_collector.py），但：
- 登入：走 example.internal/uatgame/ <PRODUCT> 表單 → Enter AGIN（新分頁）
- 進房：用 RootPageStore._instance.enterGameByVid(vid) — 不 click 座標、不 dispatchTouchEvent
- vid：從 VideoGameCore.RoomConfig.instance.getRoomInfosByType(gmtype) 動態取
- 三場景：lobby cold-start / baccarat_room (BAC 第一桌) / sicbo_room (SHB 第一桌)

每場景獨立 fresh chromium.launch + new_context（無 storage_state，等同無痕），三場景互不污染。

替代座標技術選型：T9 RootPageStore.enterGameByVid（單行 store API call）。
詳見 reports/egret_recon/click_alternatives.md。

USAGE
-----
    python performance_baseline_collector_egret.py
    python performance_baseline_collector_egret.py --trials 2 --headless
    python performance_baseline_collector_egret.py --user USER01 --pid PID01

OUTPUT
------
    <repo>/react/report/performance/browser/performance_baseline_egret_<YYYYmmdd_HHMMSS>/
        trial_1/
            lobby.json
            baccarat_room.json
            sicbo_room.json
            *.png
        trial_2/ ...
        summary.json
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

# Windows console cp950 編不了 emoji（⏱ ⚠️ 等）— 強制 utf-8（對齊 jira_ticket_perf_react.py）
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

from performance_baseline_shared import (
    INIT_OBSERVER_JS,
    SNAPSHOT_JS,
    _summarize_console,
    _summarize_network,
    _extract_lobby_metrics,
    _delta,
)


# ── 三場景定義（對齊 React baccarat_room=N006 / sicbo_room=N026 命名）────────
EGRET_SCENARIOS: list[dict[str, Any]] = [
    {"name": "lobby", "label_zh": "大廳 (PCPlaza)", "type": "lobby_only"},
    {"name": "baccarat_room", "label_zh": "百家樂 BAC 第一桌", "type": "lobby_then_room",
     "gmtype": "BAC", "expected_module": "GameBac"},
    {"name": "sicbo_room", "label_zh": "骰寶 SHB 第一桌", "type": "lobby_then_room",
     "gmtype": "SHB", "expected_module": "GameShb"},
]

ENTRY_URL = "https://example.internal/uatgame/"
DEFAULT_USER = "USER01"
DEFAULT_PID = "PID01"
STABLE_WAIT_MS = 8000  # 等 LCP/CLS 穩定（沿用 React 範式）
LOBBY_READY_TIMEOUT_MS = 60000
ROOM_READY_TIMEOUT_MS = 30000


# ── helpers ──────────────────────────────────────────────────────────────────

def _new_egret_context(pw, headless: bool):
    """fresh browser/context/entry-page，注入 PerformanceObserver 在 ctx 級
    （ctx 內所有 page 都會自動套用，包含 entry login 後新開的 lobby_page）。"""
    console_msgs: list[dict[str, Any]] = []
    bad_responses: list[dict[str, Any]] = []
    request_failures: list[dict[str, Any]] = []

    browser = pw.chromium.launch(headless=headless)
    ctx: BrowserContext = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        ignore_https_errors=True,
    )
    ctx.add_init_script(INIT_OBSERVER_JS)
    return browser, ctx, console_msgs, bad_responses, request_failures


def _attach_listeners(page: Page, console_msgs, bad_responses, request_failures):
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


def _egret_login_via_entry(ctx: BrowserContext, user: str, pid: str,
                           console_msgs, bad_responses, request_failures) -> tuple[Page, int]:
    """走 example.internal/uatgame/ <PRODUCT> 表單 → Enter AGIN，回傳 (lobby_page, login_wall_clock_ms)。

    <PRODUCT> 是第一個（最左）區塊。表單預設：
      USER=UAT01 / ACTYPE=Real / PID=PID01 / CUR=CNY / LANG=CN / GAMETYPE=<PRODUCT>大廳-0 / MH5=PC
    我們只需改 USER 為 USER01（如非 default）+ Enter AGIN。
    """
    t0 = time.time()
    entry_page = ctx.new_page()
    _attach_listeners(entry_page, console_msgs, bad_responses, request_failures)
    entry_page.goto(ENTRY_URL, wait_until="load", timeout=60000)

    # <PRODUCT> 區塊 USER 下拉（first = <PRODUCT> 區塊）
    if user != "UAT01":
        entry_page.get_by_role("button", name="USER UAT01").first.click()
        entry_page.get_by_role("option", name=user).first.click()

    # PID 預設 PID01，若使用者要求其他 PID 才改
    if pid != "PID01":
        entry_page.get_by_role("button", name="PID PID01").first.click()
        entry_page.get_by_role("option", name=pid).first.click()

    # Enter AGIN — 新分頁開
    with ctx.expect_page() as new_pp:
        entry_page.get_by_role("button", name="Enter AGIN").click()
    lobby_page = new_pp.value
    _attach_listeners(lobby_page, console_msgs, bad_responses, request_failures)

    # 關閉 entry 分頁節省 RAM（可選，不影響量測）
    try:
        entry_page.close()
    except Exception:
        pass

    return lobby_page, int((time.time() - t0) * 1000)


def _wait_egret_module(page: Page, expected: str, timeout: int) -> bool:
    """等 PCPlaza.RootPageStore._instance.getCurrentModule() === expected。"""
    try:
        page.wait_for_function(
            f"() => {{"
            f"  const inst = window.PCPlaza && window.PCPlaza.RootPageStore && window.PCPlaza.RootPageStore._instance;"
            f"  return inst && inst.getCurrentModule && inst.getCurrentModule() === '{expected}';"
            f"}}",
            timeout=timeout,
        )
        return True
    except Exception:
        return False


def _egret_get_first_vid(page: Page, gmtype: str) -> str | None:
    """從 VideoGameCore.RoomConfig 取指定 gmtype 的第一個 vid。"""
    return page.evaluate(
        f"""() => {{
            const rc = window.VideoGameCore && window.VideoGameCore.RoomConfig && window.VideoGameCore.RoomConfig.instance;
            if (!rc) return null;
            const list = rc.getRoomInfosByType('{gmtype}');
            return Array.isArray(list) && list.length > 0 ? list[0].vid : null;
        }}"""
    )


def _egret_enter_game_by_vid(page: Page, vid: str):
    page.evaluate(
        f"""() => {{
            const inst = window.PCPlaza.RootPageStore._instance;
            inst.enterGameByVid('{vid}');
        }}"""
    )


# ── 場景 collectors ──────────────────────────────────────────────────────────

def _collect_lobby_only_egret(pw, scenario: dict, headless: bool, out_dir: Path,
                              user: str, pid: str) -> dict[str, Any]:
    name = scenario["name"]
    browser, ctx, console_msgs, bad_responses, request_failures = _new_egret_context(pw, headless)
    error_msg = None
    snap = None
    login_ms = 0
    lobby_ready_ms = 0
    warn_invalid_snapshot = False  # P0-1 fix: 標記 module 沒 ready 時的 snapshot 不可信

    try:
        lobby_page, login_ms = _egret_login_via_entry(
            ctx, user, pid, console_msgs, bad_responses, request_failures)
        t1 = time.time()
        if not _wait_egret_module(lobby_page, "PCPlaza", LOBBY_READY_TIMEOUT_MS):
            error_msg = "lobby PCPlaza module not ready in time"
            warn_invalid_snapshot = True
        else:
            lobby_ready_ms = int((time.time() - t1) * 1000)
        # 等 LCP/CLS 穩定
        lobby_page.wait_for_timeout(STABLE_WAIT_MS)
        snap = lobby_page.evaluate(SNAPSHOT_JS)
        try:
            lobby_page.screenshot(path=str(out_dir / f"{name}.png"), full_page=False)
        except Exception:
            pass
    except Exception as e:
        error_msg = error_msg or f"flow failed: {e}"

    try:
        ctx.close()
        browser.close()
    except Exception:
        pass

    return {
        "scenario": name,
        "labelZh": scenario["label_zh"],
        "type": "lobby_only",
        "engine": "egret",
        "user": user,
        "pid": pid,
        "loginWallClockMs": login_ms,
        "lobbyReadyMs": lobby_ready_ms,
        "stableWaitMs": STABLE_WAIT_MS,
        "snapshot": snap,
        "error": error_msg,
        "warnInvalidSnapshot": warn_invalid_snapshot,
        "console": _summarize_console(console_msgs),
        "network": _summarize_network(bad_responses, request_failures),
    }


def _collect_lobby_then_room_egret(pw, scenario: dict, headless: bool, out_dir: Path,
                                   user: str, pid: str) -> dict[str, Any]:
    name = scenario["name"]
    gmtype = scenario["gmtype"]
    expected_module = scenario["expected_module"]
    browser, ctx, console_msgs, bad_responses, request_failures = _new_egret_context(pw, headless)
    error_msg = None
    snap_a = None
    snap_b = None
    warn_invalid_snapshot_b = False  # P0-2 fix: room module 沒 ready 時 snapshot_b 不可信
    timing = {
        "loginWallClockMs": 0,
        "lobbyReadyMs": 0,
        "vidLookupMs": 0,
        "roomEnterMs": 0,
    }
    used_vid = None

    try:
        lobby_page, login_ms = _egret_login_via_entry(
            ctx, user, pid, console_msgs, bad_responses, request_failures)
        timing["loginWallClockMs"] = login_ms

        t_lobby = time.time()
        if not _wait_egret_module(lobby_page, "PCPlaza", LOBBY_READY_TIMEOUT_MS):
            error_msg = "lobby PCPlaza module not ready"
            raise RuntimeError(error_msg)
        timing["lobbyReadyMs"] = int((time.time() - t_lobby) * 1000)
        lobby_page.wait_for_timeout(STABLE_WAIT_MS)
        snap_a = lobby_page.evaluate(SNAPSHOT_JS)
        try:
            lobby_page.screenshot(path=str(out_dir / f"{name}_a_lobby.png"), full_page=False)
        except Exception:
            pass

        # 取 vid + enterGameByVid
        t_vid = time.time()
        used_vid = _egret_get_first_vid(lobby_page, gmtype)
        timing["vidLookupMs"] = int((time.time() - t_vid) * 1000)
        if not used_vid:
            error_msg = f"no vid found for gmtype={gmtype}"
            raise RuntimeError(error_msg)

        t_room = time.time()
        _egret_enter_game_by_vid(lobby_page, used_vid)
        if not _wait_egret_module(lobby_page, expected_module, ROOM_READY_TIMEOUT_MS):
            error_msg = f"{expected_module} module not ready after enterGameByVid({used_vid})"
            warn_invalid_snapshot_b = True
        timing["roomEnterMs"] = int((time.time() - t_room) * 1000)

        lobby_page.wait_for_timeout(STABLE_WAIT_MS)
        snap_b = lobby_page.evaluate(SNAPSHOT_JS)
        try:
            lobby_page.screenshot(path=str(out_dir / f"{name}_b_room.png"), full_page=False)
        except Exception:
            pass

    except Exception as e:
        error_msg = error_msg or f"flow failed: {e}"

    try:
        ctx.close()
        browser.close()
    except Exception:
        pass

    return {
        "scenario": name,
        "labelZh": scenario["label_zh"],
        "type": "lobby_then_room",
        "engine": "egret",
        "user": user,
        "pid": pid,
        "gmtype": gmtype,
        "expectedModule": expected_module,
        "usedVid": used_vid,
        "stableWaitMs": STABLE_WAIT_MS,
        "timing": timing,
        "snapshot_a_lobby": snap_a,
        "snapshot_b_room": snap_b,
        "warnInvalidSnapshotB": warn_invalid_snapshot_b,
        "delta_room_vs_lobby": _delta(snap_b, snap_a),
        "error": error_msg,
        "console": _summarize_console(console_msgs),
        "network": _summarize_network(bad_responses, request_failures),
    }


def collect_scenario(pw, scenario, headless, out_dir, user, pid):
    if scenario["type"] == "lobby_only":
        result = _collect_lobby_only_egret(pw, scenario, headless, out_dir, user, pid)
    elif scenario["type"] == "lobby_then_room":
        result = _collect_lobby_then_room_egret(pw, scenario, headless, out_dir, user, pid)
    else:
        raise ValueError(f"unknown scenario type: {scenario['type']}")
    out_json = out_dir / f"{scenario['name']}.json"
    out_json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def _print_lobby_block(label: str, snap: dict, ready_ms_or_login: int):
    if not snap:
        print(f"  [{label}] (no snapshot)")
        return
    wv = snap.get("webVitals", {}) or {}
    lt = snap.get("longTasks", {}) or {}
    paint = snap.get("paint", {}) or {}
    cls = wv.get("cls")
    cls_str = f"{cls:.4f}" if isinstance(cls, (int, float)) else "N/A"
    tbt = lt.get("totalBlockingMs", 0)
    tbt_str = f"{tbt:.0f}" if isinstance(tbt, (int, float)) else "N/A"
    print(
        f"  [{label:24s}] LCP={wv.get('lcp')} CLS={cls_str} INP={wv.get('inp')} "
        f"FCP={paint.get('firstContentfulPaint')} longTasks={lt.get('count')} "
        f"TBT~{tbt_str}ms DOM={snap.get('domNodes')} ready={ready_ms_or_login}ms"
    )


def _print_scenario_summary(r: dict):
    name = r["scenario"]
    if r.get("error"):
        print(f"  [{name}] ⚠️ {r['error']}")
    if r["type"] == "lobby_only":
        _print_lobby_block(name, r.get("snapshot") or {}, r.get("lobbyReadyMs", 0))
    else:
        _print_lobby_block(f"{name}(lobby)", r.get("snapshot_a_lobby") or {},
                           (r.get("timing") or {}).get("lobbyReadyMs", 0))
        timing = r.get("timing", {})
        delta = r.get("delta_room_vs_lobby", {})
        used_vid = r.get("usedVid")
        cls_d = delta.get("clsDelta")
        cls_d_str = f"{cls_d:+.4f}" if isinstance(cls_d, (int, float)) else "N/A"
        print(
            f"    enter-room ⏱ vid={used_vid} login={timing.get('loginWallClockMs')}ms "
            f"vidLookup={timing.get('vidLookupMs')}ms room={timing.get('roomEnterMs')}ms"
        )
        print(
            f"    Δ room vs lobby: longTasks +{delta.get('longTasksCountDelta')}, "
            f"TBT +{delta.get('totalBlockingMsDelta')}ms, "
            f"resource +{delta.get('resourceCountDelta')}/+"
            f"{(delta.get('resourceTransferBytesDelta') or 0)/1024:.1f}KB, CLSΔ={cls_d_str}"
        )
    print(
        f"    console err={r['console']['errorCount']} warn={r['console']['warningCount']} "
        f"4xx-5xx={r['network']['badResponseCount']} reqFail={r['network']['requestFailureCount']}"
    )


def run_trial(pw, headless, trial_dir, user, pid):
    trial_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for scenario in EGRET_SCENARIOS:
        print(f"\n[trial] 場景：{scenario['name']} ({scenario['label_zh']})", flush=True)
        result = collect_scenario(pw, scenario, headless, trial_dir, user, pid)
        _print_scenario_summary(result)
        results.append(result)
    return results


def build_summary_egret(all_trials):
    """跨 trial 對齊 — 重用 React 版的 build_summary 邏輯。Egret SCENARIOS 跟 React 版是不同清單，
    所以複製 React 版的結構但用 Egret SCENARIOS 名稱。"""
    by_scenario = {s["name"]: {"labelZh": s["label_zh"], "type": s["type"], "engine": "egret",
                                "trials": []} for s in EGRET_SCENARIOS}
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
            if r["type"] == "lobby_only":
                common.update(_extract_lobby_metrics(r.get("snapshot")))
                common["loginWallClockMs"] = r.get("loginWallClockMs")
                common["lobbyReadyMs"] = r.get("lobbyReadyMs")
            else:
                common["lobby"] = _extract_lobby_metrics(r.get("snapshot_a_lobby"))
                common["roomAfter"] = _extract_lobby_metrics(r.get("snapshot_b_room"))
                common["timing"] = r.get("timing", {})
                common["deltaRoomVsLobby"] = r.get("delta_room_vs_lobby", {})
                common["usedVid"] = r.get("usedVid")
            by_scenario[sname]["trials"].append(common)
    return by_scenario


def main() -> int:
    print(
        "\n[DEPRECATION] performance_baseline_collector_egret.py 已 deprecated。\n"
        "  → 請改用 perf_runner.py：\n"
        "    python perf_runner.py --tier upgrade --adapter product-egret --trials N\n"
        "  本檔保留 backward compat 維持舊命令可用，但不再加新功能。\n",
        file=sys.stderr,
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=1, help="重複跑幾輪做一致性比對（預設 1）")
    parser.add_argument("--headless", action="store_true", help="無頭模式")
    parser.add_argument("--user", default=DEFAULT_USER, help=f"<PRODUCT> USER (default {DEFAULT_USER})")
    parser.add_argument("--pid", default=DEFAULT_PID, help=f"<PRODUCT> PID (default {DEFAULT_PID})")
    parser.add_argument("--out", help="輸出資料夾（預設 <repo>/react/report/performance/browser/performance_baseline_egret_<ts>）")
    args = parser.parse_args()

    if args.out:
        out_dir = Path(args.out)
    else:
        ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        out_dir = Path(__file__).resolve().parents[2] / "report" / "performance" / "browser" / f"performance_baseline_egret_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[info] 輸出: {out_dir}", flush=True)
    print(f"[info] 場景數: {len(EGRET_SCENARIOS)}, trials: {args.trials}", flush=True)
    print(f"[info] entry: {ENTRY_URL}, user: {args.user}, pid: {args.pid}", flush=True)

    all_trials = []
    with sync_playwright() as pw:
        for trial_idx in range(1, args.trials + 1):
            print(f"\n=== Trial {trial_idx}/{args.trials} ===", flush=True)
            trial_dir = out_dir / f"trial_{trial_idx}"
            trial_results = run_trial(pw, args.headless, trial_dir, args.user, args.pid)
            all_trials.append(trial_results)

    summary = build_summary_egret(all_trials)
    summary_path = out_dir / "summary.json"
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print("\n=== Cross-trial Summary ===")
    for sname, info in summary.items():
        print(f"\n[{sname}] {info['labelZh']} ({info['type']})")
        for t in info["trials"]:
            cls = (t.get("cls") if info["type"] == "lobby_only"
                   else (t.get("lobby") or {}).get("cls"))
            cls_str = f"{cls:.4f}" if isinstance(cls, (int, float)) else "N/A"
            if info["type"] == "lobby_only":
                print(
                    f"  trial {t['trial']}: LCP={t.get('lcp')} CLS={cls_str} "
                    f"TBT={t.get('totalBlockingMs')} DOM={t.get('domNodes')} "
                    f"err={t.get('consoleErrors')} bad={t.get('badResponses')} "
                    f"login={t.get('loginWallClockMs')}ms ready={t.get('lobbyReadyMs')}ms"
                )
            else:
                lobby = t.get("lobby") or {}
                timing = t.get("timing") or {}
                delta = t.get("deltaRoomVsLobby") or {}
                print(
                    f"  trial {t['trial']}: vid={t.get('usedVid')} lobby LCP={lobby.get('lcp')} "
                    f"CLS={cls_str} TBT={lobby.get('totalBlockingMs')} | "
                    f"login={timing.get('loginWallClockMs')}ms room={timing.get('roomEnterMs')}ms | "
                    f"Δ longTasks +{delta.get('longTasksCountDelta')} "
                    f"TBT +{delta.get('totalBlockingMsDelta')}ms"
                )
                if t.get("error"):
                    print(f"     ⚠️ {t['error']}")

    print(f"\n[done] summary: {summary_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
