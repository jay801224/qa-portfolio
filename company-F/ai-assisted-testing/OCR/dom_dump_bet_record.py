"""
dom_dump_bet_record.py — 一次性 DOM 探測腳本
目的: 進 QA N011，下注一局後 dump 投注記錄面板的 DOM 結構，
      找出正確的 selector（取代失效的 betRecordRowCard）。

用法:
  python dom_dump_bet_record.py
  python dom_dump_bet_record.py --vid N011 --env qa
"""

import argparse
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
PROJECT_ROOT = HERE.parent.parent
REACT_PYTHON = PROJECT_ROOT / "react" / "python"
SHARED_DIR = HERE.parent

sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REACT_PYTHON))
sys.path.insert(0, str(SHARED_DIR))

from bac_card_verify import (
    get_login_url, enter_game_room, _get_countdown, _is_dealing, _is_betting,
    SCREENSHOT_DIR,
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import bac_card_verify
bac_card_verify._current_game = "bac"

# ── DOM dump JS ─────────────────────────────────────────────────────────────

DUMP_RIGHT_PANEL_JS = """() => {
    var results = [];
    var allEls = document.querySelectorAll('*');
    var seen = new Set();
    for (var el of allEls) {
        var cls = (el.className || '').toString();
        if (!cls || seen.has(cls)) continue;
        if (/record|Record|bet|Bet|accordion|Accordion|expander|row|Row|card|Card|detail|Detail|history|History|tab|Tab/i.test(cls)) {
            seen.add(cls);
            var rect = el.getBoundingClientRect();
            if (rect.width > 0 && rect.height > 0) {
                results.push({
                    tag: el.tagName.toLowerCase(),
                    className: cls.substring(0, 200),
                    text: (el.textContent || '').substring(0, 100).trim(),
                    rect: {x: Math.round(rect.x), y: Math.round(rect.y), w: Math.round(rect.width), h: Math.round(rect.height)},
                    childCount: el.children.length,
                    clickable: el.tagName === 'BUTTON' || el.tagName === 'A' || el.onclick !== null || el.getAttribute('role') === 'button'
                });
            }
        }
    }
    return results;
}"""

DUMP_PANEL_TREE_JS = """(panelSelector) => {
    var panel = document.querySelector(panelSelector);
    if (!panel) return null;
    function dumpNode(node, depth) {
        if (depth > 3 || !node || node.nodeType !== 1) return null;
        var cls = (node.className || '').toString();
        var text = '';
        for (var child of node.childNodes) {
            if (child.nodeType === 3) text += child.textContent.trim();
        }
        var children = [];
        for (var ch of node.children) {
            var d = dumpNode(ch, depth + 1);
            if (d) children.push(d);
        }
        return { tag: node.tagName.toLowerCase(), cls: cls.substring(0, 150), text: text.substring(0, 80), children: children };
    }
    return dumpNode(panel, 0);
}"""

FIND_TAB_BUTTONS_JS = """() => {
    var tabs = [];
    var btns = document.querySelectorAll('button, [role="tab"], [role="button"]');
    for (var btn of btns) {
        var text = (btn.textContent || '').trim();
        var cls = (btn.className || '').toString();
        var rect = btn.getBoundingClientRect();
        if (rect.width > 0 && rect.height > 0 && text.length < 30) {
            tabs.push({
                tag: btn.tagName.toLowerCase(), text: text,
                cls: cls.substring(0, 150),
                rect: {x: Math.round(rect.x), y: Math.round(rect.y), w: Math.round(rect.width), h: Math.round(rect.height)},
                visible: rect.x > 0 && rect.y > 0
            });
        }
    }
    return tabs;
}"""


def _login_and_enter(page, ctx, env, pid, currency, vid):
    """重用 bac_4source_verify 的登入+進房邏輯（含 TSS 重試）。"""
    for attempt in range(1, 4):
        # 每次重試都重新取 URL（確保 TSS 新鮮）
        url = None
        try:
            from api_login import get_game_url as api_get
            url = api_get(env, pid, currency)
            if url:
                print(f"  [Login] API login 成功 (attempt {attempt})")
        except Exception:
            pass
        if not url:
            url = get_login_url(env, pid, currency)
        if not url:
            print(f"  [Login] 無法取得 URL")
            continue

        print(f"  嘗試 {attempt}/3...")
        page.goto(url, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)

        # 處理 QA Entry 版本選擇頁（複用 bac_4source_verify 相同邏輯）
        for _ in range(3):
            page.wait_for_timeout(2000)
            body = page.evaluate("()=>(document.body.innerText||'').substring(0,800)")
            if "Deployed Version" in body or "qa_entries" in body:
                print(f"  版本選擇頁，點擊 qa_entries...")
                try:
                    page.locator("a", has_text="qa_entries").first.click(timeout=5000)
                    page.wait_for_timeout(5000)
                    continue
                except Exception:
                    pass
            if "Go to Latest Entry" in body:
                print(f"  點擊 Go to Latest Entry...")
                try:
                    page.get_by_text("Go to Latest Entry", exact=False).first.click(timeout=5000)
                except Exception:
                    pass
                print(f"  等待遊戲載入...", end="", flush=True)
                for w in range(30):
                    page.wait_for_timeout(2000)
                    lobby_count = page.locator('[class*="LobbyItemMenu"]').count()
                    if lobby_count > 0:
                        print(f" OK ({(w+1)*2}s)")
                        break
                    pct = page.evaluate("()=>{var b=document.body.innerText||'';var m=b.match(/(\\d+)%/);return m?m[1]:''}")
                    if pct:
                        print(f" {pct}%", end="", flush=True)
                else:
                    print(f" TIMEOUT")
            break

        result, page, entry_version = enter_game_room(
            page, ctx, category="百家樂", target_room=vid)
        if result == "expired":
            print(f"  TSS 過期，重試...")
            continue
        elif result:
            print(f"[Setup] 進房成功: {vid}")
            return page, True
        else:
            print(f"  進房失敗")
            continue

    return page, False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--vid", default="N011")
    parser.add_argument("--env", default="qa")
    parser.add_argument("--pid", default="<ACCOUNT>")
    parser.add_argument("--currency", default="cny")
    args = parser.parse_args()

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = PROJECT_ROOT / "react" / "report"
    out_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = ctx.new_page()

        # ── 登入 + 進房 ──
        print(f"\n[Setup] 登入遊戲室...")
        page, ok = _login_and_enter(page, ctx, args.env, args.pid, args.currency, args.vid)
        if not ok:
            print(f"[ERROR] 3 次重試均失敗")
            browser.close()
            return

        # ── 等倒數 + 下注 ──
        print(f"\n[Phase 1] 等待投注階段...", end="", flush=True)
        for _ in range(60):
            cur = _get_countdown(page)
            if _is_betting(cur):
                print(f" OK (倒數 {cur}s)")
                break
            page.wait_for_timeout(1000)
        else:
            print(f" TIMEOUT")

        print(f"[Phase 1] 下注莊...", end="", flush=True)
        try:
            from steps.game.betting import place_bet, confirm_bet, select_chip_for_min_bet, detect_bet_mode, get_min_bet
            from react_client_autobet import click_x2
            min_bet = get_min_bet(args.vid, "莊") or 20
            select_chip_for_min_bet(page, min_bet)
            page.wait_for_timeout(500)
            place_bet(page, "莊")
            page.wait_for_timeout(500)
            mode = detect_bet_mode(page)
            if mode == "confirm":
                confirm_bet(page)
            else:
                click_x2(page)
            print(f" OK")
        except Exception as e:
            print(f" FAIL ({e})")

        # ── 等結算 ──
        print(f"[Phase 2] 等待結算...", end="", flush=True)
        for _ in range(90):
            cur = _get_countdown(page)
            if _is_dealing(cur):
                break
            page.wait_for_timeout(500)
        for _ in range(60):
            cur = _get_countdown(page)
            if _is_betting(cur):
                print(f" OK (新局倒數 {cur}s)")
                break
            page.wait_for_timeout(1000)
        else:
            print(f" OK (靜默結算)")

        print(f"[Phase 2] 等 5s 讓記錄 API 更新...")
        page.wait_for_timeout(5000)

        # ── Phase 3: DOM 探測 ──
        print(f"\n{'='*60}")
        print(f"  DOM 探測開始")
        print(f"{'='*60}")

        ss1 = str(out_dir / f"dom_dump_game_{ts}.png")
        page.screenshot(path=ss1)
        print(f"  截圖: {ss1}")

        # 找所有 tab 按鈕
        print(f"\n[Scan 1] 所有可見 tab/button:")
        tabs = page.evaluate(FIND_TAB_BUTTONS_JS)
        for t in tabs:
            if t["visible"]:
                print(f"  <{t['tag']}> text=\"{t['text']}\" cls={t['cls'][:80]} pos=({t['rect']['x']},{t['rect']['y']})")

        # 點「投注記錄」tab
        print(f"\n[Action] 嘗試點擊投注記錄 tab...")
        record_clicked = False
        record_btn = page.get_by_role("button", name="投注記錄")
        if record_btn.count() > 0 and record_btn.first.is_visible():
            record_btn.first.click(timeout=5000)
            record_clicked = True
            print(f"  方法 1 成功: get_by_role('button', name='投注記錄')")

        if not record_clicked:
            kws = ['投注記錄', '投注紀錄', 'Bet Record', '歷史記錄', '歷史紀錄']
            all_btns = page.locator("button")
            for i in range(all_btns.count()):
                btn = all_btns.nth(i)
                try:
                    text = (btn.text_content() or "").strip()
                    if any(k in text for k in kws) and btn.is_visible():
                        btn.click(timeout=3000, force=True)
                        record_clicked = True
                        print(f"  方法 2 成功: button text=\"{text}\"")
                        break
                except Exception:
                    continue

        if not record_clicked:
            menu_btns = page.locator('[class*="MenuButton"]')
            for i in range(menu_btns.count()):
                btn = menu_btns.nth(i)
                try:
                    text = (btn.text_content() or "").strip()
                    if ('紀錄' in text or '記錄' in text) and btn.is_visible():
                        btn.click(timeout=3000, force=True)
                        record_clicked = True
                        print(f"  方法 3 成功: MenuButton text=\"{text}\"")
                        break
                except Exception:
                    continue

        if not record_clicked:
            print(f"  ⚠ 所有方法都失敗")

        page.wait_for_timeout(3000)

        ss2 = str(out_dir / f"dom_dump_record_panel_{ts}.png")
        page.screenshot(path=ss2)
        print(f"  截圖: {ss2}")

        # Dump 記錄面板 DOM
        print(f"\n[Scan 2] 記錄相關 DOM 元素:")
        record_els = page.evaluate(DUMP_RIGHT_PANEL_JS)
        for el in record_els:
            marker = " ★" if el.get("clickable") else ""
            print(f"  <{el['tag']}> cls=\"{el['className'][:100]}\" "
                  f"text=\"{el['text'][:50]}\" "
                  f"rect=({el['rect']['x']},{el['rect']['y']},{el['rect']['w']},{el['rect']['h']}) "
                  f"children={el['childCount']}{marker}")

        # 嘗試點 expander
        print(f"\n[Action] 嘗試展開 expander...")
        try:
            exp = page.locator('[class*="expander"]')
            if exp.count() > 0:
                exp.first.click(timeout=5000, force=True)
                print(f"  expander 點擊成功 (count={exp.count()})")
                page.wait_for_timeout(2000)
            else:
                print(f"  沒有 expander 元素")
        except Exception as e:
            print(f"  expander 失敗: {e}")

        # 再次 dump（展開後）
        print(f"\n[Scan 3] 展開後的 DOM:")
        record_els2 = page.evaluate(DUMP_RIGHT_PANEL_JS)
        for el in record_els2:
            marker = " ★" if el.get("clickable") else ""
            print(f"  <{el['tag']}> cls=\"{el['className'][:100]}\" "
                  f"text=\"{el['text'][:50]}\" "
                  f"rect=({el['rect']['x']},{el['rect']['y']},{el['rect']['w']},{el['rect']['h']}) "
                  f"children={el['childCount']}{marker}")

        # 嘗試各種記錄行 selector
        print(f"\n[Scan 4] 嘗試各種記錄行 selector:")
        candidate_selectors = [
            '[class*="betRecordRowCard"]',
            '[class*="RecordRow"]', '[class*="recordRow"]',
            '[class*="betRow"]', '[class*="BetRow"]',
            '[class*="record_row"]', '[class*="record-row"]',
            '[class*="recordCard"]', '[class*="RecordCard"]', '[class*="record_card"]',
            '[class*="betRecord"]', '[class*="BetRecord"]',
            '[class*="historyRow"]', '[class*="HistoryRow"]',
            '[class*="bet_item"]', '[class*="BetItem"]', '[class*="betItem"]',
            '[class*="game_record"]', '[class*="GameRecord"]', '[class*="gameRecord"]',
            '[class*="Accordion"]',
        ]
        for sel in candidate_selectors:
            count = page.locator(sel).count()
            if count > 0:
                first_cls = page.locator(sel).first.evaluate("el => el.className.toString().substring(0, 150)")
                first_text = page.locator(sel).first.evaluate("el => (el.textContent||'').substring(0, 80)")
                print(f"  ✓ {sel} → count={count}, cls=\"{first_cls}\", text=\"{first_text}\"")
            else:
                print(f"  ✗ {sel} → 0")

        # 面板容器搜尋
        print(f"\n[Scan 5] 面板容器搜尋:")
        panel_candidates = [
            '[class*="RecordPage"]', '[class*="BetRecord"]',
            '[class*="GameRecord"]', '[class*="record_page"]',
            '[class*="record_list"]', '[class*="RecordList"]',
            '[class*="history"]', '[class*="History"]',
            '[class*="rightPanel"]', '[class*="RightPanel"]',
            '[class*="side_panel"]', '[class*="SidePanel"]',
        ]
        for sel in panel_candidates:
            count = page.locator(sel).count()
            if count > 0:
                print(f"  ✓ {sel} → count={count}")
                tree = page.evaluate(DUMP_PANEL_TREE_JS, sel)
                if tree:
                    print(f"    Root: <{tree['tag']}> cls=\"{tree['cls'][:80]}\"")
                    for ch in tree.get("children", [])[:10]:
                        print(f"      <{ch['tag']}> cls=\"{ch['cls'][:80]}\" text=\"{ch['text'][:40]}\"")
                        for ch2 in ch.get("children", [])[:5]:
                            print(f"        <{ch2['tag']}> cls=\"{ch2['cls'][:80]}\" text=\"{ch2['text'][:40]}\"")
            else:
                print(f"  ✗ {sel} → 0")

        ss3 = str(out_dir / f"dom_dump_expanded_{ts}.png")
        page.screenshot(path=ss3)
        print(f"\n  截圖: {ss3}")

        # 保存完整結果到 JSON
        dump_result = {
            "timestamp": ts, "vid": args.vid, "env": args.env,
            "tabs": tabs,
            "record_elements_before_expand": record_els,
            "record_elements_after_expand": record_els2,
        }
        json_path = str(out_dir / f"dom_dump_{ts}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(dump_result, f, ensure_ascii=False, indent=2)
        print(f"  JSON: {json_path}")

        print(f"\n{'='*60}")
        print(f"  DOM 探測完成")
        print(f"{'='*60}")

        print(f"\n  瀏覽器保持開啟 30 秒，可手動觀察...")
        page.wait_for_timeout(30000)
        browser.close()


if __name__ == "__main__":
    main()
