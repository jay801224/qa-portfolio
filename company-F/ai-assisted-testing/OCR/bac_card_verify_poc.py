"""
bac_card_verify_poc.py — 百家樂牌面驗證 POC

Phase 1 目標:
  1. 透過 api_login 取得 UAT game URL
  2. 進入百家樂房間
  3. 監聽 WebSocket frame，嘗試解碼提取牌面資料
  4. 在結算時截取 Canvas 畫面
  5. 輸出 WS frame 分析報告

用法:
  python bac_card_verify_poc.py                    # UAT <ACCOUNT> CNY 預設
  python bac_card_verify_poc.py --env qa           # QA 環境
  python bac_card_verify_poc.py --rounds 5         # 觀察 5 局
  python bac_card_verify_poc.py --headed           # 顯示瀏覽器
  python bac_card_verify_poc.py --url "已有URL"    # 跳過登入
"""

import argparse
import io
import json
import os
import re
import sys
import time
import zlib
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

# ── 專案內模組 ──────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from api_login import get_game_url as api_get_game_url
from get_login_link import get_game_url as pw_get_game_url
from react_client_selectors import (
    LOBBY_MENU, TAB_ICON_BUTTON, GAME_CARD_READY,
    GAME_CARD_CLICK, GAME_ROOM_READY, COUNTDOWN_EL,
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── 輸出目錄 ────────────────────────────────────────────────────────────────
HERE = Path(__file__).parent
SCREENSHOT_DIR = HERE / "screenshots" / "bac_verify_poc"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

# ── 牌值工具（複用 qa_auto_dealer 邏輯）────────────────────────────────────
SUIT_NAMES = {1: "♠", 2: "♥", 3: "♣", 4: "♦"}
FACE_NAMES = {1: "A", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7",
              8: "8", 9: "9", 10: "10", 11: "J", 12: "Q", 13: "K"}


def decode_card(value):
    """cardValue 1-52 → (face, suit) tuple"""
    face = (value - 1) // 4 + 1
    suit = (value - 1) % 4 + 1
    return face, suit


def card_display(value):
    """cardValue → 顯示字串如 'A♠', '6♥'"""
    face, suit = decode_card(value)
    return f"{FACE_NAMES.get(face, '?')}{SUIT_NAMES.get(suit, '?')}"


def bac_point(face):
    """百家樂點數：A=1, 2-9=面值, 10/J/Q/K=0"""
    if face >= 10:
        return 0
    return face


# ── WS Frame 收集器 ─────────────────────────────────────────────────────────
class WsFrameCollector:
    """收集所有 WS frame，嘗試解碼並提取牌面相關資料"""

    def __init__(self):
        self.raw_frames = []          # 所有原始 frame
        self.decoded_frames = []      # 成功解碼的 frame
        self.card_events = []         # 識別出的牌面事件
        self.ws_urls = []

    def attach(self, page):
        page.on("websocket", self._on_ws)

    def _on_ws(self, ws):
        url = ws.url
        self.ws_urls.append(url)
        print(f"  [WS] 連線建立: {url[:80]}...")
        ws.on("framereceived", lambda payload: self._on_frame(payload, "received", url))
        ws.on("framesent", lambda payload: self._on_frame(payload, "sent", url))
        ws.on("close", lambda: print(f"  [WS] 連線關閉: {url[:80]}..."))

    def _on_frame(self, payload, direction, ws_url):
        ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        frame_info = {
            "ts": ts,
            "direction": direction,
            "ws_url": ws_url[:60],
            "raw_type": type(payload).__name__,
            "raw_len": len(payload) if payload else 0,
        }

        # 嘗試多種解碼
        decoded_text = self._try_decode(payload)
        if decoded_text:
            frame_info["decoded"] = decoded_text[:500]
            self.decoded_frames.append(frame_info)

            # 搜尋牌面相關關鍵字
            card_keywords = [
                "card", "Card", "dispatch", "Dispatch",
                "sendNext", "result", "Result",
                "close", "Close", "round", "Round",
                "point", "Point", "banker", "player",
                "Banker", "Player", "deal", "Deal",
            ]
            text_lower = decoded_text.lower()
            matched = [kw for kw in card_keywords if kw.lower() in text_lower]
            if matched:
                frame_info["card_keywords"] = matched
                self.card_events.append(frame_info)
                print(f"  [WS-CARD] {ts} {direction} 關鍵字={matched} len={frame_info['raw_len']}")

        self.raw_frames.append(frame_info)

    def _try_decode(self, payload):
        """嘗試多種方式解碼 WS frame"""
        if isinstance(payload, str):
            return payload

        if isinstance(payload, bytes):
            # 1. 直接 UTF-8
            try:
                text = payload.decode("utf-8")
                if text.isprintable() or len(text) > 10:
                    return text
            except (UnicodeDecodeError, ValueError):
                pass

            # 2. JSON
            try:
                obj = json.loads(payload)
                return json.dumps(obj, ensure_ascii=False)
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass

            # 3. zlib decompress + UTF-8
            try:
                decompressed = zlib.decompress(payload)
                text = decompressed.decode("utf-8")
                return text
            except (zlib.error, UnicodeDecodeError):
                pass

            # 4. zlib decompress + JSON
            try:
                decompressed = zlib.decompress(payload)
                obj = json.loads(decompressed)
                return json.dumps(obj, ensure_ascii=False)
            except (zlib.error, json.JSONDecodeError, UnicodeDecodeError):
                pass

            # 5. msgpack
            try:
                import msgpack
                obj = msgpack.unpackb(payload, raw=False)
                return json.dumps(obj, ensure_ascii=False, default=str)
            except Exception:
                pass

            # 6. 從 binary 中提取可讀字串片段
            try:
                readable = re.findall(rb'[\x20-\x7e]{4,}', payload)
                if readable:
                    return " | ".join(s.decode("ascii") for s in readable[:10])
            except Exception:
                pass

            # 7. hex dump（前 100 bytes）
            return f"[binary {len(payload)}B] {payload[:100].hex()}"

        return None

    def summary(self):
        """輸出統計摘要"""
        lines = [
            f"WS 連線數: {len(self.ws_urls)}",
            f"總 frame 數: {len(self.raw_frames)}",
            f"  sent: {sum(1 for f in self.raw_frames if f['direction'] == 'sent')}",
            f"  received: {sum(1 for f in self.raw_frames if f['direction'] == 'received')}",
            f"成功解碼: {len(self.decoded_frames)}",
            f"牌面相關: {len(self.card_events)}",
        ]
        return "\n".join(lines)


# ── 主流程 ──────────────────────────────────────────────────────────────────

def get_countdown_text(page):
    """取得倒數計時器文字"""
    try:
        return page.evaluate(f"""() => {{
            const el = document.querySelector('{COUNTDOWN_EL}');
            return el ? (el.textContent || '').trim() : '';
        }}""")
    except Exception:
        return ""


def is_settling(text):
    """判斷是否為結算狀態"""
    settling_keywords = ["開牌中", "开牌中", "結算中", "结算中", "Dealing", "Settling"]
    return any(kw in text for kw in settling_keywords)


def is_betting(text):
    """判斷是否為下注階段（倒數數字）"""
    return text.isdigit() and int(text) > 0


def enumerate_media_elements(page):
    """列出所有 canvas / video 元素資訊"""
    info = page.evaluate("""() => {
        const result = {canvases:[], videos:[]};
        document.querySelectorAll('canvas').forEach((c, i) => {
            const r = c.getBoundingClientRect();
            result.canvases.push({
                idx: i, w: Math.round(r.width), h: Math.round(r.height),
                id: example.internal || '', cls: (c.className || '').substring(0, 60),
                visible: r.width > 10 && r.height > 10
            });
        });
        document.querySelectorAll('video').forEach((v, i) => {
            const r = v.getBoundingClientRect();
            result.videos.push({
                idx: i, w: Math.round(r.width), h: Math.round(r.height),
                src: (v.src || '').substring(0, 80), id: example.internal || '',
                visible: r.width > 10 && r.height > 10
            });
        });
        return result;
    }""")
    return info


def take_game_screenshot(page, label):
    """截取遊戲畫面 — 全頁 + 最大 Canvas + Video"""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    paths = []

    # 1. 全頁截圖（最重要 — 包含視訊 + 開牌動畫 + 下注區）
    try:
        fp = SCREENSHOT_DIR / f"fullpage_{label}_{ts}.png"
        page.screenshot(path=str(fp), full_page=False, animations="disabled")
        print(f"  [截圖] 全頁: {fp.name}")
        paths.append(str(fp))
    except Exception as e:
        print(f"  [截圖] 全頁失敗: {e}")

    # 2. 列出所有 canvas / video
    media = enumerate_media_elements(page)
    if media["canvases"]:
        visible = [c for c in media["canvases"] if c["visible"]]
        print(f"  [媒體] Canvas: {len(media['canvases'])} 個 (可見 {len(visible)})")
        for c in visible:
            print(f"    canvas[{c['idx']}] {c['w']}x{c['h']} id={c['id']!r} cls={c['cls']!r}")
    if media["videos"]:
        visible = [v for v in media["videos"] if v["visible"]]
        print(f"  [媒體] Video: {len(media['videos'])} 個 (可見 {len(visible)})")
        for v in visible:
            print(f"    video[{v['idx']}] {v['w']}x{v['h']} src={v['src']!r}")

    # 3. 截取最大的 Canvas
    canvases = page.locator("canvas").all()
    largest_area = 0
    largest_idx = -1
    for i, c in enumerate(canvases):
        try:
            if c.is_visible(timeout=1000):
                box = c.bounding_box()
                if box:
                    area = box["width"] * box["height"]
                    if area > largest_area:
                        largest_area = area
                        largest_idx = i
        except Exception:
            pass

    if largest_idx >= 0:
        try:
            shot = canvases[largest_idx].screenshot(timeout=8000)
            box = canvases[largest_idx].bounding_box()
            cp = SCREENSHOT_DIR / f"canvas_largest_{label}_{ts}.png"
            cp.write_bytes(shot)
            print(f"  [截圖] 最大 Canvas[{largest_idx}] "
                  f"{int(box['width'])}x{int(box['height'])}: {cp.name}")
            paths.append(str(cp))
        except Exception as e:
            print(f"  [截圖] 最大 Canvas 截圖失敗: {e}")

    # 4. 截取每個可見 Canvas（供分析）
    for i, c in enumerate(canvases):
        if i == largest_idx:
            continue
        try:
            if c.is_visible(timeout=500):
                box = c.bounding_box()
                if box and box["width"] > 30 and box["height"] > 30:
                    shot = c.screenshot(timeout=5000)
                    cp = SCREENSHOT_DIR / f"canvas_{i}_{int(box['width'])}x{int(box['height'])}_{label}_{ts}.png"
                    cp.write_bytes(shot)
                    paths.append(str(cp))
        except Exception:
            pass

    # 5. 截取 Video 元素（如果有）
    videos = page.locator("video").all()
    for i, v in enumerate(videos):
        try:
            if v.is_visible(timeout=500):
                box = v.bounding_box()
                if box and box["width"] > 30:
                    shot = v.screenshot(timeout=5000)
                    vp = SCREENSHOT_DIR / f"video_{i}_{int(box['width'])}x{int(box['height'])}_{label}_{ts}.png"
                    vp.write_bytes(shot)
                    print(f"  [截圖] Video[{i}] {int(box['width'])}x{int(box['height'])}: {vp.name}")
                    paths.append(str(vp))
        except Exception:
            pass

    return paths


def wait_loading_gone(page, timeout=30000):
    """等待 loading overlay 消失"""
    try:
        page.wait_for_function("""() => {
            const lp = document.getElementById('loading-page');
            if (!lp) return true;
            const style = window.getComputedStyle(lp);
            return style.display === 'none' || style.opacity === '0' || style.visibility === 'hidden';
        }""", timeout=timeout)
        print("  [載入] loading overlay 已消失")
    except Exception:
        print("  [載入] loading overlay 仍在，嘗試繼續...")


def js_click(page, el):
    """用 JS dispatchEvent 點擊（繞過 overlay 攔截）"""
    page.evaluate("""(el) => {
        const rect = el.getBoundingClientRect();
        const x = rect.left + rect.width / 2;
        const y = example.internal + rect.height / 2;
        const opts = {bubbles:true, cancelable:true, view:window, clientX:x, clientY:y, button:0};
        el.dispatchEvent(new PointerEvent('pointerdown', {...opts, pointerId:1, pointerType:'mouse'}));
        el.dispatchEvent(new MouseEvent('mousedown', opts));
        el.dispatchEvent(new PointerEvent('pointerup', {...opts, pointerId:1, pointerType:'mouse'}));
        el.dispatchEvent(new MouseEvent('mouseup', opts));
        el.dispatchEvent(new MouseEvent('click', opts));
    }""", el)


def check_session_expired(page):
    """檢查是否出現 TSS 過期提示"""
    try:
        body = page.evaluate("() => document.body.innerText || ''")
        expired_kw = ["帳號登錄已過期", "帐号登录已过期", "Login expired",
                      "session expired", "登錄已過期", "登录已过期"]
        for kw in expired_kw:
            if kw in body:
                return True
    except Exception:
        pass
    return False


def handle_entry_page(page, context):
    """處理 Latest Entry 版本選擇頁面（點 Go to Latest Entry）"""
    btn = page.get_by_text("Go to Latest Entry", exact=False)
    if btn.count() == 0:
        return None

    print("[Entry] 偵測到版本選擇頁面，點擊 Go to Latest Entry...")
    pages_before = len(context.pages)

    try:
        with context.expect_page(timeout=15000) as new_page_info:
            btn.first.click(timeout=5000)
        new_page = new_page_info.value
        new_page.wait_for_load_state("domcontentloaded", timeout=30000)
        print(f"[Entry] 新分頁已開啟: {new_page.url[:80]}...")
        return new_page
    except Exception as e:
        print(f"[Entry] expect_page 未觸發: {e}")

    # fallback: 檢查是否有比之前多出的分頁
    page.wait_for_timeout(5000)
    if len(context.pages) > pages_before:
        new_page = context.pages[-1]
        try:
            new_page.wait_for_load_state("domcontentloaded", timeout=15000)
        except Exception:
            pass
        print(f"[Entry] 找到新分頁（fallback）: {new_page.url[:80]}...")
        return new_page

    # fallback2: 同頁導航
    print("[Entry] 嘗試同頁導航")
    page.wait_for_timeout(3000)
    return page


def enter_bac_room(page, context):
    """進入百家樂房間（找有倒數的房間）"""
    # 等頁面 React 渲染
    print("[頁面] 等待 React 渲染...")
    try:
        page.wait_for_function(
            "() => document.querySelector('#root')?.children.length > 0",
            timeout=15000,
        )
    except Exception:
        print("[頁面] React 渲染緩慢，繼續...")
    page.wait_for_timeout(2000)

    # 檢查是否在 Latest Entry / Entries 頁面
    body_text = page.evaluate("() => (document.body.innerText || '').substring(0, 1000)") or ""
    if "Latest Entry" in body_text or "Go to Latest Entry" in body_text or "Entries" in body_text:
        print("[Entry] 偵測到版本選擇頁面")
        new_page = handle_entry_page(page, context)
        if new_page and new_page != page:
            page = new_page
            # 新頁面也需要等 React 載入
            try:
                page.wait_for_function(
                    "() => document.querySelector('#root')?.children.length > 0",
                    timeout=15000,
                )
            except Exception:
                pass
            page.wait_for_timeout(2000)
        elif not new_page:
            print("[Entry] 無法通過版本選擇頁面")
            return False, page

    # 等大廳載入
    print("[大廳] 等待載入...")
    try:
        page.wait_for_selector(LOBBY_MENU, timeout=30000)
    except Exception:
        # 可能已在遊戲室中
        try:
            page.wait_for_selector(GAME_ROOM_READY, timeout=5000)
            print("[大廳] 似乎已在遊戲室中")
            return True, page
        except Exception:
            # 可能 TSS 過期
            if check_session_expired(page):
                print("[大廳] TSS 已過期！")
                return "expired", page
            print("[大廳] 載入失敗")
            return False, page

    # 等 loading overlay 消失（縮短等待）
    wait_loading_gone(page, timeout=10000)

    print("[大廳] 已載入，尋找百家樂分頁...")

    # 點百家樂分頁（用 JS click 繞過可能的 overlay）
    tabs = page.query_selector_all(TAB_ICON_BUTTON)
    bac_tab = None
    for tab in tabs:
        text = tab.text_content() or ""
        if "百家" in text or "Baccarat" in text.lower():
            bac_tab = tab
            break

    if bac_tab:
        js_click(page, bac_tab)
        print("[大廳] 已點擊百家樂分頁")
        page.wait_for_timeout(1500)
    else:
        print("[大廳] 找不到百家樂分頁，嘗試直接找房間卡...")

    # 等房間卡出現
    try:
        page.wait_for_selector(GAME_CARD_READY, timeout=8000)
    except Exception:
        if check_session_expired(page):
            return "expired", page
        print("[大廳] 房間卡未出現")
        return False, page

    # 嘗試點擊第一個可用的百家樂房間
    cards = page.query_selector_all(GAME_CARD_CLICK)
    if not cards:
        print("[大廳] 找不到房間卡點擊區域")
        return False, page

    print(f"[大廳] 找到 {len(cards)} 個房間卡，點擊第一個...")
    js_click(page, cards[0])
    page.wait_for_timeout(2000)

    # 等遊戲室載入
    try:
        page.wait_for_selector(GAME_ROOM_READY, timeout=15000)
        print("[遊戲室] 已載入")
        return True, page
    except Exception:
        if check_session_expired(page):
            return "expired", page
        print("[遊戲室] 載入超時")
        return False, page


def run_poc(env, pid, currency, rounds, headed, url):
    """POC 主流程"""
    print("=" * 60)
    print("百家樂牌面驗證 POC — Phase 1: WS 攔截 + Canvas 截圖")
    print("=" * 60)

    # 取得 game URL — 優先使用 Loading Page（example.internal），fallback 到 API
    if not url:
        print(f"\n[登入] 取得 {env.upper()} / {pid} / {currency.upper()} game URL...")
        print(f"  策略: Loading Page 優先 → API fallback")
        url = pw_get_game_url(pid=pid, currency=currency, env=env,
                              strategy="loading-page", headless=True)
        if not url:
            print("[登入] Loading Page 失敗，嘗試 API 登入...")
            url = api_get_game_url(env, pid, currency)
        if not url:
            print("[登入] 所有登入方式均失敗")
            return
        print(f"[登入] 成功")

    print(f"[URL] {url[:100]}...")

    # 啟動 Playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=not headed)
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            locale="zh-TW",
        )
        page = context.new_page()

        # 掛載 WS 監聽
        collector = WsFrameCollector()
        collector.attach(page)

        # 進入大廳 + 房間（含 TSS 過期重試）
        max_retries = 3
        for attempt in range(1, max_retries + 1):
            if attempt > 1:
                # 重新取 URL
                print(f"\n[重試 {attempt}/{max_retries}] 重新取得 game URL...")
                url = pw_get_game_url(pid=pid, currency=currency, env=env,
                                      strategy="loading-page", headless=True)
                if not url:
                    url = api_get_game_url(env, pid, currency)
                if not url:
                    print("[登入] 重試登入失敗")
                    browser.close()
                    return
                print(f"[登入] 重新取得成功")

            print(f"\n[瀏覽器] 開啟頁面 (嘗試 {attempt})...")
            page.goto(url, timeout=30000, wait_until="domcontentloaded")

            result, page = enter_bac_room(page, context)
            # 新分頁開啟時需重新掛載 WS 監聽
            collector.attach(page)
            if result == "expired":
                print(f"[TSS] 過期，將重試...")
                continue
            elif result:
                break
            else:
                print("[錯誤] 進房失敗（非過期問題）")
                take_game_screenshot(page, "lobby_fail")
                browser.close()
                return
        else:
            print(f"[錯誤] {max_retries} 次重試均失敗")
            take_game_screenshot(page, "lobby_fail_final")
            browser.close()
            return

        # ── 多局觀察：三段連拍策略 ──────────────────────────────
        print(f"\n[監控] 開始觀察 {rounds} 局...")
        round_count = 0
        prev_state = ""
        round_frames = {}  # {round_num: {"burst": [...], "settle": path, "catchup": path}}
        start_time = time.time()
        video_loc = page.locator("video").first

        def burst_video(label):
            """快速截取 Video 元素，回傳 (path, bytes)"""
            ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            try:
                shot = video_loc.screenshot(timeout=3000)
                p = SCREENSHOT_DIR / f"v_{label}_{ts}.png"
                p.write_bytes(shot)
                return str(p)
            except Exception:
                return None

        while round_count < rounds and (time.time() - start_time) < 600:
            text = get_countdown_text(page)

            if text != prev_state:
                elapsed_min = (time.time() - start_time) / 60

                # ── 階段 A：進入開牌 → 0.5 秒連拍 ──
                if is_settling(text) and not is_settling(prev_state):
                    round_count += 1
                    print(f"  [{elapsed_min:.1f}m] [局 {round_count}/{rounds}] "
                          f"'{text}' — 開始連拍...")
                    frames = []
                    for i in range(20):  # 最多 10 秒
                        p = burst_video(f"r{round_count}_burst{i:02d}")
                        if p:
                            frames.append(p)
                        cur = get_countdown_text(page)
                        # 結算中 → 進入階段 B
                        if cur != text and not is_settling(cur):
                            break
                        page.wait_for_timeout(500)

                    round_frames[round_count] = {"burst": frames}
                    print(f"    連拍 {len(frames)} 幀")

                # ── 階段 B：結算中 → 截一張 ──
                if "结算" in text and "开牌" in (prev_state or ""):
                    p = burst_video(f"r{round_count}_settle")
                    if p and round_count in round_frames:
                        round_frames[round_count]["settle"] = p
                    print(f"  [{elapsed_min:.1f}m] 結算截圖")

                # ── 階段 C：結算→下注過渡期 → 補截（影像追齊）──
                if is_betting(text) and is_settling(prev_state):
                    # 立即補截一張 + 2 秒後再補一張
                    p1 = burst_video(f"r{round_count}_catchup0")
                    page.wait_for_timeout(2000)
                    p2 = burst_video(f"r{round_count}_catchup1")
                    if round_count in round_frames:
                        round_frames[round_count]["catchup"] = [
                            x for x in [p1, p2] if x]
                    print(f"  [{elapsed_min:.1f}m] [下注] 倒數 {text}s — "
                          f"過渡期補截 {sum(1 for x in [p1,p2] if x)} 張")

                prev_state = text

            page.wait_for_timeout(300)

        # 統計
        total_frames = sum(
            len(v.get("burst", [])) + (1 if v.get("settle") else 0) + len(v.get("catchup", []))
            for v in round_frames.values()
        )
        print(f"\n[完成] 觀察 {round_count} 局，共 {total_frames} 張截圖，"
              f"耗時 {time.time() - start_time:.0f} 秒")
        for rn, rv in round_frames.items():
            print(f"  局 {rn}: 連拍 {len(rv.get('burst',[]))} + "
                  f"結算 {1 if rv.get('settle') else 0} + "
                  f"補截 {len(rv.get('catchup',[]))}")

        elapsed = time.time() - start_time
        print(f"\n[完成] 觀察 {round_count} 局，耗時 {elapsed:.0f} 秒")

        # 輸出 WS 分析報告
        print("\n" + "=" * 60)
        print("WS Frame 分析報告")
        print("=" * 60)
        print(collector.summary())

        if collector.card_events:
            print(f"\n牌面相關 frame（共 {len(collector.card_events)} 筆）:")
            for i, evt in enumerate(collector.card_events[:30]):
                print(f"  [{i+1}] {evt['ts']} {evt['direction']} "
                      f"kw={evt.get('card_keywords', [])} "
                      f"len={evt['raw_len']}")
                if 'decoded' in evt:
                    print(f"       {evt['decoded'][:200]}")
        else:
            print("\n未偵測到牌面相關 frame")

        # 儲存完整 frame log
        log_path = SCREENSHOT_DIR / f"ws_frames_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        log_data = {
            "env": env,
            "pid": pid,
            "currency": currency,
            "rounds_observed": round_count,
            "elapsed_sec": round(elapsed, 1),
            "ws_urls": collector.ws_urls,
            "summary": {
                "total_frames": len(collector.raw_frames),
                "decoded_frames": len(collector.decoded_frames),
                "card_events": len(collector.card_events),
            },
            "card_events": collector.card_events[:50],
            "decoded_samples": collector.decoded_frames[:50],
            "round_frames": {str(k): v for k, v in round_frames.items()},
        }
        log_path.write_text(json.dumps(log_data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n[LOG] 完整 frame log: {log_path}")

        if screenshots:
            print(f"[截圖] 共 {len(screenshots)} 張截圖存於: {SCREENSHOT_DIR}")

        browser.close()


def main():
    ap = argparse.ArgumentParser(description="百家樂牌面驗證 POC")
    ap.add_argument("--env", default="uat", help="qa / uat")
    ap.add_argument("--pid", default="<ACCOUNT>", help="PID")
    ap.add_argument("--currency", default="cny", help="幣別")
    ap.add_argument("--rounds", type=int, default=3, help="觀察局數")
    ap.add_argument("--headed", action="store_true", help="顯示瀏覽器")
    ap.add_argument("--url", default="", help="直接使用已有 URL")
    args = ap.parse_args()

    run_poc(args.env, args.pid, args.currency, args.rounds, args.headed, args.url)


if __name__ == "__main__":
    main()
