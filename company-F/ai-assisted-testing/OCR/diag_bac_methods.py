"""
diag_bac_methods.py — BAC 四種替代送牌方法診斷

依序測試 4 種方法，每種送 4 張已知牌（A♠ 2♥ 3♣ 4♦），
檢查 resultCards 是否記錄了正確牌值。

方法：
  1. scanNextCard    — 模擬掃描器輸入
  2. sendModifyCard  — 修改已送出的牌
  3. manulScanBurnCard — 手動掃描燒牌
  4. sendNextCardProto — Proto 格式送牌（手動建構）

用法：
  cd shared/OCR
  python diag_bac_methods.py --vid N011 --headed
  python diag_bac_methods.py --vid N011 --headed --method 1      # 只測第 1 種
  python diag_bac_methods.py --vid N011 --headed --method 1,2    # 測第 1,2 種
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
    CARD_GAMES, SHBConsoleMonitor, card_display, encode_card,
)

# 已知牌序：A♠ 2♥ 3♣ 4♦ (只送 4 張基本牌，加快每輪速度)
KNOWN_CARDS = [
    encode_card(1, 1),   # A♠ = 1
    encode_card(2, 2),   # 2♥ = 6
    encode_card(3, 3),   # 3♣ = 11
    encode_card(4, 4),   # 4♦ = 16
]

STORE_MODULE = "GameBac"
STORE_CLASS = "GameBac.DataStore"


class FullConsoleCapture:
    def __init__(self):
        self.lock = threading.Lock()
        self.messages = []

    def on_console(self, msg):
        with self.lock:
            self.messages.append((time.time(), msg.text))

    def dump(self, since=None):
        since = since or 0
        with self.lock:
            return [(t, m) for t, m in self.messages if t >= since and len(m) > 10]

    def clear(self):
        with self.lock:
            self.messages.clear()


def build_dealer_url(vid):
    try:
        from network_config import get_url
        return get_url(8082, f"/dealer-tools/main/?vid={vid}&isManual=true")
    except ImportError:
        return f"http://example.internal:8082/dealer-tools/main/?vid={vid}&isManual=true"


def js(page, body):
    """執行 JS，自動取得 DataStore instance。"""
    return page.evaluate(f'''(function(){{
        var fn = window[Object.keys(window).find(function(k){{return k.startsWith("$getInstance")}})];
        if (!fn) return null;
        var s = null;
        if (typeof {STORE_MODULE} !== 'undefined' && {STORE_MODULE}.DataStore)
            s = fn({STORE_CLASS});
        if (!s) s = fn(Plaza.DataStoreBase);
        if (!s) return null;
        {body}
    }})()''')


def get_gs(page):
    return js(page, "return typeof s.getGameStatus==='function' ? s.getGameStatus() : -1;")


def get_dispatch(page):
    return js(page, """
        var d = s.dispatchCardResp;
        if (!d) return null;
        return {
            cardIndex: d.cardIndex || d.cardindex || 0,
            who: d.who || 0,
            visible: d.visible || 1,
            gameCode: d.gameCode || ''
        };
    """)


def get_result_cards(page):
    return js(page, """
        return {
            resultCards: s.resultCards ? Array.from(s.resultCards) : null,
            currentCardIndex: s.currentCardIndex || s._currentCardIndex || 0,
            isResultSubmited: !!s.isResultSubmited,
            result: s.result,
            scannedCards: s.scannedCards ? JSON.stringify(s.scannedCards).substring(0, 300) : null,
            cardListHash: s.cardListHash || ''
        };
    """)


def wait_for_fresh_dispatch(page, timeout=60):
    """等待一個新的 dispatch (ci <= 2)，必要時 startGame。"""
    print("  等待新局 dispatch...", end="", flush=True)

    for t in range(timeout):
        gs = get_gs(page)

        # gs=2 → closeRound
        if gs == 2:
            if t == 0 or t % 10 == 0:
                print(f" close(gs=2)", end="", flush=True)
                js(page, "if (s.dealerCloseRound) s.dealerCloseRound();")
                page.wait_for_timeout(3000)
                continue

        # gs=0 → startGame
        if gs == 0:
            if t == 0 or t % 10 == 0:
                print(f" start(gs=0)", end="", flush=True)
                js(page, "if (s.dealerStartGame) s.dealerStartGame();")

        # gs=1 → 倒數中，等結束
        d = get_dispatch(page)
        if d and d.get("cardIndex", 0) >= 1 and d.get("cardIndex", 0) <= 2:
            gc = d.get("gameCode", "")
            print(f" OK (ci={d['cardIndex']}, gc={gc})")
            return d

        if t % 10 == 9:
            print(f" ({t+1}s gs={gs})", end="", flush=True)

        page.wait_for_timeout(1000)

    print(f" 超時")
    return None


def probe_method_signatures(page):
    """探測所有四種方法的函數簽名。"""
    return js(page, """
        var sigs = {};

        if (typeof s.scanNextCard === 'function')
            sigs.scanNextCard = {exists: true, src: s.scanNextCard.toString().substring(0, 400), len: s.scanNextCard.length};
        else
            sigs.scanNextCard = {exists: false};

        if (typeof s.sendModifyCard === 'function')
            sigs.sendModifyCard = {exists: true, src: s.sendModifyCard.toString().substring(0, 400), len: s.sendModifyCard.length};
        else
            sigs.sendModifyCard = {exists: false};

        if (typeof s.manulScanBurnCard === 'function')
            sigs.manulScanBurnCard = {exists: true, src: s.manulScanBurnCard.toString().substring(0, 400), len: s.manulScanBurnCard.length};
        else
            sigs.manulScanBurnCard = {exists: false};

        if (typeof s.sendNextCardProto === 'function')
            sigs.sendNextCardProto = {exists: true, src: s.sendNextCardProto.toString().substring(0, 400), len: s.sendNextCardProto.length};
        else
            sigs.sendNextCardProto = {exists: false};

        // 額外：sendNextCard 完整原始碼
        if (typeof s.sendNextCard === 'function')
            sigs.sendNextCard = {exists: true, src: s.sendNextCard.toString().substring(0, 400), len: s.sendNextCard.length};

        // 額外：探測 APIManager 相關方法
        var apiMethods = [];
        try {
            var api = s.APIManager || (typeof Plaza !== 'undefined' ? Plaza.APIManager : null);
            if (!api) {
                // 嘗試從 module 搜尋
                for (var k in s) {
                    if (k === 'APIManager' || (s[k] && typeof s[k] === 'object' && s[k].sendCMDNewCard)) {
                        api = s[k];
                        break;
                    }
                }
            }
            if (api) {
                for (var k in api) {
                    if (typeof api[k] === 'function' && (k.indexOf('Card') >= 0 || k.indexOf('card') >= 0 || k.indexOf('scan') >= 0 || k.indexOf('Scan') >= 0)) {
                        apiMethods.push(k + '(' + api[k].length + ')');
                    }
                }
            }
        } catch(e) {}
        sigs.apiCardMethods = apiMethods;

        return sigs;
    """)


# ================================================================
# 四種送牌方法
# ================================================================

def method_1_scanNextCard(page, cards):
    """方法 1: scanNextCard — 模擬掃描器輸入"""
    print("\n" + "─" * 50)
    print("  方法 1: scanNextCard")
    print("─" * 50)

    d = wait_for_fresh_dispatch(page)
    if not d:
        return {"method": "scanNextCard", "success": False, "reason": "no dispatch"}

    t_start = time.time()
    sent = 0

    for idx, val in enumerate(cards):
        d = get_dispatch(page)
        if not d:
            print(f"  牌 #{idx+1}: 無 dispatch，停止")
            break

        ci = d.get("cardIndex", 0)
        who = d.get("who", 0)
        vis = d.get("visible", 1)

        print(f"  牌 #{idx+1}: ci={ci} → scanNextCard({val}) [{card_display(val)}]")

        # 嘗試不同的呼叫方式
        ret = js(page, f"""
            var ret = {{}};
            try {{
                // 方式 A: scanNextCard(cardValue)
                var r = s.scanNextCard({val});
                ret.a = r === undefined ? 'undef' : JSON.stringify(r).substring(0, 200);
            }} catch(e) {{
                ret.a_err = e.message;
            }}
            ret.ci_after = s.dispatchCardResp ? (s.dispatchCardResp.cardIndex || s.dispatchCardResp.cardindex || 0) : -1;
            ret.resultCards = s.resultCards ? Array.from(s.resultCards) : null;
            return ret;
        """)
        print(f"    回傳: {ret}")

        page.wait_for_timeout(2000)

        # 檢查 ci 是否推進
        d2 = get_dispatch(page)
        ci2 = d2.get("cardIndex", 0) if d2 else -1
        print(f"    ci: {ci} → {ci2} ({'推進' if ci2 > ci else '未推進'})")

        sent += 1
        if ci >= 6:
            break

    page.wait_for_timeout(3000)
    rc = get_result_cards(page)
    print(f"\n  結果: {rc}")

    has_nonzero = rc and rc.get("resultCards") and any(v != 0 for v in rc["resultCards"])
    return {
        "method": "scanNextCard",
        "sent": sent,
        "resultCards": rc.get("resultCards") if rc else None,
        "success": has_nonzero,
    }


def method_2_sendModifyCard(page, cards):
    """方法 2: sendModifyCard — 先用原始 sendNextCard 送，再用 sendModifyCard 覆蓋"""
    print("\n" + "─" * 50)
    print("  方法 2: sendModifyCard")
    print("─" * 50)

    d = wait_for_fresh_dispatch(page)
    if not d:
        return {"method": "sendModifyCard", "success": False, "reason": "no dispatch"}

    sent = 0

    for idx, val in enumerate(cards):
        d = get_dispatch(page)
        if not d:
            print(f"  牌 #{idx+1}: 無 dispatch，停止")
            break

        ci = d.get("cardIndex", 0)
        who = d.get("who", 0)
        vis = d.get("visible", 1)

        print(f"  牌 #{idx+1}: ci={ci}")

        # 先用 sendNextCard 送一張隨機牌（讓 ci 推進）
        dummy_val = 52  # K♦
        print(f"    step1: sendNextCard({dummy_val}) [dummy]")
        js(page, f"if (s.sendNextCard) s.sendNextCard({dummy_val},{ci},{vis},{who});")
        page.wait_for_timeout(2000)

        # 再用 sendModifyCard 覆蓋為正確牌值
        print(f"    step2: sendModifyCard({val}, {ci}) [{card_display(val)}]")
        ret = js(page, f"""
            var ret = {{}};
            try {{
                var r = s.sendModifyCard({val}, {ci});
                ret.result = r === undefined ? 'undef' : JSON.stringify(r).substring(0, 200);
            }} catch(e) {{
                ret.err = e.message;
            }}
            try {{
                // 也試帶更多參數
                var r2 = s.sendModifyCard({val}, {ci}, {vis}, {who});
                ret.result2 = r2 === undefined ? 'undef' : JSON.stringify(r2).substring(0, 200);
            }} catch(e2) {{
                ret.err2 = e2.message;
            }}
            ret.resultCards = s.resultCards ? Array.from(s.resultCards) : null;
            return ret;
        """)
        print(f"    回傳: {ret}")

        page.wait_for_timeout(2000)
        sent += 1
        if ci >= 6:
            break

    page.wait_for_timeout(3000)
    rc = get_result_cards(page)
    print(f"\n  結果: {rc}")

    has_nonzero = rc and rc.get("resultCards") and any(v != 0 for v in rc["resultCards"])
    return {
        "method": "sendModifyCard",
        "sent": sent,
        "resultCards": rc.get("resultCards") if rc else None,
        "success": has_nonzero,
    }


def method_3_manulScanBurnCard(page, cards):
    """方法 3: manulScanBurnCard — 手動掃描燒牌（可能需要不同流程）"""
    print("\n" + "─" * 50)
    print("  方法 3: manulScanBurnCard")
    print("─" * 50)

    d = wait_for_fresh_dispatch(page)
    if not d:
        return {"method": "manulScanBurnCard", "success": False, "reason": "no dispatch"}

    sent = 0

    for idx, val in enumerate(cards):
        d = get_dispatch(page)
        if not d:
            break

        ci = d.get("cardIndex", 0)
        who = d.get("who", 0)
        vis = d.get("visible", 1)

        print(f"  牌 #{idx+1}: ci={ci} → manulScanBurnCard({val}) [{card_display(val)}]")

        ret = js(page, f"""
            var ret = {{}};
            try {{
                var r = s.manulScanBurnCard({val});
                ret.a = r === undefined ? 'undef' : JSON.stringify(r).substring(0, 200);
            }} catch(e) {{
                ret.a_err = e.message;
            }}
            // 也嘗試帶 cardIndex
            try {{
                var r2 = s.manulScanBurnCard({val}, {ci});
                ret.b = r2 === undefined ? 'undef' : JSON.stringify(r2).substring(0, 200);
            }} catch(e2) {{
                ret.b_err = e2.message;
            }}
            ret.ci_after = s.dispatchCardResp ? (s.dispatchCardResp.cardIndex || 0) : -1;
            ret.resultCards = s.resultCards ? Array.from(s.resultCards) : null;
            ret.burnCardList = s.burnCardList ? JSON.stringify(s.burnCardList).substring(0, 200) : null;
            return ret;
        """)
        print(f"    回傳: {ret}")

        page.wait_for_timeout(2000)
        sent += 1
        if ci >= 6:
            break

    page.wait_for_timeout(3000)
    rc = get_result_cards(page)
    print(f"\n  結果: {rc}")

    has_nonzero = rc and rc.get("resultCards") and any(v != 0 for v in rc["resultCards"])
    return {
        "method": "manulScanBurnCard",
        "sent": sent,
        "resultCards": rc.get("resultCards") if rc else None,
        "success": has_nonzero,
    }


def method_4_proto_construct(page, cards):
    """方法 4: 手動建構 Proto 格式 + writeBytes 直送 WebSocket"""
    print("\n" + "─" * 50)
    print("  方法 4: Proto/APIManager 直送")
    print("─" * 50)

    d = wait_for_fresh_dispatch(page)
    if not d:
        return {"method": "proto_construct", "success": False, "reason": "no dispatch"}

    sent = 0

    for idx, val in enumerate(cards):
        d = get_dispatch(page)
        if not d:
            break

        ci = d.get("cardIndex", 0)
        who = d.get("who", 0)
        vis = d.get("visible", 1)

        print(f"  牌 #{idx+1}: ci={ci}")

        # 方式 A: 嘗試透過 sendNextCardProto (即使探測說不存在，某些 store 路徑可能有)
        # 方式 B: 直接呼叫 APIManager.sendCMDNewCard + socket.writeBytes
        # 方式 C: 嘗試 addScannedCard + sendNextCard 組合
        ret = js(page, f"""
            var ret = {{}};

            // 方式 A: sendNextCardProto
            try {{
                if (typeof s.sendNextCardProto === 'function') {{
                    var r = s.sendNextCardProto([{{cardindex:{ci},val:{val},handindex:0}}]);
                    ret.proto = r === undefined ? 'undef' : JSON.stringify(r).substring(0, 200);
                }} else {{
                    ret.proto = 'not_exist';
                }}
            }} catch(e) {{
                ret.proto_err = e.message;
            }}

            // 方式 B: addScannedCard 先登記 + sendNextCard
            try {{
                if (typeof s.addScannedCard === 'function') {{
                    s.addScannedCard({val});
                    ret.addScanned = 'ok';
                }}
            }} catch(e) {{
                ret.addScanned_err = e.message;
            }}
            try {{
                if (typeof s.sendNextCard === 'function') {{
                    s.sendNextCard({val},{ci},{vis},{who});
                    ret.sendAfterAdd = 'ok';
                }}
            }} catch(e) {{
                ret.sendAfterAdd_err = e.message;
            }}

            // 方式 C: 直接寫 scannedCards 字典再 sendNextCard
            try {{
                if (s.scannedCards) {{
                    s.scannedCards[{ci}] = {val};
                    ret.directWrite = 'ok';
                }}
            }} catch(e) {{
                ret.directWrite_err = e.message;
            }}

            page_wait = 500;
            ret.ci_after = s.dispatchCardResp ? (s.dispatchCardResp.cardIndex || 0) : -1;
            ret.resultCards = s.resultCards ? Array.from(s.resultCards) : null;
            ret.scannedCards = s.scannedCards ? JSON.stringify(s.scannedCards).substring(0, 300) : null;
            return ret;
        """)
        print(f"    回傳: {ret}")

        page.wait_for_timeout(3000)

        d2 = get_dispatch(page)
        ci2 = d2.get("cardIndex", 0) if d2 else -1
        print(f"    ci: {ci} → {ci2} ({'推進' if ci2 > ci else '未推進'})")

        sent += 1
        if ci >= 6:
            break

    page.wait_for_timeout(3000)
    rc = get_result_cards(page)
    print(f"\n  結果: {rc}")

    has_nonzero = rc and rc.get("resultCards") and any(v != 0 for v in rc["resultCards"])
    return {
        "method": "proto_construct",
        "sent": sent,
        "resultCards": rc.get("resultCards") if rc else None,
        "success": has_nonzero,
    }


# ================================================================
# 主程式
# ================================================================

def close_and_reset(page):
    """closeRound + 等待 gs=0"""
    print("\n  重置房間狀態...", end="", flush=True)
    js(page, "if (s.dealerCloseRound) s.dealerCloseRound();")
    page.wait_for_timeout(5000)
    js(page, "if (s.dealerCloseRound) s.dealerCloseRound();")
    page.wait_for_timeout(3000)
    gs = get_gs(page)
    print(f" gs={gs}")


def run(vid, headed, dealer_id, methods_to_test):
    from playwright.sync_api import sync_playwright

    url = build_dealer_url(vid)

    print("=" * 60)
    print("  BAC 替代送牌方法診斷")
    print("=" * 60)
    print(f"  房間: {vid}")
    print(f"  URL:  {url}")
    print(f"  測試方法: {methods_to_test}")
    print(f"  已知牌序: {' '.join(card_display(c) for c in KNOWN_CARDS)}")
    print(f"  牌值:     {KNOWN_CARDS}")
    print()

    monitor = SHBConsoleMonitor()
    console = FullConsoleCapture()

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=not headed)
        ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = ctx.new_page()
        page.route("**/*nanocosmos*", lambda route: route.abort())
        page.route("**/*h5live*", lambda route: route.abort())
        page.on("console", monitor.on_console)
        page.on("console", console.on_console)

        def _dismiss(d):
            try:
                d.accept()
            except Exception:
                pass
        page.on("dialog", _dismiss)

        # ── 載入 + 登入 ──
        print("[載入] Dealer Tool...", end="", flush=True)
        try:
            page.goto(url, wait_until="networkidle", timeout=60000)
        except Exception:
            pass
        page.wait_for_timeout(10000)
        print(" OK")

        print(f"[登入] ID={dealer_id}...", end="", flush=True)
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
            page.wait_for_timeout(5000)
            gs = get_gs(page)
            if gs is not None and gs >= 0:
                print(f" OK (gs={gs})")
            else:
                print(f" FAIL")
                browser.close()
                return
        page.wait_for_timeout(3000)

        # ── 探測函數簽名 ──
        print("\n[探測] 方法簽名...")
        sigs = probe_method_signatures(page)
        if sigs:
            for name in ["scanNextCard", "sendModifyCard", "manulScanBurnCard", "sendNextCardProto", "sendNextCard"]:
                info = sigs.get(name, {})
                if info.get("exists"):
                    print(f"  {name}({info.get('len', '?')} params):")
                    src = info.get("src", "")
                    # 印出前 3 行
                    for line in src.split("\n")[:3]:
                        print(f"    {line.strip()}")
                else:
                    print(f"  {name}: 不存在")
            if sigs.get("apiCardMethods"):
                print(f"\n  APIManager card 相關: {sigs['apiCardMethods']}")
        print()

        # ── 等待房間穩定（自動開牌房需等完當前局）──
        print("[等待] 房間穩定...", end="", flush=True)
        for t in range(30):
            gs = get_gs(page)
            if gs == 0:
                print(f" gs=0 閒置 ({t+1}s)")
                break
            if gs == 2:
                if t % 5 == 0:
                    js(page, "if (s.dealerCloseRound) s.dealerCloseRound();")
                    print(f" close(gs=2)", end="", flush=True)
            if gs == 1:
                print(f" 倒數中(gs=1)", end="", flush=True)
            page.wait_for_timeout(1000)
        else:
            gs = get_gs(page)
            print(f" 超時 gs={gs}")

        # ── 依序測試每種方法 ──
        results = []
        method_funcs = {
            1: ("scanNextCard", method_1_scanNextCard),
            2: ("sendModifyCard", method_2_sendModifyCard),
            3: ("manulScanBurnCard", method_3_manulScanBurnCard),
            4: ("proto_construct", method_4_proto_construct),
        }

        for m_id in methods_to_test:
            name, func = method_funcs[m_id]
            console.clear()

            try:
                result = func(page, KNOWN_CARDS)
            except Exception as e:
                result = {"method": name, "success": False, "error": str(e)}
                print(f"  [ERROR] {e}")

            results.append(result)

            # 印出此方法期間的關鍵 console
            msgs = console.dump()
            card_msgs = [m for _, m in msgs if any(kw in m.lower() for kw in ['card', 'send', 'scan', 'result', 'new_card'])]
            if card_msgs:
                print(f"\n  Console 關鍵訊息:")
                for m in card_msgs[:10]:
                    print(f"    {m[:200]}")

            # closeRound 重置
            close_and_reset(page)

        # ── 總結 ──
        print()
        print("=" * 60)
        print("  測試總結")
        print("=" * 60)
        for r in results:
            status = "✓ 成功" if r.get("success") else "✗ 失敗"
            rc = r.get("resultCards", [])
            print(f"  方法 {r['method']:25s} {status}  resultCards={rc}")

        success_methods = [r["method"] for r in results if r.get("success")]
        if success_methods:
            print(f"\n  可行方法: {', '.join(success_methods)}")
        else:
            print(f"\n  所有方法均失敗。可能需要 Canvas 座標點擊方案。")

        # 如果 headed，保持開啟
        if headed:
            print("\n  [headed] 保持 15 秒供觀察...")
            page.wait_for_timeout(15000)

        browser.close()

    # 寫報告
    report = {
        "timestamp": datetime.now().isoformat(),
        "vid": vid,
        "methods_tested": methods_to_test,
        "signatures": sigs,
        "results": results,
        "success_methods": success_methods,
    }
    report_path = PROJECT_ROOT / "shared" / "report" / "bac_verify" / f"diag_methods_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    print(f"\n  診斷報告: {report_path}")


def main():
    parser = argparse.ArgumentParser(description="BAC 替代送牌方法診斷")
    parser.add_argument("--vid", default="N011", help="房間 ID")
    parser.add_argument("--headed", action="store_true", help="顯示瀏覽器")
    parser.add_argument("--dealer-id", default="8232", help="Dealer ID")
    parser.add_argument("--method", default="1,2,3,4", help="要測試的方法 (如 1,2,3,4 或 1)")
    args = parser.parse_args()

    methods = [int(m.strip()) for m in args.method.split(",") if m.strip()]
    run(args.vid, args.headed, args.dealer_id, methods)


if __name__ == "__main__":
    main()
