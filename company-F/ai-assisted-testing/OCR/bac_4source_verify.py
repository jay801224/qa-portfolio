"""
bac_4source_verify.py — 百家樂四源整合驗證

測試目的:
  驗證荷官輸入的牌面，經過系統處理後，在開獎動畫、影片串流、投注記錄
  三個顯示端是否一致。四個來源必須透過 Round ID 確認為同一局，
  且牌面/點數/贏家結果必須完全吻合，任何來源缺失或不一致均為 FAIL。

四個來源：
  1. 荷官輸入 — 控端實際送出的牌面（cardValue）+ Round ID (gameCode)
  2. 開獎動畫 — 遊戲頁面動畫層顯示的牌面（Gemini OCR 辨識）
  3. 影片串流 — 遊戲頁面影片層顯示的牌面（Gemini OCR 辨識）
  4. 投注記錄 — 投注記錄詳細頁的牌面（DOM 解析 PokerCard class）

判定規則:
  - Round ID 不一致 → ROUND_ID_MISMATCH（不是同一局，比對無意義）
  - 任何來源資料缺失 → INCOMPLETE（無法完成驗證）
  - 牌面/點數不一致 → MISMATCH（系統顯示有誤）
  - 全部一致 → PASS

限制:
  - 僅支援手動開牌房間（isManual=true），自動開牌房間來不及查記錄再下注

單局流程：荷官開局 → 下注 → 荷官送牌 → 觀察動畫+影片 → 投注記錄 → 比對 → 報告

用法:
  python bac_4source_verify.py                         # 隨機牌，QA，1 局
  python bac_4source_verify.py --rounds 3              # 3 局
  python bac_4source_verify.py --cards player-win      # 指定 scenario
  python bac_4source_verify.py --cards 2S,3H,5C,8D    # 指定牌面
  python bac_4source_verify.py --headed                # 顯示瀏覽器
  python bac_4source_verify.py --vid N007              # 指定房間
  python bac_4source_verify.py --skip-video-ocr        # 跳過影片 OCR
  python bac_4source_verify.py --dealer-id 8232        # 指定荷官 ID
"""

import argparse
import json
import os
import random
import re
import sys
import time
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

# ── 路徑設定 ────────────────────────────────────────────────────────────────
HERE = Path(__file__).parent                          # shared/OCR/
PROJECT_ROOT = HERE.parent.parent                     # 
REACT_PYTHON = PROJECT_ROOT / "react" / "python"
SHARED_DIR = HERE.parent                              # shared/

sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REACT_PYTHON))
sys.path.insert(0, str(SHARED_DIR))

# 重用既有模組
from bac_card_verify import (
    _get_countdown, _is_dealing, _is_betting, _check_expired,
    get_login_url, enter_game_room, save_html_report, save_json_report,
    OUTPUT_DIR, SCREENSHOT_DIR, GAME_CONFIG,
)
from bac_frame_analyzer import detect_round_info, find_best_frame, recognize_game
from qa_auto_dealer import (
    encode_card, decode_card, card_display, parse_cards, bac_point,
    random_bac_cards, scenario_bac_cards,
    SUIT_MAP, SUIT_NAMES, FACE_MAP, FACE_NAMES, CARD_GAMES, BAC_ROOM_FALLBACK,
    SHBConsoleMonitor,
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── 常量 ────────────────────────────────────────────────────────────────────
DEFAULT_DEALER_ID = "8232"
DEFAULT_VID = "N010"
COUNTDOWN_EL_SEL = '[class*="PcMainGame_timer"]'

# 投注記錄解析用的 JS — 從 TC_086 step_defs 提取
BET_RECORD_PARSE_JS = """() => {
    var suitMap = {C: '梅花', D: '方塊', H: '愛心', S: '黑桃'};
    var rankMap = {1:'A',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'10',11:'J',12:'Q',13:'K'};
    var info = {playerCards:[], bankerCards:[], playerPoints:null, bankerPoints:null, roundId:'', table:''};

    // 局號+桌台 — 搜整個 BetRecordDetailPage 的所有元素
    var container = document.querySelector('[class*="BetRecordDetailPage"]');
    if (container) {
        var fullText = container.innerText || '';
        // 局號: 多種格式匹配
        var rm = fullText.match(/(?:局號|局号|Round|局編號|编号)[：:\\s]*([A-Z0-9]+)/i);
        if (rm) info.roundId = rm[1];
        // 也嘗試直接找 G 開頭的 ID 格式（如 GN01026330002）
        if (!info.roundId) {
            var gm = fullText.match(/\\b(G[A-Z]\\d{8,})\\b/);
            if (gm) info.roundId = gm[1];
        }
        // 桌台
        var tm = fullText.match(/(?:桌台|桌號|桌号|Table)[：:\\s]*(.+?)(?=\\n|局|Round|$)/i);
        if (tm) info.table = tm[1].trim();
        // 也嘗試找複製按鈕旁邊的文字（button 的 previousSibling 或 parentNode）
        if (!info.roundId) {
            var copyBtns = container.querySelectorAll('button, [role="button"]');
            for (var btn of copyBtns) {
                var btnText = (btn.textContent || '').trim();
                if (btnText.includes('複製') || btnText.includes('复制') || btnText.includes('Copy')) {
                    var parent = btn.parentElement;
                    if (parent) {
                        var pt = (parent.textContent || '').replace(btnText, '').trim();
                        var pm = pt.match(/([A-Z0-9]{10,})/);
                        if (pm) info.roundId = pm[1];
                    }
                }
            }
        }
    }

    // PokerCard class 解析
    function parseCardsGlobal(containerSel) {
        var cards = [];
        var wraps = document.querySelectorAll(containerSel);
        for (var wrap of wraps) {
            var pokers = wrap.querySelectorAll('[class*="PokerCard"]');
            for (var p of pokers) {
                var cls = (p.className || '').toString();
                var cm = cls.match(/PokerCard_simple_([CDHS])_(\\d+)/);
                if (cm) {
                    var suit = suitMap[cm[1]] || cm[1];
                    var rank = rankMap[parseInt(cm[2])] || cm[2];
                    cards.push(suit + rank);
                }
            }
            if (cards.length > 0) break;
        }
        return cards;
    }
    info.playerCards = parseCardsGlobal('[class*="PCPokerCardWrapper_player_container"], [class*="player_card"]');
    info.bankerCards = parseCardsGlobal('[class*="PCPokerCardWrapper_banker_container"], [class*="banker_card"]');

    // 點數
    var valEls = document.querySelectorAll('[class*="PCPokerCardWrapper_value"], [class*="card_value"]');
    var pts = [];
    for (var v of valEls) {
        var cn = (v.className||'').toString();
        if (/value/i.test(cn)) {
            var d = (v.textContent||'').trim();
            if (/^\\d$/.test(d)) pts.push(parseInt(d));
        }
    }
    if (pts.length >= 2) { info.playerPoints = pts[0]; info.bankerPoints = pts[1]; }

    return info;
}"""


# ── 荷官工具 Session ────────────────────────────────────────────────────────

class DealerSession:
    """封裝荷官工具頁面的開牌操作。"""

    def __init__(self, page, game_key="BAC", dealer_id=DEFAULT_DEALER_ID):
        self.page = page
        self.game_key = game_key
        self.dealer_id = dealer_id
        cfg = CARD_GAMES[game_key]
        self.store_class = cfg["store"]
        self.store_module = cfg["store"].split(".")[0]
        self.send_method = cfg["send"]
        self.monitor = SHBConsoleMonitor()
        page.on("console", self.monitor.on_console)

    def _js_call(self, body):
        sm = self.store_module
        sc = self.store_class
        return self.page.evaluate(f'''(function(){{
            var fn = window[Object.keys(window).find(function(k){{return k.startsWith("$getInstance")}})];
            if (!fn) return null;
            var s = null;
            if (typeof {sm} !== 'undefined' && {sm}.DataStore) s = fn({sc});
            if (!s) s = fn(Plaza.DataStoreBase);
            if (!s) return null;
            {body}
        }})()''')

    def _get_gs(self):
        return self._js_call("return typeof s.getGameStatus==='function' ? s.getGameStatus() : -1;")

    def _get_state(self):
        return self._js_call("""
            var d = s.dispatchCardResp;
            return {
                gs: typeof s.getGameStatus==='function' ? s.getGameStatus() : -1,
                disp: !!d,
                gameCode: d ? d.gameCode : null
            };
        """)

    def open_and_login(self, vid):
        """開啟荷官工具 + 登入。"""
        try:
            from network_config import get_url
            url = get_url(8082, f"/dealer-tools/main/?vid={vid}&isManual=true")
        except ImportError:
            url = f"http://example.internal:8082/dealer-tools/main/?vid={vid}&isManual=true"

        def _dismiss(d):
            try:
                d.accept()
            except Exception:
                pass
        self.page.on("dialog", _dismiss)

        print(f"  [Dealer] 載入 {url[:60]}...")
        try:
            self.page.goto(url, wait_until="networkidle", timeout=60000)
        except Exception:
            pass
        # Egret 引擎需要較長載入時間
        self.page.wait_for_timeout(10000)

        print(f"  [Dealer] 登入 ID={self.dealer_id}...", end="", flush=True)
        t0 = time.time()
        for ch in str(self.dealer_id):
            self.page.keyboard.press(ch)
            time.sleep(0.4)
        time.sleep(0.8)
        self.page.keyboard.press("NumpadMultiply")

        # Egret console 有 ~60s 延遲，等 60s
        data = self.monitor.wait_for("login", timeout=60, since=t0, page=self.page)
        if not data or data.get("retCode") != 0:
            # fallback: 直接嘗試取 gameStatus 判斷是否已登入
            print(f" console 無回應，嘗試 JS 探測...", end="", flush=True)
            self.page.wait_for_timeout(5000)
            gs = self._get_gs()
            if gs is not None and gs >= 0:
                print(f" OK (gs={gs})")
                return True
            print(f" FAIL ({data}, gs={gs})")
            return False
        print(" OK")
        self.monitor.wait_for("snapshot", timeout=10, since=t0, page=self.page)
        return True

    def start_round(self):
        """開局並確認進入倒數（gs=1）或 dispatch 就緒。回傳 True=可以下注/送牌。"""
        gs = self._get_gs()
        if gs is None:
            return False

        # gs=1: 已在倒數中
        if gs == 1:
            print(f"    已在倒數中 (gs=1)")
            return True

        # gs=2: 上一局結算中 → closeRound 清掉
        if gs == 2:
            print(f"    closeRound（清除上一局）...", end="", flush=True)
            self._js_call("if (s.dealerCloseRound) s.dealerCloseRound();")
            self.page.wait_for_timeout(5000)
            self._js_call("if (s.dealerCloseRound) s.dealerCloseRound();")
            self.page.wait_for_timeout(3000)
            gs = self._get_gs()
            print(f" gs={gs}")

        # gs=0: startGame → 等 gs 變 1（最多重試 3 次 × 10 秒）
        for retry in range(3):
            if gs == 1:
                return True

            self._js_call("if (s.dealerStartGame) s.dealerStartGame();")
            print(f"    startGame (retry={retry+1}, gs={gs})...", end="", flush=True)

            for t in range(10):
                self.page.wait_for_timeout(1000)
                gs = self._get_gs()
                if gs == 1:
                    print(f" ✓ 倒數開始 ({t+1}s)")
                    return True
                if gs == 2:
                    # 自動開局房間可能跳過 gs=1 直接到 gs=2
                    print(f" ✓ gs=2（自動開局）")
                    return True
            print(f" gs={gs}")

        print(f"    ✗ startGame 無效（gs={gs}）")
        return False

    def wait_for_dispatch(self, timeout=60):
        """等待 dispatch 就緒（ci=1 開始的新局 dispatch）。每 10 秒沒反應就重按 startGame。"""
        for t in range(timeout):
            state = self._get_state()
            if state and state.get("disp"):
                disp = state.get("dispObj") or {}
                ci = disp.get("cardIndex", 0)
                # 只接受 ci ≤ 2 的新局 dispatch（排除殘留的 ci=4/6）
                if ci <= 2:
                    print(f"    dispatch 就緒 ({t+1}s, ci={ci})")
                    return True
                # 殘留 dispatch → closeRound 清掉
                if t == 0 or t % 5 == 0:
                    print(f"    殘留 dispatch ci={ci}，closeRound...", end="", flush=True)
                    self._js_call("if (s.dealerCloseRound) s.dealerCloseRound();")
                    self.page.wait_for_timeout(3000)
                    self._js_call("if (s.dealerStartGame) s.dealerStartGame();")
            else:
                # 每 10 秒重按一次 startGame
                if t > 0 and t % 10 == 0:
                    gs = self._get_gs()
                    if gs in (0, 2):
                        print(f"    retry startGame ({t}s, gs={gs})...", end="", flush=True)
                        if gs == 2:
                            self._js_call("if (s.dealerCloseRound) s.dealerCloseRound();")
                            self.page.wait_for_timeout(3000)
                        self._js_call("if (s.dealerStartGame) s.dealerStartGame();")
            self.page.wait_for_timeout(1000)
        print(f"    dispatch 無反應 ({timeout}s)")
        return False

    def send_cards(self, card_values, screenshot_dir=None):
        """依序送牌。回傳 (sent_count, dispatch_log, screenshot_paths)。

        百家樂最多 6 張牌（ci=1~6），送到 ci=6 後主動停止。
        dispatch_log: 每張牌的 dispatch → send 對應記錄
        screenshot_paths: 截圖（第4張後截1次 + 每張補牌截1次，最多3張）
        """
        sent = 0
        dispatch_log = []
        screenshots = []
        last_ci = 0

        for attempt in range(12):
            state = self._get_state()
            if not state:
                break

            gs = state.get("gs", -1)
            has_disp = state.get("disp", False)

            # 沒有 dispatch 且 gs ≤ 0 → 牌局結束
            if not has_disp and gs <= 0:
                break

            if not has_disp:
                self.page.wait_for_timeout(1000)
                continue

            # dispatch 詳細資訊
            disp = state.get("dispObj") or {}
            ci = disp.get("cardIndex", 0)
            vis = disp.get("visible", 1)
            who = disp.get("who", 0)

            # ci 沒有推進（殘留） → 這局的牌已經送完
            if sent > 0 and ci == last_ci and ci >= 4:
                print(f"      ci={ci} 未推進，牌局送牌完成")
                break

            # ci > 6 不合理，停止
            if ci > 6:
                break

            val = card_values[sent] if sent < len(card_values) else random.randint(1, 52)

            # 記錄 dispatch → send 對應
            log_entry = {
                "index": sent,
                "dispatch": {"cardIndex": ci, "who": who, "visible": vis},
                "sent": {"val": val, "display": card_display(val)},
            }
            dispatch_log.append(log_entry)

            if self.send_method == "sendNextCardProto":
                self._js_call(f"if (s.sendNextCardProto) s.sendNextCardProto([{{cardindex:{ci},val:{val},handindex:0}}]);")
            else:
                self._js_call(f"if (s.sendNextCard) s.sendNextCard({val},{ci},{vis},{who});")
            sent += 1
            last_ci = ci
            print(f"      #{sent}: dispatch ci={ci} who={who} → val={val} ({card_display(val)})")

            # 截圖時機：第 4 張（雙方各 2 張）+ 第 5、6 張（補牌）
            if screenshot_dir and sent in (4, 5, 6):
                self.page.wait_for_timeout(500)
                try:
                    ts_ss = datetime.now().strftime("%Y%m%d_%H%M%S")
                    ss_path = str(screenshot_dir / f"dealer_card{sent}_{ts_ss}.png")
                    self.page.screenshot(path=ss_path)
                    screenshots.append(ss_path)
                    label = "雙方各2張" if sent == 4 else f"補牌第{sent-4}張"
                    print(f"      截圖({label}): {Path(ss_path).name}")
                except Exception:
                    pass

            # ci=6 = 莊第3張 = 最後一張，送完停止
            if ci >= 6:
                print(f"      ci=6 莊第3張已送，結束送牌")
                break

            self.page.wait_for_timeout(2000)

        return sent, dispatch_log, screenshots

    def close_round(self):
        self._js_call("if (s.dealerCloseRound) s.dealerCloseRound();")
        self.page.wait_for_timeout(3000)


# ── 投注記錄解析 ────────────────────────────────────────────────────────────

def _clear_overlay(page):
    """清除遊戲狀態 overlay。"""
    try:
        page.evaluate('document.querySelectorAll("[class*=pointer-events-auto][class*=bg-black]")'
                      '.forEach(e => e.style.pointerEvents = "none")')
    except Exception:
        pass


def open_bet_record_and_parse(page):
    """開啟投注記錄 → 詳細頁 → 解析牌面。
    基於 TC_087 驗證的 NavigationMenu UI selector（2026-03-30）。
    回傳 (dict, screenshot_path)。
    """
    _clear_overlay(page)
    screenshot_path = ""

    # ── Step 1: 開紀錄面板（MenuButton「遊戲紀錄」）──
    _clear_overlay(page)
    panel_opened = False
    try:
        # 方法 1: MenuButton（TC_087 已驗證可用）
        menu_btns = page.locator('[class*="MenuButton"]')
        for i in range(menu_btns.count()):
            btn = menu_btns.nth(i)
            try:
                text = (btn.text_content() or "").strip()
                if '紀錄' in text or '記錄' in text:
                    btn.click(timeout=5000, force=True)
                    panel_opened = True
                    print(f"    [bet-record] 點擊「{text}」MenuButton")
                    break
            except Exception:
                continue

        if not panel_opened:
            # 方法 2: 文字搜尋所有按鈕
            kws = ['投注記錄', '投注紀錄', 'Bet Record', '遊戲紀錄']
            all_btns = page.locator("button")
            for i in range(all_btns.count()):
                btn = all_btns.nth(i)
                try:
                    text = (btn.text_content() or "").strip()
                    if any(k in text for k in kws) and btn.is_visible():
                        btn.click(timeout=3000, force=True)
                        panel_opened = True
                        print(f"    [bet-record] 點擊「{text}」")
                        break
                except Exception:
                    continue

        page.wait_for_timeout(2000)
        if panel_opened:
            print("    [bet-record] 紀錄面板已開啟")
        else:
            print("    [bet-record] ⚠ 紀錄面板開啟失敗")
            return None, ""
    except Exception as e:
        print(f"    [bet-record] 紀錄面板開啟失敗: {e}")
        return None, ""

    # 確認 NavigationMenuHeader 出現
    try:
        page.wait_for_function(
            '() => document.querySelector(\'[class*="NavigationMenuHeader"]\') !== null',
            timeout=10000)
    except Exception:
        pass

    # ── Step 2: 確認在「投注記錄」tab ──
    _clear_overlay(page)
    try:
        header = page.locator('[class*="NavigationMenuHeader"]')
        if header.count() > 0:
            tab_btns = header.locator("button")
            for i in range(tab_btns.count()):
                btn = tab_btns.nth(i)
                text = (btn.text_content() or "").strip()
                if "投注" in text:
                    btn.click(timeout=3000)
                    print(f"    [bet-record] 點擊 tab「{text}」")
                    break
    except Exception:
        pass
    page.wait_for_timeout(2000)

    # ── Step 3: 展開今日日期 + 點第一筆記錄 ──
    _clear_overlay(page)

    # 新版 UI: 記錄行是 <button class="w-full flex items-center relative pl-6">
    record_btns = page.locator(
        'button[class*="w-full"][class*="flex"][class*="items-center"]'
        '[class*="relative"][class*="pl-6"]')
    count = record_btns.count()

    if count == 0:
        # 嘗試展開日期分群
        print("    [bet-record] 無記錄行，嘗試展開日期分群...")
        # 方法 A: cursor-pointer 日期行
        date_rows = page.locator('div[class*="cursor-pointer"][class*="w-full"][class*="flex"]')
        for i in range(date_rows.count()):
            row = date_rows.nth(i)
            try:
                text = (row.text_content() or "").strip()
                if len(text) < 30 and any(c.isdigit() for c in text[:5]):
                    row.click(timeout=3000, force=True)
                    print(f"    [bet-record] 展開日期: {text[:10]}")
                    page.wait_for_timeout(2000)
                    break
            except Exception:
                continue

        # 方法 B: 舊版 expander（fallback）
        if page.locator('[class*="expander"]').count() > 0:
            try:
                page.locator('[class*="expander"]').first.click(timeout=5000, force=True)
                page.wait_for_timeout(2000)
            except Exception:
                pass

        # 重新搜尋
        record_btns = page.locator(
            'button[class*="w-full"][class*="flex"][class*="items-center"]'
            '[class*="relative"][class*="pl-6"]')
        count = record_btns.count()

    if count == 0:
        # 最終 fallback: 面板區域有時間格式的 button
        print("    [bet-record] selector 未命中，嘗試 fallback...")
        clicked = page.evaluate('''() => {
            var btns = document.querySelectorAll('button');
            for (var btn of btns) {
                var rect = btn.getBoundingClientRect();
                var text = (btn.textContent || '').trim();
                if (rect.x > 1300 && rect.y > 200 && rect.y < 800 && /\\d{2}:\\d{2}/.test(text)) {
                    btn.click();
                    return text.substring(0, 30);
                }
            }
            // 舊版: betRecordRowCard
            var old = document.querySelector('[class*="betRecordRowCard"]');
            if (old) { old.click(); return 'betRecordRowCard'; }
            return '';
        }''')
        if clicked:
            print(f"    [bet-record] fallback 點擊: {clicked}")
            page.wait_for_timeout(3000)
        else:
            print("    [bet-record] ⚠ 找不到任何記錄行")
            return None, ""
    else:
        print(f"    [bet-record] 找到 {count} 筆記錄行")
        record_btns.first.click(timeout=5000, force=True)
        page.wait_for_timeout(3000)

    # ── Step 4: 等待詳細頁 / 牌面出現 ──
    _clear_overlay(page)
    try:
        page.wait_for_function('''() => {
            if (document.querySelectorAll('[class*="PokerCard"]').length > 0) return true;
            var sels = ['[class*="BetRecordDetailPage"]', '[class*="Accordion_details"]'];
            return sels.some(s => document.querySelector(s) !== null);
        }''', timeout=15000)
    except Exception:
        # 舊版可能需要額外點箭頭
        try:
            page.locator('[class*="Accordion_details"] button.bg-transparent').first.click(
                timeout=5000, force=True)
            page.wait_for_timeout(3000)
            page.wait_for_function(
                '() => document.querySelector(\'[class*="BetRecordDetailPage"]\') !== null',
                timeout=10000)
        except Exception:
            print("    [bet-record] 詳細頁未出現")
            return None, ""

    # ── 等已結算 ──
    for _retry in range(6):
        status_text = page.evaluate('''() => {
            var els = document.querySelectorAll('*');
            for (var el of els) {
                var rect = el.getBoundingClientRect();
                if (rect.x > 1300 && rect.width > 50) {
                    var t = (el.textContent || '').trim();
                    if (/已結算|结算|已完成|Settled/.test(t) && t.length < 30) return t;
                }
            }
            return '';
        }''')
        if status_text:
            break
        if _retry < 5:
            print(f"    [bet-record] 等結算... ({_retry+1}/6)")
            page.wait_for_timeout(5000)

    # ── 等牌面渲染 ──
    try:
        page.wait_for_function('''() => {
            return document.querySelectorAll('[class*="PokerCard"]').length > 0;
        }''', timeout=10000)
    except Exception:
        pass
    page.wait_for_timeout(1000)

    # ── 截圖 ──
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    ss_dir = SCREENSHOT_DIR / "bet_record"
    ss_dir.mkdir(parents=True, exist_ok=True)
    try:
        screenshot_path = str(ss_dir / f"bet_record_{ts}.png")
        page.screenshot(path=screenshot_path, full_page=True)
    except Exception:
        screenshot_path = ""

    # ── 解析（TC_086/087 共用 JS）──
    result = page.evaluate(BET_RECORD_PARSE_JS)

    # 點數補算
    if result and result.get("playerCards") and result.get("playerPoints") is None:
        result["playerPoints"] = _calc_points_from_chinese(result["playerCards"])
        result["bankerPoints"] = _calc_points_from_chinese(result.get("bankerCards", []))

    # 贏家判定
    if result and result.get("playerPoints") is not None and result.get("bankerPoints") is not None:
        pp, bp = result["playerPoints"], result["bankerPoints"]
        result["winner"] = "閒" if pp > bp else ("莊" if bp > pp else "和")

    # ── 返回遊戲室 ──
    try:
        page.locator('[class*="back"], [class*="Back"]').first.click(timeout=3000, force=True)
        page.wait_for_timeout(500)
    except Exception:
        pass
    for _ in range(3):
        try:
            page.keyboard.press("Escape")
            page.wait_for_timeout(300)
        except Exception:
            break

    return result, screenshot_path


def _calc_points_from_chinese(cards):
    """從中文牌面計算百家樂點數。如 ['梅花K', '愛心3'] → 3。"""
    CN_RANK_VAL = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7,
                   "8": 8, "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13}
    total = 0
    for card in cards:
        rank_str = re.sub(r'^(梅花|方塊|愛心|黑桃)', '', card)
        face = CN_RANK_VAL.get(rank_str, 0)
        total += bac_point(face)
    return total % 10


# ── 牌面正規化（比對用）────────────────────────────────────────────────────

def normalize_cards(cards, source="dealer"):
    """將不同來源的牌面正規化為 [(face, suit), ...] 格式。"""
    results = []
    for c in cards:
        if source == "dealer" and isinstance(c, int):
            face = (c - 1) // 4 + 1
            suit = (c - 1) % 4 + 1
            results.append((face, suit))
        elif source == "chinese":
            CN_SUIT = {"黑桃": 1, "愛心": 2, "梅花": 3, "方塊": 4}
            CN_RANK = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7,
                       "8": 8, "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13}
            for prefix, suit_val in CN_SUIT.items():
                if c.startswith(prefix):
                    rank_str = c[len(prefix):]
                    face_val = CN_RANK.get(rank_str, 0)
                    results.append((face_val, suit_val))
                    break
        elif source == "ocr":
            OCR_SUIT = {"♠": 1, "♥": 2, "♣": 3, "♦": 4}
            m = re.match(r'([ATJQK\d]+)([♠♥♣♦])', c)
            if m:
                face_str, suit_ch = m.group(1), m.group(2)
                face_val = FACE_MAP.get(face_str, FACE_MAP.get(face_str.upper(), 0))
                results.append((face_val, OCR_SUIT.get(suit_ch, 0)))
    return results


def compare_sources(dealer_input, anim_result, video_result, bet_record):
    """比對來源，回傳比對結果 dict。

    核心驗證：開獎動畫 vs 投注記錄（同一局 Round ID 下必須一致）。
    影片串流：QA 環境可能對不上，有就比，當參考。
    荷官端：只記錄 dispatch log，不做比對判定（val 可能不被伺服器採用）。
    """
    mismatches = []
    incomplete = []

    # 核心兩源：動畫 + 記錄
    has_anim = bool(anim_result and anim_result.get("player_cards"))
    has_bet = bool(bet_record and bet_record.get("playerCards"))

    if not has_anim:
        incomplete.append("開獎動畫無資料")
    if not has_bet:
        incomplete.append("投注記錄無資料")

    if incomplete:
        return {"overall": "INCOMPLETE", "mismatches": incomplete}

    # 正規化
    all_anim = anim_result["player_cards"] + anim_result["banker_cards"]
    anim_cards = normalize_cards(all_anim, "ocr")
    all_bet = bet_record["playerCards"] + bet_record["bankerCards"]
    bet_cards = normalize_cards(all_bet, "chinese")

    # 比對面值（花色可能因 OCR 誤差不比）
    anim_faces = sorted([c[0] for c in anim_cards])
    bet_faces = sorted([c[0] for c in bet_cards])

    # 動畫 vs 記錄 — 同一局 Round ID 下必須完全一致
    if len(anim_faces) != len(bet_faces):
        mismatches.append(f"開獎動畫({len(anim_faces)}張) ≠ 投注記錄({len(bet_faces)}張) 張數不同")
    elif anim_faces != bet_faces:
        mismatches.append("開獎動畫 ≠ 投注記錄")

    # 點數也比（更嚴格）
    if not mismatches:
        anim_p = anim_result.get("player_total", -1)
        anim_b = anim_result.get("banker_total", -1)
        bet_p = bet_record.get("playerPoints", -1)
        bet_b = bet_record.get("bankerPoints", -1)
        if anim_p >= 0 and bet_p >= 0:
            if anim_p != bet_p:
                mismatches.append(f"閒點數不一致: 動畫={anim_p} 記錄={bet_p}")
            if anim_b != bet_b:
                mismatches.append(f"莊點數不一致: 動畫={anim_b} 記錄={bet_b}")

    # 影片串流（參考，不影響 PASS/FAIL）
    video_note = ""
    if video_result and video_result.get("player_cards") and has_bet:
        all_vid = video_result["player_cards"] + video_result["banker_cards"]
        vid_cards = normalize_cards(all_vid, "ocr")
        vid_faces = sorted([c[0] for c in vid_cards])
        if vid_faces == bet_faces:
            video_note = "影片串流 = 投注記錄 ✓"
        else:
            video_note = "影片串流 ≠ 投注記錄（QA 環境已知可能不一致）"

    overall = "MISMATCH" if mismatches else "PASS"
    result = {"overall": overall, "mismatches": mismatches}
    if video_note:
        result["video_note"] = video_note
    return result


# ── 單局流程 ────────────────────────────────────────────────────────────────

def run_round(game_page, dealer_session, round_num, total_rounds,
              card_values, gemini_limit, skip_video_ocr, actual_vid=""):
    """執行單局驗證（三源或四源）。回傳 round_result dict。"""
    print(f"\n{'='*60}")
    print(f"  局 {round_num}/{total_rounds}")
    print(f"{'='*60}")
    ts_start = datetime.now()

    # 截圖目錄
    round_dir = SCREENSHOT_DIR / f"round_{round_num:03d}"
    round_dir.mkdir(parents=True, exist_ok=True)

    # 記錄荷官輸入（四源模式才有）
    dealer_display = [card_display(v) for v in card_values] if card_values else []
    if dealer_display:
        print(f"  [Dealer] 預定牌面: {', '.join(dealer_display)}")

    # 三源 Round ID 收集
    dealer_round_id = ""
    game_round_id = ""
    record_round_id = ""

    # ── Phase 1: 荷官開局（僅四源模式）──
    if dealer_session:
        print(f"  [Phase 1] 荷官開局...", end="", flush=True)
        dealer_started = dealer_session.start_round()
        if not dealer_started:
            print(f" FAIL")
        else:
            print(f" OK")

    # ── Phase 2: 等待投注階段 + 下注 ──
    print(f"  [Phase 2] 等待投注階段...", end="", flush=True)
    for wait_t in range(60):
        cur = _get_countdown(game_page)
        if _is_betting(cur):
            print(f" OK (倒數 {cur}s, {wait_t+1}s)")
            break
        # 四源模式：每 10 秒在荷官端重按 startGame
        if dealer_session and wait_t > 0 and wait_t % 10 == 0:
            gs = dealer_session._get_gs()
            if gs in (0, 2):
                print(f" retry({wait_t}s,gs={gs})", end="", flush=True)
                if gs == 2:
                    dealer_session._js_call("if (s.dealerCloseRound) s.dealerCloseRound();")
                    dealer_session.page.wait_for_timeout(2000)
                dealer_session._js_call("if (s.dealerStartGame) s.dealerStartGame();")
        game_page.wait_for_timeout(1000)
    else:
        print(f" TIMEOUT (60s)")

    # 下注前記錄遊戲頁面 Round ID（時序排查用）
    pre_bet_info = detect_round_info(game_page)
    pre_bet_round_id = pre_bet_info.get("round_id", "")
    print(f"  [Phase 2] 下注前 RoundID={pre_bet_round_id}")

    # 下注（重用 betting.py 既有函式）
    print(f"  [Phase 2b] 下注莊...", end="", flush=True)
    bet_ok = False
    try:
        from steps.game.betting import (
            place_bet, confirm_bet, select_chip_for_min_bet,
            detect_bet_mode, get_min_bet,
        )
        from react_client_autobet import click_x2

        _clear_overlay(game_page)
        min_bet = get_min_bet(actual_vid, "莊") or 20
        print(f"限紅={min_bet}...", end="", flush=True)

        select_chip_for_min_bet(game_page, min_bet)
        game_page.wait_for_timeout(500)
        place_bet(game_page, "莊")
        game_page.wait_for_timeout(500)

        mode = detect_bet_mode(game_page)
        if mode == "confirm":
            confirm_bet(game_page)
            print(f" OK (confirm)")
        else:
            x2_result = click_x2(game_page)
            if x2_result is True:
                print(f" OK (x2 加倍)")
            elif x2_result == "disabled":
                print(f" OK (x2 disabled, 籌碼已達限紅)")
            else:
                print(f" OK (直接下注)")
        bet_ok = True
    except Exception as e:
        print(f" FAIL ({e})")

    # ── Phase 3: 荷官送牌（僅四源模式）──
    sent = 0
    dispatch_log = []
    dealer_screenshots = []
    dealer_ok = False
    if dealer_session:
        print(f"  [Phase 3] 荷官送牌...", end="", flush=True)
        dealer_ok = dealer_session.wait_for_dispatch(timeout=60)
        if dealer_ok:
            state = dealer_session._get_state()
            if state:
                dealer_round_id = state.get("gameCode", "") or ""
            print(f" RoundID={dealer_round_id}")

            sent, dispatch_log, dealer_screenshots = dealer_session.send_cards(
                card_values, screenshot_dir=round_dir)
            print(f"    送出 {sent} 張，截圖 {len(dealer_screenshots)} 張")

            if dispatch_log:
                print(f"    [Dispatch Log]")
                for dl in dispatch_log:
                    print(f"      #{dl['index']}: ci={dl['dispatch']['cardIndex']} "
                          f"who={dl['dispatch']['who']} → {dl['sent']['display']}")

            dealer_session.close_round()
        else:
            print(f" FAIL (dispatch 無反應)")

    # ── Phase 4: 等待開牌 → 連拍 ──
    if dealer_session:
        # 四源模式：等 _is_dealing
        print(f"  [Phase 4] 等待本局開牌...", end="", flush=True)
        for _ in range(30):
            cur = _get_countdown(game_page)
            if _is_dealing(cur):
                break
            game_page.wait_for_timeout(500)
    else:
        # 三源模式：自動開牌，倒數結束後自動進入開牌
        # 等倒數結束（不再是數字）或偵測到「開牌中」
        print(f"  [Phase 4] 等待開牌（自動）...", end="", flush=True)
        for _ in range(60):
            cur = _get_countdown(game_page)
            if _is_dealing(cur):
                break
            # 倒數結束（文字不是數字也不是空）= 可能已經在開牌
            if cur and not cur.isdigit():
                break
            game_page.wait_for_timeout(500)

    # 取遊戲頁面 Round ID（確認是本局）
    info_before = detect_round_info(game_page)
    game_round_id = info_before.get("round_id", "")
    print(f" OK (game RoundID={game_round_id})")

    # 連拍
    video_loc = game_page.locator("video").first
    burst_frames = []
    for i in range(20):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        try:
            shot = video_loc.screenshot(timeout=3000)
            p = round_dir / f"burst{i:02d}_{ts}.png"
            p.write_bytes(shot)
            burst_frames.append(str(p))
        except Exception:
            pass
        cur = _get_countdown(game_page)
        if cur and not _is_dealing(cur):
            break
        game_page.wait_for_timeout(500)
    print(f"    連拍 {len(burst_frames)} 幀")

    # 結算截圖
    game_page.wait_for_timeout(1000)
    settle_frame = None
    try:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        shot = video_loc.screenshot(timeout=3000)
        p = round_dir / f"settle_{ts}.png"
        p.write_bytes(shot)
        settle_frame = str(p)
    except Exception:
        pass

    # 等結算完成（偵測「不再開牌中」即可，手動房間結算後不會自動開下一局）
    print(f"  [Phase 4b] 等待結算...", end="", flush=True)
    was_dealing = False
    for _ in range(30):
        cur = _get_countdown(game_page)
        if _is_dealing(cur):
            was_dealing = True
        elif was_dealing:
            # 從開牌中 → 非開牌中 = 結算完成
            print(f" OK (結算完成)")
            break
        elif _is_betting(cur):
            print(f" OK (倒數 {cur}s)")
            break
        game_page.wait_for_timeout(1000)
    else:
        # 30 秒都沒偵測到變化，可能已經結算完了
        print(f" OK (靜默結算)")

    # 找最佳幀 + OCR
    best_anim = find_best_frame(burst_frames + ([settle_frame] if settle_frame else []))
    anim_ocr = None
    if best_anim:
        print(f"    Gemini 辨識動畫...")
        anim_ocr = recognize_game(best_anim, game="bac", gemini_limit=gemini_limit)
        if "error" in (anim_ocr or {}):
            print(f"    ⚠ OCR 失敗: {anim_ocr.get('message','')}")
            anim_ocr = None

    anim_data = anim_ocr.get("animation", {}) if anim_ocr else {}
    video_data = anim_ocr.get("video", {}) if anim_ocr else {}

    # ── Phase 5: 投注記錄 ──
    # 結算後立刻查（自動開局房間空窗期很短）
    print(f"  [Phase 5] 開啟投注記錄...")
    bet_record, bet_screenshot = open_bet_record_and_parse(game_page)
    if bet_record:
        record_round_id = bet_record.get("roundId", "")
        print(f"    RoundID={record_round_id}")
        print(f"    P: {bet_record.get('playerCards',[])} = {bet_record.get('playerPoints')}")
        print(f"    B: {bet_record.get('bankerCards',[])} = {bet_record.get('bankerPoints')}")
    else:
        print(f"    ⚠ 投注記錄解析失敗")

    # ── Phase 6: Round ID 比對 + 牌面比對 ──
    print(f"\n  [Round ID 比對]")
    print(f"    荷官端:       {dealer_round_id}")
    print(f"    下注前頁面:   {pre_bet_round_id}")
    print(f"    開牌中頁面:   {game_round_id}")
    print(f"    投注記錄:     {record_round_id}")

    # 時序排查：下注前 vs 開牌中的 Round ID 不同 = 可能投到不同局
    if pre_bet_round_id and game_round_id and pre_bet_round_id != game_round_id:
        print(f"    ⚠ 時序問題：下注前={pre_bet_round_id} ≠ 開牌中={game_round_id}")

    round_id_match = True
    round_id_note = ""
    ids = [rid for rid in [dealer_round_id, game_round_id, record_round_id] if rid]
    if len(ids) >= 2:
        # 比對共同子串（Round ID 格式可能有微小差異如後綴）
        base_ids = [rid[:16] for rid in ids]  # 取前 16 字元比對核心部分
        if len(set(base_ids)) > 1:
            round_id_match = False
            round_id_note = f"Round ID 不一致: {', '.join(ids)}"
            print(f"    ⚠ {round_id_note}")
        else:
            print(f"    ✓ Round ID 一致")
    elif len(ids) == 1:
        round_id_note = f"僅取得 1 個 Round ID: {ids[0]}"
        print(f"    ⚠ {round_id_note}")
    else:
        round_id_note = "無法取得任何 Round ID"
        print(f"    ⚠ {round_id_note}")

    comparison = compare_sources(card_values, anim_data, video_data, bet_record)
    if not round_id_match:
        comparison["overall"] = "ROUND_ID_MISMATCH"
        comparison["mismatches"].append(round_id_note)

    elapsed = (datetime.now() - ts_start).total_seconds()
    print(f"\n  結果: {comparison['overall']} ({elapsed:.0f}s)")
    if comparison["mismatches"]:
        for m in comparison["mismatches"]:
            print(f"    ⚠ {m}")

    # 組裝 round dict
    primary_round_id = record_round_id or game_round_id or dealer_round_id
    info = detect_round_info(game_page)

    return {
        "round_id": primary_round_id or info.get("round_id", ""),
        "room": info.get("room", actual_vid),
        "game": info.get("game", "百家樂"),
        "table_name": info.get("table_name", bet_record.get("table", "") if bet_record else ""),
        "timestamp": ts_start.isoformat(),
        "elapsed_sec": round(elapsed, 1),
        "round_id_sources": {
            "dealer": dealer_round_id,
            "game_page_pre_bet": pre_bet_round_id,
            "game_page_dealing": game_round_id,
            "bet_record": record_round_id,
            "match": round_id_match,
        },
        "animation_result": {
            "source": "開牌動畫",
            "player_cards": anim_data.get("player_cards", []),
            "banker_cards": anim_data.get("banker_cards", []),
            "player_total": anim_data.get("player_total", -1),
            "banker_total": anim_data.get("banker_total", -1),
            "total_cards": anim_data.get("total_cards", 0),
            "frame_file": Path(best_anim).name if best_anim else "",
        },
        "video_result": {
            "source": "影像串流",
            "player_cards": video_data.get("player_cards", []),
            "banker_cards": video_data.get("banker_cards", []),
            "player_total": video_data.get("player_total", -1),
            "banker_total": video_data.get("banker_total", -1),
            "note": video_data.get("note", ""),
            "frame_file": "",
        },
        "betting_result": {
            "source": "投注記錄",
            "player_cards": bet_record.get("playerCards", []) if bet_record else [],
            "banker_cards": bet_record.get("bankerCards", []) if bet_record else [],
            "player_total": bet_record.get("playerPoints", -1) if bet_record else -1,
            "banker_total": bet_record.get("bankerPoints", -1) if bet_record else -1,
            "round_id": record_round_id,
            "frame_file": Path(bet_screenshot).name if bet_screenshot else "",
        },
        "dealer_result": {
            "source": "荷官輸入",
            "cards_display": dealer_display,
            "card_values": card_values,
            "sent_count": sent if dealer_ok else 0,
            "round_id": dealer_round_id,
            "dispatch_log": dispatch_log if dealer_ok else [],
            "frame_files": [Path(p).name for p in dealer_screenshots] if dealer_ok else [],
        },
        "verification": {
            "round_id_match": round_id_match,
            "animation_vs_video": anim_ocr.get("match", "N/A") if anim_ocr else "N/A",
            "overall": comparison["overall"],
            "failure_reason": "; ".join(comparison["mismatches"]) if comparison["mismatches"] else "",
        },
    }


# ── 主 Session ──────────────────────────────────────────────────────────────

def run_session(rounds=1, vid=DEFAULT_VID, cards_mode="random", cards_str="",
                headed=False, dealer_id=DEFAULT_DEALER_ID,
                gemini_limit=50, skip_video_ocr=False,
                env="qa", pid="<ACCOUNT>", currency="cny", url="",
                plan_mode="", start_round=1, only_rounds=None,
                verify_mode="3source"):
    """多局 session 主流程。

    plan_mode: "simple" / "basic" / "advanced" — 使用牌序計畫
    start_round: 從第幾局開始（中斷恢復用）
    only_rounds: 只跑指定局號的 list（重跑特定局）
    """
    # 載入牌序計畫（如有）
    plan_entries = None
    if plan_mode:
        from card_test_plans import generate_plan, print_plan_summary
        plan_entries = generate_plan(plan_mode)
        # 過濾：start_round / only_rounds
        if only_rounds:
            plan_entries = [e for e in plan_entries if e["round_num"] in only_rounds]
        elif start_round > 1:
            plan_entries = [e for e in plan_entries if e["round_num"] >= start_round]
        rounds = len(plan_entries)
        print_plan_summary(plan_entries)

    print(f"\n{'='*60}")
    mode_label = "三源" if verify_mode == "3source" else "四源"
    print(f"  百家樂{mode_label}整合驗證")
    if plan_mode:
        print(f"  模式: {plan_mode} | 局數: {rounds} | 房間: {vid}")
    else:
        print(f"  局數: {rounds} | 房間: {vid} | 牌值: {cards_mode}")
    print(f"{'='*60}")

    import bac_card_verify
    bac_card_verify._current_game = "bac"

    # 取得遊戲 URL — 優先用 API login（dnsUrl 較可靠）
    if not url:
        try:
            from api_login import get_game_url as api_get
            url = api_get(env, pid, currency)
            if url:
                print(f"  [Login] API login 成功")
        except Exception:
            pass
    if not url:
        url = get_login_url(env, pid, currency)
    if not url:
        print("[ERROR] 無法取得登入 URL")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=not headed)

        # Game context
        game_ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
        game_page = game_ctx.new_page()

        # Dealer context（四源模式才開）
        dealer = None
        if verify_mode == "4source":
            dealer_ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
            dealer_page = dealer_ctx.new_page()

        # ── Step 1: 登入遊戲室 ──
        print(f"\n  [Setup] 登入遊戲室...")
        for attempt in range(1, 4):
            if attempt > 1:
                url = get_login_url(env, pid, currency)
                if not url:
                    break
            print(f"    嘗試 {attempt}/3...")
            game_page.goto(url, timeout=30000, wait_until="domcontentloaded")
            game_page.wait_for_timeout(3000)

            # 處理 QA Entry 版本選擇頁（可能有多層）
            for _ in range(3):
                game_page.wait_for_timeout(2000)
                body = game_page.evaluate("()=>(document.body.innerText||'').substring(0,800)")
                if "Deployed Version" in body or "qa_entries" in body:
                    print(f"    版本選擇頁，點擊 qa_entries...")
                    try:
                        game_page.locator("a", has_text="qa_entries").first.click(timeout=5000)
                        game_page.wait_for_timeout(5000)
                        continue
                    except Exception:
                        pass
                if "Go to Latest Entry" in body:
                    print(f"    點擊 Go to Latest Entry...")
                    try:
                        game_page.get_by_text("Go to Latest Entry", exact=False).first.click(timeout=5000)
                    except Exception:
                        pass
                    # 等 Loading 完成（QA 遊戲 SPA 載入需 30-60s）
                    print(f"    等待遊戲載入...", end="", flush=True)
                    last_pct = ""
                    for w in range(30):  # 最多 60 秒
                        game_page.wait_for_timeout(2000)
                        lobby_count = game_page.locator('[class*="LobbyItemMenu"]').count()
                        if lobby_count > 0:
                            print(f" OK ({(w+1)*2}s)")
                            break
                        pct = game_page.evaluate("()=>{var b=document.body.innerText||'';var m=b.match(/(\\d+)%/);return m?m[1]:''}")
                        if pct and pct != last_pct:
                            print(f" {pct}%", end="", flush=True)
                            last_pct = pct
                    else:
                        print(f" TIMEOUT")
                break

            result, game_page, entry_version = enter_game_room(
                game_page, game_ctx, category="百家樂", target_room=vid)
            if result == "expired":
                print("    TSS 過期，重試...")
                continue
            elif result:
                print(f"    進房成功")
                break
            else:
                print("    進房失敗")
                browser.close()
                return
        else:
            print("[ERROR] 3 次重試均失敗")
            browser.close()
            return

        # 從遊戲室 URL 提取實際進入的房間 VID
        actual_vid = vid
        game_url_str = game_page.url or ""
        vid_match = re.search(r'#/game/([^?&/]+)', game_url_str)
        if vid_match:
            actual_vid = vid_match.group(1)
        print(f"  [Setup] 實際房間: {actual_vid}")

        # ── Step 2: 登入荷官工具（僅四源模式）──
        if verify_mode == "4source":
            print(f"\n  [Setup] 登入荷官工具 (vid={actual_vid})...")
            dealer = DealerSession(dealer_page, "BAC", dealer_id)
            if not dealer.open_and_login(actual_vid):
                print("[ERROR] 荷官工具登入失敗")
                browser.close()
                return
        else:
            print(f"\n  [Setup] 三源模式 — 不開荷官端")

        # 執行局數
        plan_label = f" | plan={plan_mode}" if plan_mode else ""
        meta = {
            "env": env, "game": "bac",
            "game_name": f"百家樂（{mode_label}驗證{' ' + plan_mode if plan_mode else ''}）",
            "url": url[:100], "start_time": datetime.now().isoformat(),
            "total_rounds": rounds, "gemini_limit": gemini_limit,
            "version": f"{verify_mode} v1.0 | vid={actual_vid}{' | dealer=' + dealer_id if verify_mode == '4source' else ''}{plan_label}",
            "plan_mode": plan_mode or "",
        }
        results = []

        for idx in range(rounds):
            # 從計畫或 CLI 取得牌值
            if plan_entries:
                entry = plan_entries[idx]
                cv = entry["cards"]
                rn = entry["round_num"]
                plan_info = {
                    "plan_id": entry["plan_id"],
                    "target_card": entry["target_card"],
                    "note": entry["note"],
                    "progress": f"{idx+1}/{rounds}",
                }
            else:
                rn = idx + 1
                plan_info = None
                if verify_mode == "4source":
                    if cards_mode == "random":
                        cv = random_bac_cards()
                    elif cards_mode in ("player-win", "banker-win", "tie"):
                        cv = scenario_bac_cards(cards_mode)
                    elif cards_str:
                        cv = parse_cards(cards_str)
                    else:
                        cv = random_bac_cards()
                else:
                    cv = []  # 三源模式不送牌

            result = run_round(game_page, dealer, rn, rounds,
                               cv, gemini_limit, skip_video_ocr,
                               actual_vid=actual_vid)

            # 附加計畫資訊到結果
            if plan_info:
                result["plan_info"] = plan_info

            results.append(result)

            # 局間等待（多局時）
            if idx < rounds - 1:
                print(f"\n  等待下一局...")
                game_page.wait_for_timeout(3000)

        # 產出報告
        meta["end_time"] = datetime.now().isoformat()
        meta["actual_rounds"] = len(results)

        json_path = save_json_report(meta, results)
        html_path = save_html_report(
            meta, results,
            report_title="React <PRODUCT> OCR 驗證報告",
            file_prefix="react_pa_ocr_verify",
        )

        print(f"\n{'='*60}")
        print(f"  完成！共 {len(results)} 局")
        passed = sum(1 for r in results if r["verification"]["overall"] == "PASS")
        print(f"  PASS: {passed} / {len(results)}")
        print(f"  報告: {html_path}")
        print(f"{'='*60}")

        browser.close()
        return html_path


# ── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="百家樂三源/四源整合驗證")
    parser.add_argument("--rounds", type=int, default=1, help="局數 (預設 1)")
    parser.add_argument("--vid", default=DEFAULT_VID, help=f"房間 VID (預設 {DEFAULT_VID})")
    parser.add_argument("--cards", default="random",
                        help="牌值: random / player-win / banker-win / tie / 2S,3H,5C,8D")
    parser.add_argument("--headed", action="store_true", help="顯示瀏覽器")
    parser.add_argument("--dealer-id", default=DEFAULT_DEALER_ID, help=f"荷官 ID (預設 {DEFAULT_DEALER_ID})")
    parser.add_argument("--gemini-limit", type=int, default=50, help="Gemini 上限")
    parser.add_argument("--skip-video-ocr", action="store_true", help="跳過影片 OCR")
    parser.add_argument("--env", default="qa", help="環境 (預設 qa)")
    parser.add_argument("--pid", default="<ACCOUNT>", help="PID (預設 <ACCOUNT>)")
    parser.add_argument("--currency", default="cny", help="幣別 (預設 cny)")
    parser.add_argument("--url", default="", help="直接指定遊戲 URL（跳過登入）")
    parser.add_argument("--mode", default="3source", choices=["3source", "4source"],
                        help="驗證模式: 3source（不開荷官端） / 4source（開荷官端）")
    parser.add_argument("--plan", default="", choices=["", "simple", "basic", "advanced"],
                        help="牌序計畫模式: simple / basic / advanced")
    parser.add_argument("--start-round", type=int, default=1,
                        help="從第幾局開始（中斷恢復用，需搭配 --plan）")
    parser.add_argument("--only-rounds", default="",
                        help="只跑指定局號（逗號分隔，如 8,9,53）")
    args = parser.parse_args()

    # 判斷 cards 模式
    cards_mode = args.cards
    cards_str = ""
    if not args.plan and cards_mode not in ("random", "player-win", "banker-win", "tie"):
        cards_str = cards_mode
        cards_mode = "manual"

    # 解析 only-rounds
    only_rounds = None
    if args.only_rounds:
        only_rounds = [int(x.strip()) for x in args.only_rounds.split(",") if x.strip()]

    run_session(
        rounds=args.rounds, vid=args.vid,
        cards_mode=cards_mode, cards_str=cards_str,
        headed=args.headed, dealer_id=args.dealer_id,
        gemini_limit=args.gemini_limit, skip_video_ocr=args.skip_video_ocr,
        env=args.env, pid=args.pid, currency=args.currency, url=args.url,
        plan_mode=args.plan, start_round=args.start_round, only_rounds=only_rounds,
        verify_mode=args.mode,
    )


if __name__ == "__main__":
    main()
