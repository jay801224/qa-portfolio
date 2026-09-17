"""
diag_bac_js_inject.py — 診斷 BAC 百家樂 JS 注入是否有效

目的：
  1. 開啟荷官端 N011，登入
  2. 送出已知牌序（全用特定牌值）
  3. 監聽 ALL console 輸出（不過濾），記錄伺服器回傳
  4. 檢查 sendNextCard 回傳值 + dispatchCardResp 變化
  5. 產出診斷報告：JS 注入是否真的被伺服器接受

用法：
  cd shared/OCR
  python diag_bac_js_inject.py --vid N011 --headed
"""

import argparse
import json
import re
import sys
import time
import threading
from pathlib import Path
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "react" / "python"))

from qa_auto_dealer import (
    CARD_GAMES, SHBConsoleMonitor, card_display, decode_card,
    encode_card,
)


# 已知牌序：A♠ 2♥ 3♣ 4♦ 5♠ 6♥ → cardValue = 1, 6, 11, 16, 17, 22
KNOWN_CARDS = [
    encode_card(1, 1),   # A♠ = 1
    encode_card(2, 2),   # 2♥ = 6
    encode_card(3, 3),   # 3♣ = 11
    encode_card(4, 4),   # 4♦ = 16
    encode_card(5, 1),   # 5♠ = 17
    encode_card(6, 2),   # 6♥ = 22
]


class FullConsoleCapture:
    """捕獲 ALL console 輸出，不過濾。"""

    def __init__(self):
        self.lock = threading.Lock()
        self.messages = []

    def on_console(self, msg):
        text = msg.text
        with self.lock:
            self.messages.append((time.time(), text))

    def dump(self, since=None):
        since = since or 0
        with self.lock:
            return [(t, m) for t, m in self.messages if t >= since]


def build_dealer_url(vid):
    try:
        sys.path.insert(0, str(PROJECT_ROOT / "react" / "python"))
        from network_config import get_url
        return get_url(8082, f"/dealer-tools/main/?vid={vid}&isManual=true")
    except ImportError:
        return f"http://example.internal:8082/dealer-tools/main/?vid={vid}&isManual=true"


def js_call(page, store_module, store_class, body):
    return page.evaluate(f'''(function(){{
        var fn = window[Object.keys(window).find(function(k){{return k.startsWith("$getInstance")}})];
        if (!fn) return null;
        var s = null;
        if (typeof {store_module} !== 'undefined' && {store_module}.DataStore)
            s = fn({store_class});
        if (!s) s = fn(Plaza.DataStoreBase);
        if (!s) return null;
        {body}
    }})()''')


def run_diagnostic(vid, headed, dealer_id):
    from playwright.sync_api import sync_playwright

    cfg = CARD_GAMES["BAC"]
    store_class = cfg["store"]
    store_module = store_class.split(".")[0]
    send_method = cfg["send"]

    url = build_dealer_url(vid)

    print("=" * 60)
    print("  BAC JS 注入診斷")
    print("=" * 60)
    print(f"  房間: {vid}")
    print(f"  URL:  {url}")
    print(f"  Store: {store_class}")
    print(f"  Send:  {send_method}")
    print(f"  已知牌序: {' '.join(card_display(c) for c in KNOWN_CARDS)}")
    print(f"  牌值:     {KNOWN_CARDS}")
    print()

    monitor = SHBConsoleMonitor()
    full_capture = FullConsoleCapture()

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=not headed)
        ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = ctx.new_page()
        page.route("**/*nanocosmos*", lambda route: route.abort())
        page.route("**/*h5live*", lambda route: route.abort())
        page.on("console", monitor.on_console)
        page.on("console", full_capture.on_console)

        def _dismiss(d):
            try:
                d.accept()
            except Exception:
                pass
        page.on("dialog", _dismiss)

        # ── Step 1: 載入 ──
        print("[Step 1] 載入 Dealer Tool...", end="", flush=True)
        try:
            page.goto(url, wait_until="networkidle", timeout=60000)
        except Exception:
            pass
        page.wait_for_timeout(10000)
        print(" OK")

        # ── Step 2: 登入 ──
        print(f"[Step 2] 登入 ID={dealer_id}...", end="", flush=True)
        t_login = time.time()
        for ch in str(dealer_id):
            page.keyboard.press(ch)
            time.sleep(0.4)
        time.sleep(0.8)
        page.keyboard.press("NumpadMultiply")

        login_data = monitor.wait_for("login", timeout=60, since=t_login, page=page)
        if login_data and login_data.get("retCode") == 0:
            print(" OK")
        else:
            # fallback: JS 探測
            page.wait_for_timeout(5000)
            gs = js_call(page, store_module, store_class,
                         "return typeof s.getGameStatus==='function' ? s.getGameStatus() : -1;")
            if gs is not None and gs >= 0:
                print(f" OK (via JS, gs={gs})")
            else:
                print(f" FAIL ({login_data}, gs={gs})")
                browser.close()
                return

        page.wait_for_timeout(3000)

        # ── Step 3: 探測可用的 API 方法 ──
        print()
        print("[Step 3] 探測 DataStore 方法...")
        methods_check = js_call(page, store_module, store_class, """
            var methods = {};
            methods.sendNextCard = typeof s.sendNextCard === 'function';
            methods.sendNextCardProto = typeof s.sendNextCardProto === 'function';
            methods.dealerStartGame = typeof s.dealerStartGame === 'function';
            methods.dealerCloseRound = typeof s.dealerCloseRound === 'function';
            methods.getGameStatus = typeof s.getGameStatus === 'function';
            methods.dispatchCardResp = !!s.dispatchCardResp;

            // 探測 sendNextCard 的參數定義
            if (typeof s.sendNextCard === 'function') {
                methods.sendNextCard_src = s.sendNextCard.toString().substring(0, 200);
            }
            if (typeof s.sendNextCardProto === 'function') {
                methods.sendNextCardProto_src = s.sendNextCardProto.toString().substring(0, 200);
            }

            // 探測 store 的所有方法名
            var allMethods = [];
            for (var key in s) {
                if (typeof s[key] === 'function' && key.toLowerCase().indexOf('card') >= 0) {
                    allMethods.push(key);
                }
            }
            methods.card_related_methods = allMethods;

            // 探測 send 相關方法
            var sendMethods = [];
            for (var key in s) {
                if (typeof s[key] === 'function' && key.toLowerCase().indexOf('send') >= 0) {
                    sendMethods.push(key);
                }
            }
            methods.send_related_methods = sendMethods;

            return methods;
        """)

        if methods_check:
            print(f"  sendNextCard:      {methods_check.get('sendNextCard')}")
            print(f"  sendNextCardProto: {methods_check.get('sendNextCardProto')}")
            print(f"  dealerStartGame:   {methods_check.get('dealerStartGame')}")
            print(f"  dealerCloseRound:  {methods_check.get('dealerCloseRound')}")
            print(f"  getGameStatus:     {methods_check.get('getGameStatus')}")
            print(f"  dispatchCardResp:  {methods_check.get('dispatchCardResp')}")
            print()
            print(f"  card 相關方法: {methods_check.get('card_related_methods', [])}")
            print(f"  send 相關方法: {methods_check.get('send_related_methods', [])}")
            if methods_check.get('sendNextCard_src'):
                print(f"\n  sendNextCard 原始碼片段:")
                print(f"    {methods_check['sendNextCard_src']}")
            if methods_check.get('sendNextCardProto_src'):
                print(f"\n  sendNextCardProto 原始碼片段:")
                print(f"    {methods_check['sendNextCardProto_src']}")
        else:
            print("  [ERROR] 無法取得 DataStore")
            browser.close()
            return

        # ── Step 4: 開局 + 送牌 ──
        print()
        print("[Step 4] 開局...")

        gs = js_call(page, store_module, store_class,
                     "return typeof s.getGameStatus==='function' ? s.getGameStatus() : -1;")
        print(f"  當前 gameStatus = {gs}")

        # 如果 gs=2, closeRound 先
        if gs == 2:
            print("  gs=2, 先 closeRound...", end="", flush=True)
            js_call(page, store_module, store_class, "if (s.dealerCloseRound) s.dealerCloseRound();")
            page.wait_for_timeout(5000)
            gs = js_call(page, store_module, store_class,
                         "return typeof s.getGameStatus==='function' ? s.getGameStatus() : -1;")
            print(f" gs={gs}")

        # startGame
        if gs == 0:
            print("  startGame...", end="", flush=True)
            js_call(page, store_module, store_class, "if (s.dealerStartGame) s.dealerStartGame();")
            for t in range(30):
                page.wait_for_timeout(1000)
                gs = js_call(page, store_module, store_class,
                             "return typeof s.getGameStatus==='function' ? s.getGameStatus() : -1;")
                if gs == 1:
                    print(f" gs=1 倒數中 ({t+1}s)")
                    break
                if gs == 2:
                    print(f" gs=2 ({t+1}s)")
                    break
                if t % 5 == 4:
                    print(f" gs={gs}({t+1}s)", end="", flush=True)
            else:
                print(f" 超時 gs={gs}")

        # 等待 dispatch
        print("  等待 dispatch...", end="", flush=True)
        t_dispatch = time.time()
        dispatch_found = False
        for t in range(60):
            state = js_call(page, store_module, store_class, """
                var d = s.dispatchCardResp;
                if (!d) return null;
                return {
                    cardIndex: d.cardIndex || d.cardindex || 0,
                    who: d.who || 0,
                    visible: d.visible || 1,
                    gameCode: d.gameCode || '',
                    handindex: d.handindex || d.handIndex || 0,
                    raw: JSON.stringify(d).substring(0, 500)
                };
            """)
            if state and state.get("cardIndex", 0) >= 1:
                print(f" 就緒 ({t+1}s)")
                print(f"  dispatch 原始: {state.get('raw', '')}")
                dispatch_found = True
                break
            if t % 10 == 9:
                gs2 = js_call(page, store_module, store_class,
                              "return typeof s.getGameStatus==='function' ? s.getGameStatus() : -1;")
                print(f" gs={gs2}({t+1}s)", end="", flush=True)
                if gs2 == 0 or gs2 == 2:
                    js_call(page, store_module, store_class, "if (s.dealerStartGame) s.dealerStartGame();")
            page.wait_for_timeout(1000)

        if not dispatch_found:
            print(f" 無 dispatch，放棄")
            # 顯示所有 console
            print("\n[Console dump]")
            for ts, msg in full_capture.dump(since=t_login):
                if len(msg) > 10:
                    print(f"  [{datetime.fromtimestamp(ts).strftime('%H:%M:%S')}] {msg[:200]}")
            browser.close()
            return

        # ── Step 5: 逐張送牌 + 驗證 ──
        print()
        print("[Step 5] 送牌 + 驗證（關鍵步驟）")
        print(f"  計畫送出: {' '.join(card_display(c) for c in KNOWN_CARDS)}")
        print()

        t_send_start = time.time()
        sent_cards = []
        send_results = []

        for attempt in range(12):
            # 讀取當前 dispatch 狀態
            state = js_call(page, store_module, store_class, """
                var d = s.dispatchCardResp;
                if (!d) return {disp: false, gs: typeof s.getGameStatus==='function' ? s.getGameStatus() : -1};
                return {
                    disp: true,
                    gs: typeof s.getGameStatus==='function' ? s.getGameStatus() : -1,
                    cardIndex: d.cardIndex || d.cardindex || 0,
                    who: d.who || 0,
                    visible: d.visible || 1,
                    gameCode: d.gameCode || '',
                    raw: JSON.stringify(d).substring(0, 500)
                };
            """)

            if not state or not state.get("disp"):
                gs_now = state.get("gs", -1) if state else -1
                if gs_now <= 0:
                    print(f"  [結束] 無 dispatch, gs={gs_now}")
                    break
                page.wait_for_timeout(1000)
                continue

            ci = state.get("cardIndex", 0)
            who = state.get("who", 0)
            vis = state.get("visible", 1)

            if ci > 6:
                break

            idx = len(sent_cards)
            if idx >= len(KNOWN_CARDS):
                break

            val = KNOWN_CARDS[idx]
            print(f"  送牌 #{idx+1}: dispatch ci={ci} who={who} vis={vis}")
            print(f"    → 準備送 val={val} ({card_display(val)})")

            # 送牌前截取 dispatch 原始狀態
            pre_dispatch = state.get("raw", "")

            # ==== 核心送牌 ====
            if send_method == "sendNextCardProto":
                send_result = js_call(page, store_module, store_class,
                    f"""
                    var ret = null;
                    if (s.sendNextCardProto) {{
                        ret = s.sendNextCardProto([{{cardindex:{ci},val:{val},handindex:0}}]);
                    }}
                    return {{ret: ret === undefined ? 'undefined' : JSON.stringify(ret)}};
                    """)
            else:
                send_result = js_call(page, store_module, store_class,
                    f"""
                    var ret = null;
                    if (s.sendNextCard) {{
                        ret = s.sendNextCard({val},{ci},{vis},{who});
                    }}
                    return {{ret: ret === undefined ? 'undefined' : JSON.stringify(ret)}};
                    """)

            print(f"    → sendNextCard 回傳: {send_result}")

            page.wait_for_timeout(2000)

            # 送牌後檢查 dispatch 是否變化
            post_state = js_call(page, store_module, store_class, """
                var d = s.dispatchCardResp;
                if (!d) return {disp: false};
                return {
                    disp: true,
                    cardIndex: d.cardIndex || d.cardindex || 0,
                    who: d.who || 0,
                    visible: d.visible || 1,
                    raw: JSON.stringify(d).substring(0, 500)
                };
            """)

            post_ci = post_state.get("cardIndex", 0) if post_state else 0
            ci_advanced = post_ci > ci

            print(f"    → 送牌後 dispatch ci: {ci} → {post_ci} (推進={'是' if ci_advanced else '否'})")
            if post_state:
                print(f"    → 送牌後 dispatch raw: {post_state.get('raw', '')[:200]}")

            sent_cards.append(val)
            send_results.append({
                "index": idx,
                "val_sent": val,
                "display_sent": card_display(val),
                "dispatch_ci_before": ci,
                "dispatch_ci_after": post_ci,
                "ci_advanced": ci_advanced,
                "send_return": send_result,
                "pre_dispatch": pre_dispatch[:200],
                "post_dispatch": post_state.get("raw", "")[:200] if post_state else "",
            })

            if ci >= 6:
                print(f"  [完成] ci=6 最後一張")
                break

            page.wait_for_timeout(1000)

        # ── Step 6: 等待結算 + 收集結果 ──
        print()
        print("[Step 6] 等待結算...")
        page.wait_for_timeout(5000)

        # 檢查 game_result 相關的 console 輸出
        game_result = js_call(page, store_module, store_class, """
            // 嘗試取得最終遊戲結果
            var result = {};
            if (s.gameResultResp) result.gameResult = JSON.stringify(s.gameResultResp).substring(0, 1000);
            if (s.cardList) result.cardList = JSON.stringify(s.cardList).substring(0, 500);
            if (s.bacResultResp) result.bacResult = JSON.stringify(s.bacResultResp).substring(0, 500);
            // 嘗試用各種名稱找結果
            var resultKeys = [];
            for (var k in s) {
                if (k.toLowerCase().indexOf('result') >= 0 || k.toLowerCase().indexOf('card') >= 0) {
                    var v = s[k];
                    if (v !== null && v !== undefined && typeof v !== 'function') {
                        resultKeys.push(k + '=' + JSON.stringify(v).substring(0, 100));
                    }
                }
            }
            result.resultKeys = resultKeys;
            return result;
        """)

        print(f"  DataStore 中 result/card 相關屬性:")
        if game_result:
            for key in game_result.get("resultKeys", []):
                print(f"    {key}")
            if game_result.get("gameResult"):
                print(f"\n  gameResultResp: {game_result['gameResult'][:300]}")
            if game_result.get("bacResult"):
                print(f"  bacResultResp:  {game_result['bacResult'][:300]}")

        # ── Step 7: Console 完整輸出（送牌期間）──
        print()
        print("[Step 7] 送牌期間 Console 輸出（過濾空白/短訊息）:")
        console_during_send = full_capture.dump(since=t_send_start)
        card_related_msgs = []
        for ts, msg in console_during_send:
            if len(msg) > 15:
                ts_str = datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                print(f"  [{ts_str}] {msg[:300]}")
                if any(kw in msg.lower() for kw in ['card', 'send', 'dispatch', 'result', 'game', 'round', 'bac']):
                    card_related_msgs.append(msg)

        # ── Step 8: 診斷結論 ──
        print()
        print("=" * 60)
        print("  診斷結論")
        print("=" * 60)
        print(f"  送出牌數: {len(sent_cards)}")
        print(f"  送出牌值: {sent_cards}")
        print(f"  送出顯示: {' '.join(card_display(c) for c in sent_cards)}")
        print()

        all_advanced = all(r["ci_advanced"] for r in send_results) if send_results else False
        print(f"  ci 是否每次都推進: {'是 ✓' if all_advanced else '否 ✗'}")

        # 判定
        if not send_results:
            verdict = "FAIL — 沒有成功送出任何牌"
        elif not all_advanced:
            verdict = "SUSPECT — ci 沒有推進，JS 注入可能被忽略"
        else:
            verdict = "NEED_VERIFY — ci 有推進，但需要對比前端實際顯示才能確定牌值是否正確"

        print(f"\n  判定: {verdict}")
        print()

        # closeRound
        js_call(page, store_module, store_class, "if (s.dealerCloseRound) s.dealerCloseRound();")
        page.wait_for_timeout(3000)

        # 如果是 headed 模式，暫停讓使用者觀察
        if headed:
            print("  [headed 模式] 瀏覽器保持開啟 30 秒供觀察...")
            page.wait_for_timeout(30000)

        browser.close()

    # 寫診斷報告
    report = {
        "timestamp": datetime.now().isoformat(),
        "vid": vid,
        "store": store_class,
        "send_method": send_method,
        "methods_available": methods_check,
        "known_cards": KNOWN_CARDS,
        "known_cards_display": [card_display(c) for c in KNOWN_CARDS],
        "send_results": send_results,
        "verdict": verdict,
        "console_card_related": card_related_msgs[:20],
    }
    report_path = PROJECT_ROOT / "shared" / "report" / "bac_verify" / f"diag_js_inject_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"  診斷報告: {report_path}")


def main():
    parser = argparse.ArgumentParser(description="BAC JS 注入診斷")
    parser.add_argument("--vid", default="N011", help="房間 ID")
    parser.add_argument("--headed", action="store_true", help="顯示瀏覽器")
    parser.add_argument("--dealer-id", default="8232", help="Dealer ID")
    args = parser.parse_args()
    run_diagnostic(args.vid, args.headed, args.dealer_id)


if __name__ == "__main__":
    main()
