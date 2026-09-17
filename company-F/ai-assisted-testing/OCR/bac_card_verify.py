"""
bac_card_verify.py — 百家樂牌面點數驗證主程式

流程: Loading Page 登入 → 進房 → 每局連拍 → Gemini 辨識 → JSON+HTML 報告

用法:
  python bac_card_verify.py                           # UAT, 3 局
  python bac_card_verify.py --rounds 10               # 10 局
  python bac_card_verify.py --headed                  # 顯示瀏覽器
  python bac_card_verify.py --gemini-limit 20         # Gemini 上限 20 次
  python bac_card_verify.py --skip-video-ocr          # 跳過影像層（省 Gemini）
  python bac_card_verify.py --retention-days 7        # 截圖保留 7 天
  python bac_card_verify.py --url "已有URL"           # 跳過登入
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta
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

from get_login_link import get_game_url as pw_get_game_url
from api_login import get_game_url as api_get_game_url
from react_client_selectors import LOBBY_MENU, COUNTDOWN_EL
from bac_frame_analyzer import (
    detect_round_info, find_best_frame, recognize_game, get_gemini_usage,
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── 遊戲設定 ──────────────────────────────────────────────────────────────
GAME_CONFIG = {
    "bac": {
        "name": "百家樂", "category": "百家樂", "default_room": "",
        "dealing_kw": ["开牌中", "開牌中", "结算中", "結算中", "Dealing", "Settling"],
    },
    "sic": {
        "name": "骰寶", "category": "骰寶", "default_room": "N026",
        "dealing_kw": ["开牌中", "開牌中", "结算中", "結算中", "摇骰中", "搖骰中", "Shaking", "Dealing"],
    },
    "ssic": {
        "name": "超倍骰寶", "category": "骰寶", "default_room": "P016",
        "dealing_kw": ["开牌中", "開牌中", "结算中", "結算中", "摇骰中", "搖骰中", "Shaking", "Dealing"],
    },
}

# ── 常數 ──────────────────────────────────────────────────────────────────
OUTPUT_DIR = PROJECT_ROOT / "shared" / "report" / "bac_verify"
SCREENSHOT_DIR = OUTPUT_DIR / "screenshots"


# ── 工具函式 ──────────────────────────────────────────────────────────────

def _ensure_dirs():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


def _get_countdown(page) -> str:
    try:
        return page.evaluate(f"""() => {{
            const el = document.querySelector('{COUNTDOWN_EL}');
            return el ? (el.textContent || '').trim() : '';
        }}""")
    except Exception:
        return ""


_current_game = "bac"  # 全域遊戲類型（由 run() 設定）

def _is_dealing(text: str) -> bool:
    kws = GAME_CONFIG.get(_current_game, GAME_CONFIG["bac"])["dealing_kw"]
    return any(kw in text for kw in kws)


def _is_betting(text: str) -> bool:
    return text.isdigit() and int(text) > 0


def _js_click(page, el):
    page.evaluate("""(el) => {
        const r = el.getBoundingClientRect();
        const x = r.left + r.width/2, y = example.internal + r.height/2;
        const o = {bubbles:true,cancelable:true,view:window,clientX:x,clientY:y,button:0};
        el.dispatchEvent(new PointerEvent('pointerdown',{...o,pointerId:1,pointerType:'mouse'}));
        el.dispatchEvent(new MouseEvent('mousedown',o));
        el.dispatchEvent(new PointerEvent('pointerup',{...o,pointerId:1,pointerType:'mouse'}));
        el.dispatchEvent(new MouseEvent('mouseup',o));
        el.dispatchEvent(new MouseEvent('click',o));
    }""", el)


def _check_expired(page) -> bool:
    try:
        body = page.evaluate("() => (document.body.innerText||'').substring(0,300)")
        return any(kw in body for kw in ["帳號登錄已過期", "帐号登录已过期", "session expired"])
    except Exception:
        return False


# ── 登入 ──────────────────────────────────────────────────────────────────

def get_login_url(env, pid, currency):
    """Loading Page 優先 → API fallback"""
    url = pw_get_game_url(pid=pid, currency=currency, env=env,
                          strategy="loading-page", headless=True)
    if not url:
        print("  Loading Page 失敗，嘗試 API...")
        url = api_get_game_url(env, pid, currency)
    return url or ""


# ── 進房 ──────────────────────────────────────────────────────────────────

def enter_game_room(page, context, category="百家樂", target_room=""):
    """Entry 頁面 → 大廳 → 進房。回傳 (success, page, version)。"""
    # 等 React
    try:
        page.wait_for_function(
            "()=>document.querySelector('#root')?.children.length>0", timeout=15000)
    except Exception:
        pass
    page.wait_for_timeout(2000)

    # Entry 頁面
    body = page.evaluate("()=>(document.body.innerText||'').substring(0,1000)")
    entry_version = ""
    ver_m = re.search(r"@pa/host\s+v[\d.]+", body)
    if ver_m:
        entry_version = ver_m.group(0)

    if "Go to Latest Entry" in body:
        try:
            page.get_by_text("Go to Latest Entry", exact=False).first.click(timeout=5000)
        except Exception:
            pass
        page.wait_for_timeout(8000)

    # 等大廳
    try:
        page.wait_for_selector(LOBBY_MENU, timeout=30000)
    except Exception:
        if _check_expired(page):
            return "expired", page, entry_version
        return False, page, entry_version

    page.wait_for_timeout(1000)

    # 點遊戲分頁
    kw = "百家" if "百家" in category else category[:2]
    for tab in page.query_selector_all('[class*="ItemInfo_icon_button"]'):
        if kw in (tab.text_content() or ""):
            _js_click(page, tab)
            break
    page.wait_for_timeout(2000)

    # 進房 — 指定房間或第一個
    cards = page.query_selector_all('[class*="GameCardFrame_click_area"]')
    if not cards:
        return False, page, entry_version

    target_card = cards[0]  # 預設第一個
    if target_room:
        # 嘗試找匹配 target_room 的房間卡
        all_frames = page.query_selector_all('[class*="GameCardFrame"]')
        for frame in all_frames:
            text = (frame.text_content() or "").replace(" ", "")
            # 零填充比對：D054→D54, N010→N10, N006→N6
            room_clean = re.sub(r'([A-Za-z])0+', r'\1', target_room).upper()
            if room_clean in text.upper() or target_room.upper() in text.upper():
                click_area = frame.query_selector('[class*="click_area"]')
                if click_area:
                    target_card = click_area
                    print(f"  找到指定房間 {target_room}")
                    break
        else:
            print(f"  ⚠ 未找到房間 {target_room}，使用第一個")

    _js_click(page, target_card)
    page.wait_for_timeout(4000)

    # 等遊戲室
    try:
        page.wait_for_selector('[class*="PcMainGame_timer"]', timeout=15000)
        return True, page, entry_version
    except Exception:
        if _check_expired(page):
            return "expired", page, entry_version
        return False, page, entry_version


# ── 連拍 + 分析 ──────────────────────────────────────────────────────────

def observe_round(page, round_num, video_loc, gemini_limit, skip_video_ocr, game="bac"):
    """觀察一局：連拍 → 找最佳幀 → Gemini 辨識。回傳 round dict。"""
    ts_start = datetime.now()
    round_dir = SCREENSHOT_DIR / f"round_{round_num:03d}"
    round_dir.mkdir(exist_ok=True)

    def _burst(label):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        try:
            shot = video_loc.screenshot(timeout=3000)
            p = round_dir / f"{label}_{ts}.png"
            p.write_bytes(shot)
            return str(p)
        except Exception:
            return None

    # 偵測局資訊（開牌前先抓一次局號）
    info = detect_round_info(page)
    print(f"    房間={info['room']} 局號={info['round_id']} 桌={info['table_name']}")

    # 階段 A: 連拍
    burst_frames = []
    for i in range(20):
        p = _burst(f"burst{i:02d}")
        if p:
            burst_frames.append(p)
        cur = _get_countdown(page)
        if cur != "" and not _is_dealing(cur):
            break
        page.wait_for_timeout(500)
    print(f"    連拍 {len(burst_frames)} 幀")

    # 階段 B: 結算截圖
    settle_frame = None
    cur = _get_countdown(page)
    if _is_dealing(cur) or cur == "":
        page.wait_for_timeout(1000)
        settle_frame = _burst("settle")

    # 階段 C: 過渡期補截（等下注開始）
    catchup_frames = []
    for _ in range(10):
        cur = _get_countdown(page)
        if _is_betting(cur):
            p1 = _burst("catchup_0")
            page.wait_for_timeout(2000)
            p2 = _burst("catchup_1")
            catchup_frames = [x for x in [p1, p2] if x]
            break
        page.wait_for_timeout(500)

    print(f"    結算 {1 if settle_frame else 0} + 補截 {len(catchup_frames)}")

    # 重新抓局號（結算後頁面可能更新了新局號）
    info2 = detect_round_info(page)
    if info2["round_id"] and info2["round_id"] != info["round_id"]:
        # 頁面局號已更新 → 用新的
        info["round_id"] = info2["round_id"]
    elif info["round_id"]:
        # 局號沒變 → 加時間戳後綴確保唯一
        ts_suffix = datetime.now().strftime("%H%M%S")
        info["round_id"] = f"{info['round_id']}_{ts_suffix}"

    # 找最佳幀
    all_frames = burst_frames + ([settle_frame] if settle_frame else []) + catchup_frames
    best_anim = find_best_frame(burst_frames + ([settle_frame] if settle_frame else []))
    best_video = find_best_frame(catchup_frames) if catchup_frames else ""

    print(f"    最佳動畫幀: {Path(best_anim).name if best_anim else '無'}")
    print(f"    最佳影像幀: {Path(best_video).name if best_video else '無'}")

    # Gemini 辨識
    anim_result = None
    video_result = None

    if best_anim:
        print(f"    Gemini 辨識動畫...")
        anim_result = recognize_game(best_anim, game=game, gemini_limit=gemini_limit)
        if "error" in anim_result:
            print(f"    ⚠ 動畫辨識失敗: {anim_result['message']}")
        else:
            anim = anim_result.get("animation", {})
            vid = anim_result.get("video", {})
            if anim.get("dice"):
                print(f"    動畫: 🎲 {anim.get('dice',[])} → {anim.get('display','')}")
            else:
                print(f"    動畫: P={anim.get('player_cards',[])} B={anim.get('banker_cards',[])}")
            if vid and (vid.get("player_cards") or vid.get("dice")):
                if vid.get("dice"):
                    print(f"    影像(同幀): 🎲 {vid.get('dice',[])} → {vid.get('display','')}")
                else:
                    print(f"    影像(同幀): P={vid.get('player_cards',[])} B={vid.get('banker_cards',[])}")
                video_result = vid

    # 如果同幀沒影像結果且有 catchup 幀 → 額外辨識
    if not video_result and best_video and not skip_video_ocr:
        print(f"    Gemini 辨識影像（catchup）...")
        vid_raw = recognize_game(best_video, game=game, gemini_limit=gemini_limit)
        if "error" not in vid_raw:
            video_result = vid_raw.get("video") or vid_raw.get("animation")

    # 清理非里程碑幀
    milestone_files = set()
    if best_anim:
        milestone_files.add(best_anim)
    if best_video:
        milestone_files.add(best_video)
    if settle_frame:
        milestone_files.add(settle_frame)
    for f in all_frames:
        if f not in milestone_files:
            try:
                os.remove(f)
            except OSError:
                pass

    # 判定失敗狀態
    elapsed = (datetime.now() - ts_start).total_seconds()
    failure_reason = ""

    if not burst_frames:
        overall = "CAPTURE_FAIL"
        failure_reason = "Video 元素截圖失敗（連拍 0 幀）"
        print(f"    ⚠ {failure_reason}")
    elif not best_anim or (not anim_result):
        # 有連拍但找不到最佳幀或未辨識
        from bac_frame_analyzer import _frame_has_cards
        cards_found = any(_frame_has_cards(f) for f in burst_frames if os.path.exists(f))
        if not cards_found:
            overall = "VIDEO_NO_LOAD"
            failure_reason = f"連拍 {len(burst_frames)} 幀均無牌面偵測（影片未載入）"
            print(f"    ⚠ {failure_reason}")
        else:
            overall = "OCR_FAIL"
            failure_reason = "有牌面但辨識失敗"
    elif anim_result and "error" in anim_result:
        overall = "OCR_FAIL"
        failure_reason = anim_result.get("message", "Gemini 辨識失敗")
        print(f"    ⚠ OCR 失敗: {failure_reason}")
    else:
        anim_data = anim_result.get("animation", {})
        match_status = anim_result.get("match", "N/A")
        if not anim_data.get("player_cards") and not anim_data.get("banker_cards"):
            overall = "VIDEO_NO_LOAD"
            failure_reason = "Gemini 回傳空牌面（影片可能未載入）"
            print(f"    ⚠ {failure_reason}")
        else:
            overall = "PASS" if match_status == "MATCH" else match_status

    anim_data = anim_result.get("animation", {}) if anim_result and "error" not in anim_result else {}

    return {
        "round_id": info["round_id"],
        "room": info["room"],
        "game": info["game"],
        "table_name": info["table_name"],
        "timestamp": ts_start.isoformat(),
        "elapsed_sec": round(elapsed, 1),
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
            "player_cards": video_result.get("player_cards", []) if video_result else [],
            "banker_cards": video_result.get("banker_cards", []) if video_result else [],
            "player_total": video_result.get("player_total", -1) if video_result else -1,
            "banker_total": video_result.get("banker_total", -1) if video_result else -1,
            "note": video_result.get("note", "") if video_result else "未辨識",
            "frame_file": Path(best_video).name if best_video else "",
        },
        "betting_result": None,
        "dealer_result": None,
        "verification": {
            "animation_vs_video": overall,
            "overall": overall,
            "failure_reason": failure_reason,
        },
    }


# ── 人力預估（動態計算）─────────────────────────────────────────────────────

def _fmt_time(hours, min_unit="hours"):
    """小時 → 人類可讀格式（中英文通用）。min_unit="days" 時最小單位為天。"""
    days = hours / 8  # 工作日
    if min_unit == "days":
        if days < 5:
            return f"{max(days, 1):.1f} day"
        weeks = days / 5
        if weeks < 4:
            return f"{weeks:.1f} wk"
        return f"{weeks / 4:.1f} mo"
    if hours < 1:
        return f"{hours * 60:.0f} min"
    if hours < 24:
        return f"{hours:.1f} hr"
    if days < 5:
        return f"{days:.1f} day"
    weeks = days / 5
    if weeks < 4:
        return f"{weeks:.1f} wk"
    return f"{weeks / 4:.1f} mo"


def _calc_effort_bac_verify(total_rounds, gemini_calls):
    """依局數和 Gemini 呼叫次數動態計算人力預估。"""
    rounds = max(total_rounds, 1)
    # 手動 QA：每局人工看視訊重播 + 逐張對牌，約 3 分鐘/局
    manual_hours = rounds * 3 / 60
    # 一般自動測試人員：從零建置截圖比對工具 + OCR 調參
    auto_hours = 40 + rounds * 0.1
    # 資深自動化：熟悉 OCR + Playwright，較快建置
    senior_hours = 16 + rounds * 0.05
    # AI（Claude + Gemini）：開發 + 調校 + 自動化執行（最小單位 1 天）
    ai_hours = max(8, 8 + rounds * 0.05 + gemini_calls * 0.01)
    if ai_hours >= senior_hours:
        ai_hours = senior_hours * 0.3
    return {
        "manual": _fmt_time(manual_hours) + " / run",
        "auto": _fmt_time(auto_hours),
        "senior": _fmt_time(senior_hours),
        "ai": _fmt_time(ai_hours, min_unit="days"),
    }


# ── 截圖清理 ──────────────────────────────────────────────────────────────

def cleanup_old_screenshots(retention_days: int):
    """刪除超過 retention_days 天的截圖。"""
    if retention_days <= 0:
        return
    cutoff = datetime.now() - timedelta(days=retention_days)
    count = 0
    for d in SCREENSHOT_DIR.iterdir():
        if d.is_dir() and d.name.startswith("round_"):
            for f in d.iterdir():
                if f.is_file() and datetime.fromtimestamp(f.stat().st_mtime) < cutoff:
                    f.unlink()
                    count += 1
            # 空目錄也刪
            if not any(d.iterdir()):
                d.rmdir()
    if count:
        print(f"[清理] 刪除 {count} 張超過 {retention_days} 天的截圖")


# ── 報告產出 ──────────────────────────────────────────────────────────────

def _backup(path):
    """寫檔前備份（若檔案已存在）"""
    try:
        sys.path.insert(0, str(SHARED_DIR))
        from report_tools.report_backup import backup_report
        backup_report(str(path))
    except Exception:
        pass


def save_json_report(meta: dict, rounds: list):
    """儲存 JSON 報告。"""
    report = {"meta": meta, "rounds": rounds}
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    game_tag = meta.get("game", "bac")
    path = OUTPUT_DIR / f"bac_verify_{game_tag}_{ts}.json"
    _backup(path)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[報告] JSON: {path}")
    return str(path)


def save_html_report(meta: dict, rounds: list, *, report_title="", file_prefix=""):
    """儲存 HTML 報告。report_title 可自訂標題，file_prefix 可自訂檔名前綴。"""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    game_tag = meta.get("game", "bac")
    prefix = file_prefix or f"bac_verify_{game_tag}"
    path = OUTPUT_DIR / f"{prefix}_{ts}.html"
    _backup(path)

    # 統計
    total = len(rounds)
    passed = sum(1 for r in rounds if r["verification"]["overall"] == "PASS")
    mismatch = sum(1 for r in rounds if r["verification"]["overall"] == "MISMATCH")
    load_fail = sum(1 for r in rounds if r["verification"]["overall"] in ("VIDEO_NO_LOAD", "CAPTURE_FAIL"))
    ocr_fail = sum(1 for r in rounds if r["verification"]["overall"] == "OCR_FAIL")
    other = total - passed - mismatch - load_fail - ocr_fail

    # 狀態 → 顏色映射
    STATUS_COLORS = {
        "PASS": "#C6EFCE",
        "MATCH": "#C6EFCE",
        "MISMATCH": "#FFC7CE",
        "VIDEO_NO_LOAD": "#FFE0B2",
        "CAPTURE_FAIL": "#FFE0B2",
        "OCR_FAIL": "#FFF3CD",
        "VIDEO_UNCLEAR": "#FFF3CD",
    }

    rows_html = ""
    for idx, r in enumerate(rounds):
        anim = r["animation_result"]
        vid = r["video_result"]
        status = r["verification"]["overall"]
        failure = r["verification"].get("failure_reason", "")
        color = STATUS_COLORS.get(status, "#FFF3CD")

        # 截圖縮圖 HTML（相對於報告的路徑）
        round_dir = f"screenshots/round_{idx+1:03d}"
        anim_img = ""
        if anim.get("frame_file"):
            img_path = f"{round_dir}/{anim['frame_file']}"
            anim_img = (f'<br><img src="{img_path}" class="thumb" '
                        f'onclick="showModal(this.src)" title="Animation frame">')
        vid_img = ""
        if vid.get("frame_file"):
            img_path = f"{round_dir}/{vid['frame_file']}"
            vid_img = (f'<br><img src="{img_path}" class="thumb" '
                       f'onclick="showModal(this.src)" title="Video frame">')

        # 動畫欄內容（牌面 / 張數 / 總點數 分開顯示）
        if anim.get('dice'):
            anim_text = f"🎲 {', '.join(str(d) for d in anim['dice'])} → {anim.get('display','')}"
        elif anim.get('player_cards'):
            p_cards = anim['player_cards']
            b_cards = anim['banker_cards']
            p_total = anim.get('player_total', '?')
            b_total = anim.get('banker_total', '?')
            anim_text = (f"閒({len(p_cards)}張): {', '.join(p_cards)}<br>"
                         f"<b>→ {p_total}點</b><br>"
                         f"莊({len(b_cards)}張): {', '.join(b_cards)}<br>"
                         f"<b>→ {b_total}點</b>")
        elif failure:
            anim_text = f"⚠ {failure}"
        else:
            anim_text = "—"

        # 影像欄內容
        if vid.get('dice'):
            vid_text = f"🎲 {', '.join(str(d) for d in vid['dice'])} → {vid.get('display','')}"
        elif vid.get('player_cards'):
            vp = vid['player_cards']
            vb = vid['banker_cards']
            vp_total = vid.get('player_total', '?')
            vb_total = vid.get('banker_total', '?')
            vid_text = (f"閒({len(vp)}張): {', '.join(vp)}<br>"
                        f"<b>→ {vp_total}點</b><br>"
                        f"莊({len(vb)}張): {', '.join(vb)}<br>"
                        f"<b>→ {vb_total}點</b>")
        else:
            vid_text = vid.get('note', '—')

        # 投注記錄欄（牌面 / 張數 / 總點數 分開顯示 + Round ID）
        bet = r.get("betting_result")
        if bet and bet.get("player_cards"):
            bp = bet['player_cards']
            bb = bet['banker_cards']
            bp_total = bet.get('player_total', '?')
            bb_total = bet.get('banker_total', '?')
            bet_text = (f"閒({len(bp)}張): {', '.join(bp)}<br>"
                        f"<b>→ {bp_total}點</b><br>"
                        f"莊({len(bb)}張): {', '.join(bb)}<br>"
                        f"<b>→ {bb_total}點</b>")
            bet_rid = bet.get("round_id", "")
            if bet_rid:
                bet_text += f"<br><small>局號: {bet_rid}</small>"
            if bet.get("frame_file"):
                bet_img_path = f"screenshots/bet_record/{bet['frame_file']}"
                bet_text += (f'<br><img src="{bet_img_path}" class="thumb" '
                             f'onclick="showModal(this.src)" title="Bet Record">')
        else:
            bet_text = "—"

        # Dealer Side 欄（輸入 + dispatch log + 截圖）
        dealer = r.get("dealer_result")
        if dealer and dealer.get("cards_display"):
            dealer_text = f"<b>送出:</b> {', '.join(dealer['cards_display'])}"
            # Dispatch log
            dlog = dealer.get("dispatch_log", [])
            if dlog:
                dealer_text += "<br><b>Dispatch:</b><br>"
                for dl in dlog:
                    ci = dl['dispatch']['cardIndex']
                    who = dl['dispatch']['who']
                    val_disp = dl['sent']['display']
                    dealer_text += f"<small>#{dl['index']}: ci={ci} who={who} → {val_disp}</small><br>"
            dealer_rid = dealer.get("round_id", "")
            if dealer_rid:
                dealer_text += f"<small>局號: {dealer_rid}</small>"
            # 截圖（可能多張）
            for ff in dealer.get("frame_files", []):
                img_path = f"{round_dir}/{ff}"
                dealer_text += (f'<br><img src="{img_path}" class="thumb" '
                                f'onclick="showModal(this.src)" title="Dealer">')
        else:
            dealer_text = "—"

        # 計畫資訊（如有）
        plan = r.get("plan_info")
        round_id_display = r['round_id']
        if plan:
            round_id_display = (f"<b>{plan['plan_id']}</b><br>"
                                f"目標: {plan['target_card']}<br>"
                                f"<small>{plan['progress']}</small><br>"
                                f"{r['round_id']}")

        rows_html += f"""<tr style="background:{color}">
  <td>{round_id_display}</td>
  <td>{r['room']}</td>
  <td>{r['game']}</td>
  <td>{anim_text}{anim_img}</td>
  <td>{vid_text}{vid_img}</td>
  <td>{bet_text}</td>
  <td>{dealer_text}</td>
  <td><b>{status}</b></td>
</tr>"""

    gemini = get_gemini_usage(meta.get("gemini_limit", 50))
    effort = _calc_effort_bac_verify(total, gemini["session_used"])
    report_title_js = report_title or "牌面驗證報告"

    html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<title data-i18n="title">{report_title or '牌面驗證報告'}</title>
<style>
  body {{ font-family: -apple-system, 'Segoe UI', sans-serif; margin: 0; background: #f0f2f5; color: #333; }}
  .lang-toggle {{ background: #0a3d91; padding: 8px 40px; display: flex; justify-content: flex-end; gap: 0; }}
  .lang-btn {{ padding: 5px 14px; border: 1px solid rgba(255,255,255,0.5); background: transparent;
               color: white; cursor: pointer; font-size: 12px; transition: all 0.2s; }}
  .lang-btn:first-child {{ border-radius: 4px 0 0 4px; }}
  .lang-btn:last-child {{ border-radius: 0 4px 4px 0; }}
  .lang-btn.active {{ background: white; color: #1a237e; font-weight: bold; }}
  .header {{ background: linear-gradient(135deg, #1a237e, #283593); color: white;
             padding: 30px 40px; display: flex; gap: 24px; align-items: flex-start; }}
  .header-main {{ flex: 1; min-width: 0; }}
  .header-main h1 {{ font-size: 24px; margin: 0 0 8px; }}
  .meta {{ font-size: 14px; opacity: 0.85; line-height: 1.8; word-break: break-all; }}
  .effort-panel {{ background: rgba(255,255,255,0.1); border-radius: 10px; padding: 14px 18px;
                   min-width: 260px; flex-shrink: 0; }}
  .effort-panel h4 {{ font-size: 12px; opacity: 0.7; margin: 0 0 10px; letter-spacing: 0.5px;
                      text-transform: uppercase; }}
  .effort-row {{ display: flex; justify-content: space-between; align-items: center;
                 padding: 5px 0; border-bottom: 1px solid rgba(255,255,255,0.1); font-size: 12px; }}
  .effort-role {{ opacity: 0.9; }}
  .effort-time {{ font-weight: bold; }}
  .effort-row.ai-row .effort-time {{ color: #69f0ae; }}
  .stats {{ display: flex; gap: 16px; padding: 20px 40px; flex-wrap: wrap; }}
  .stat {{ flex: 1; min-width: 120px; background: white; padding: 15px 25px; border-radius: 10px;
           text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
  .stat .num {{ font-size: 2em; font-weight: bold; }}
  .stat.pass .num {{ color: #2e7d32; }}
  .stat.mismatch .num {{ color: #c62828; }}
  .stat.load-fail .num {{ color: #e65100; }}
  .stat.na .num {{ color: #9e9e9e; }}
  .gemini {{ margin: 0 40px 20px; background: white; padding: 12px 20px; border-radius: 8px;
             font-size: 0.9em; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
  .section {{ padding: 0 40px 20px; }}
  table {{ width: 100%; border-collapse: collapse; background: white; font-size: 13px;
           box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
  th {{ background: #1F4E79; color: white; padding: 10px; text-align: left; }}
  td {{ padding: 8px 10px; border-bottom: 1px solid #ddd; vertical-align: top; }}
  .thumb {{ width: 180px; margin-top: 5px; cursor: pointer; border: 1px solid #ccc; border-radius: 4px; }}
  .thumb:hover {{ border-color: #1a237e; box-shadow: 0 0 6px rgba(26,35,126,0.3); }}
  .modal-bg {{ display:none; position:fixed; top:0; left:0; width:100%; height:100%;
               background:rgba(0,0,0,0.8); z-index:9999; justify-content:center; align-items:center; }}
  .modal-bg.active {{ display:flex; }}
  .modal-bg img {{ max-width:90%; max-height:90%; border-radius:8px; }}
  .modal-close {{ position:fixed; top:15px; right:25px; color:white; font-size:2em; cursor:pointer; z-index:10000; }}
</style>
</head>
<body>
<div class="lang-toggle">
  <button class="lang-btn active" onclick="switchLang('zh')">中文</button>
  <button class="lang-btn" onclick="switchLang('en')">EN</button>
</div>
<div class="header">
  <div class="header-main">
    <h1><span data-i18n="title">{report_title or '牌面驗證報告'}</span> — {meta.get('game_name', meta.get('env','').upper())}</h1>
    <div class="meta">
      <span data-i18n="lbl_version">版本</span>: {meta.get('version','')} |
      <span data-i18n="lbl_env">環境</span>: {meta.get('env','').upper()} |
      <span data-i18n="lbl_url">網址</span>: {meta.get('url','')[:80]}...<br>
      <span data-i18n="lbl_time">執行時間</span>: {meta.get('start_time','')} |
      <span data-i18n="lbl_rounds">總局數</span>: {total}
    </div>
  </div>
  <div class="effort-panel">
    <h4 data-i18n="effort_title">人力預估</h4>
    <div class="effort-row"><span class="effort-role" data-i18n="effort_manual_qa">手動 QA</span><span class="effort-time">{effort['manual']}</span></div>
    <div class="effort-row"><span class="effort-role" data-i18n="effort_auto_tester">一般自動測試人員</span><span class="effort-time">{effort['auto']}</span></div>
    <div class="effort-row"><span class="effort-role" data-i18n="effort_senior">資深自動化測試</span><span class="effort-time">{effort['senior']}</span></div>
    <div class="effort-row ai-row"><span class="effort-role" data-i18n="effort_ai">AI（Claude + Gemini）</span><span class="effort-time">{effort['ai']}</span></div>
  </div>
</div>

<div class="stats">
  <div class="stat pass"><div class="num">{passed}</div><span data-i18n="stat_pass">PASS</span></div>
  <div class="stat mismatch"><div class="num">{mismatch}</div><span data-i18n="stat_mismatch">MISMATCH</span></div>
  <div class="stat load-fail"><div class="num">{load_fail}</div><span data-i18n="stat_load_fail">Load Fail</span></div>
  <div class="stat na"><div class="num">{ocr_fail + other}</div><span data-i18n="stat_na">N/A</span></div>
  <div class="stat"><div class="num">{total}</div><span data-i18n="stat_total">Total</span></div>
</div>

<div class="gemini">
  <span data-i18n="gemini_quota">Gemini 額度</span>:
  <span data-i18n="gemini_today">今日</span> {gemini['daily_used']}/{gemini['daily_limit']} |
  <span data-i18n="gemini_session">本次</span> {gemini['session_used']}/{gemini['session_limit']} |
  <span data-i18n="gemini_remaining">剩餘</span> {gemini['remaining']}
</div>

<div class="section">
<table>
<tr>
  <th data-i18n="th_round">局號</th><th data-i18n="th_room">房間</th><th data-i18n="th_game">遊戲</th>
  <th data-i18n="th_animation">開牌動畫</th><th data-i18n="th_video">影像串流</th>
  <th data-i18n="th_betting">投注紀錄</th><th data-i18n="th_dealer">Dealer Side</th><th data-i18n="th_result">結果</th>
</tr>
{rows_html}
</table>
</div>

<div class="modal-bg" id="imgModal" onclick="this.classList.remove('active')">
  <span class="modal-close" onclick="document.getElementById('imgModal').classList.remove('active')">&times;</span>
  <img id="modalImg" src="">
</div>
<script>
function showModal(src) {{
  document.getElementById('modalImg').src = src;
  document.getElementById('imgModal').classList.add('active');
}}
const I18N = {{
  "zh": {{
    "title": "{report_title_js}",
    "lbl_version": "版本", "lbl_env": "環境", "lbl_url": "網址",
    "lbl_time": "執行時間", "lbl_rounds": "總局數",
    "effort_title": "人力預估",
    "effort_manual_qa": "手動 QA", "effort_auto_tester": "一般自動測試人員",
    "effort_senior": "資深自動化測試", "effort_ai": "AI（Claude + Gemini）",
    "stat_pass": "PASS", "stat_mismatch": "MISMATCH",
    "stat_load_fail": "載入失敗", "stat_na": "N/A", "stat_total": "總局數",
    "th_round": "局號", "th_room": "房間", "th_game": "遊戲",
    "th_animation": "開牌動畫", "th_video": "影像串流",
    "th_betting": "投注紀錄", "th_dealer": "Dealer Side", "th_result": "結果",
    "gemini_quota": "Gemini 額度", "gemini_today": "今日",
    "gemini_session": "本次", "gemini_remaining": "剩餘"
  }},
  "en": {{
    "title": "{report_title_js if report_title_js != '牌面驗證報告' else 'Card Verification Report'}",
    "lbl_version": "Version", "lbl_env": "Env", "lbl_url": "URL",
    "lbl_time": "Time", "lbl_rounds": "Rounds",
    "effort_title": "Effort Estimation",
    "effort_manual_qa": "Manual QA", "effort_auto_tester": "Automation Tester",
    "effort_senior": "Senior Automation", "effort_ai": "AI (Claude + Gemini)",
    "stat_pass": "PASS", "stat_mismatch": "MISMATCH",
    "stat_load_fail": "Load Fail", "stat_na": "N/A", "stat_total": "Total",
    "th_round": "Round", "th_room": "Room", "th_game": "Game",
    "th_animation": "Animation", "th_video": "Video Stream",
    "th_betting": "Betting", "th_dealer": "Dealer Side", "th_result": "Result",
    "gemini_quota": "Gemini Quota", "gemini_today": "Today",
    "gemini_session": "Session", "gemini_remaining": "Remaining"
  }}
}};
let currentLang = localStorage.getItem('report_lang') || 'zh';
function switchLang(lang) {{
  currentLang = lang;
  localStorage.setItem('report_lang', lang);
  const t = I18N[lang];
  document.documentElement.lang = lang === 'zh' ? 'zh-Hant' : 'en';
  document.querySelectorAll('[data-i18n]').forEach(el => {{
    const key = el.getAttribute('data-i18n');
    if (t[key] !== undefined) el.textContent = t[key];
  }});
  document.querySelectorAll('.lang-btn').forEach(btn => {{
    btn.classList.toggle('active', btn.textContent.trim() === (lang === 'zh' ? '中文' : 'EN'));
  }});
}}
switchLang(currentLang);
</script>
</body></html>"""

    path.write_text(html, encoding="utf-8")
    print(f"[報告] HTML: {path}")
    return str(path)


# ── 主流程 ────────────────────────────────────────────────────────────────

def run(env, pid, currency, rounds, headed, url,
        gemini_limit, skip_video_ocr, retention_days, game="bac"):
    global _current_game
    _current_game = game
    gcfg = GAME_CONFIG.get(game, GAME_CONFIG["bac"])

    _ensure_dirs()
    cleanup_old_screenshots(retention_days)

    print("=" * 60)
    print(f"牌面驗證系統 — {gcfg['name']}")
    print("=" * 60)

    # 登入
    if not url:
        print(f"\n[登入] {env.upper()} / {pid} / {currency.upper()}")
        url = get_login_url(env, pid, currency)
        if not url:
            print("[登入] 失敗")
            return

    # Gemini 額度
    usage = get_gemini_usage(gemini_limit)
    print(f"\n[Gemini] 今日 {usage['daily_used']}/{usage['daily_limit']} | "
          f"本次上限 {gemini_limit} | 剩餘 {usage['remaining']}")

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=not headed)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()

        # 進房（含 TSS 重試）
        entry_version = ""
        for attempt in range(1, 4):
            if attempt > 1:
                url = get_login_url(env, pid, currency)
                if not url:
                    break
            print(f"\n[瀏覽器] 嘗試 {attempt}...")
            page.goto(url, timeout=30000, wait_until="domcontentloaded")
            result, page, entry_version = enter_game_room(
                page, context, category=gcfg["category"], target_room=gcfg["default_room"])
            if result == "expired":
                print("  TSS 過期，重試...")
                continue
            elif result:
                break
            else:
                print("  進房失敗")
                browser.close()
                return
        else:
            print("[錯誤] 3 次重試均失敗")
            browser.close()
            return

        # 版本
        version = entry_version
        url_ver = re.search(r"/pa/pc/v([\d.]+)/", page.url)
        if url_ver:
            version = f"@pa/host v{url_ver.group(1)}"

        meta = {
            "version": version,
            "url": page.url,
            "env": env,
            "pid": pid,
            "currency": currency,
            "game": game,
            "game_name": gcfg["name"],
            "start_time": datetime.now().isoformat(),
            "total_rounds": rounds,
            "gemini_limit": gemini_limit,
            "retention_days": retention_days,
        }

        print(f"\n[開始] 版本={version} 局數={rounds}")

        # Video 元素
        video_loc = page.locator("video").first
        round_results = []

        for rn in range(1, rounds + 1):
            # 等下注階段
            print(f"\n[局 {rn}/{rounds}] 等待開牌...")
            prev = ""
            for _ in range(120):  # 最多 60 秒
                cur = _get_countdown(page)
                if _is_dealing(cur) and not _is_dealing(prev):
                    break
                prev = cur
                page.wait_for_timeout(500)
            else:
                print("  等待超時")
                break

            result = observe_round(page, rn, video_loc, gemini_limit, skip_video_ocr, game=game)
            round_results.append(result)

            status = result["verification"]["overall"]
            anim = result["animation_result"]
            if anim.get("dice"):
                print(f"  → {status} | {anim.get('display', '')}")
            else:
                print(f"  → {status} | P={anim.get('player_total',-1)} "
                      f"B={anim.get('banker_total',-1)} ({anim.get('total_cards',0)}張)")

        # 報告
        meta["end_time"] = datetime.now().isoformat()
        meta["actual_rounds"] = len(round_results)
        json_path = save_json_report(meta, round_results)
        html_path = save_html_report(meta, round_results)

        # 最終額度
        final_usage = get_gemini_usage(gemini_limit)
        print(f"\n[Gemini] 最終: 今日 {final_usage['daily_used']}/{final_usage['daily_limit']} | "
              f"本次 {final_usage['session_used']}/{final_usage['session_limit']}")

        browser.close()
        print(f"\n完成！報告: {html_path}")


def main():
    ap = argparse.ArgumentParser(description="牌面/骰面驗證系統")
    ap.add_argument("--env", default="uat")
    ap.add_argument("--pid", default="<ACCOUNT>")
    ap.add_argument("--currency", default="cny")
    ap.add_argument("--game", default="bac", choices=["bac", "sic", "ssic"],
                    help="遊戲: bac=百家樂, sic=骰寶, ssic=超倍骰寶")
    ap.add_argument("--rounds", type=int, default=3)
    ap.add_argument("--headed", action="store_true")
    ap.add_argument("--url", default="")
    ap.add_argument("--gemini-limit", type=int, default=50)
    ap.add_argument("--skip-video-ocr", action="store_true")
    ap.add_argument("--retention-days", type=int, default=7)
    ap.add_argument("--from-json", default="",
                    help="從 JSON 重產 HTML 報告（不執行驗證）")
    args = ap.parse_args()

    # 從 JSON 重產報告
    if args.from_json:
        _ensure_dirs()
        with open(args.from_json, encoding="utf-8") as f:
            data = json.load(f)
        path = save_html_report(data["meta"], data["rounds"])
        print(f"重產完成: {path}")
        return

    run(args.env, args.pid, args.currency, args.rounds, args.headed, args.url,
        args.gemini_limit, args.skip_video_ocr, args.retention_days, args.game)


if __name__ == "__main__":
    main()
