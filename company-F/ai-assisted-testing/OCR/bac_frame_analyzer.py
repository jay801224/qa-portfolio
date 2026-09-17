"""
bac_frame_analyzer.py — 百家樂牌面幀分析器

功能：
  1. detect_round_info(page)  — 從 DOM/URL 取得房間號、局號、遊戲、版本
  2. find_best_frame(frames)  — 從連拍幀中找牌面最清晰的幀
  3. recognize_cards(path)    — Gemini Vision 辨識牌面（結構化 JSON 輸出）
  4. get_gemini_usage()       — 查詢今日 Gemini 用量

設計原則：
  - 免費資訊（房間/局號/版本）全部走 DOM/URL，不消耗 Gemini
  - Gemini 僅用於牌面辨識，每局 1~2 次
  - 額度管控：超過上限停止辨識，只做截圖記錄
"""

import json
import os
import re
import sys
from pathlib import Path

import cv2
import numpy as np

# ── Gemini 相關（延遲 import 避免啟動慢）─────────────────────────────────────

_SHARED_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # shared/
sys.path.insert(0, _SHARED_DIR)

# Gemini 呼叫計數（本次執行內）
_session_gemini_calls = 0


def _get_gemini_module():
    """延遲載入 gemini_vision 模組"""
    from ai.gemini_vision import (
        _call_gemini_api,
        _load_image_part,
        check_daily_usage,
        DAILY_CALL_LIMIT,
    )
    return _call_gemini_api, _load_image_part, check_daily_usage, DAILY_CALL_LIMIT


# ── 1. 局資訊偵測（免費，不消耗 Gemini）────────────────────────────────────────

def detect_round_info(page) -> dict:
    """從 DOM / URL 取得當局資訊。

    Returns:
        {
            "room": "L047",
            "table_name": "百家乐 L47",
            "game": "百家樂",
            "round_id": "GL04726327033",
            "version": "v1.2.20",
            "url": "https://example.internal",
            "timer": "开牌中",
        }
    """
    info = {"room": "", "table_name": "", "game": "", "round_id": "",
            "version": "", "url": "", "timer": ""}

    try:
        info["url"] = page.url or ""
    except Exception:
        pass

    # 房間號 from URL hash
    url = info["url"]
    if "#/game/" in url:
        info["room"] = url.split("#/game/")[-1].split("?")[0].split("&")[0]

    # 版本 from URL path
    ver_m = re.search(r"/pa/pc/v([\d.]+)/", url)
    if ver_m:
        info["version"] = f"v{ver_m.group(1)}"

    # DOM 掃描
    try:
        dom = page.evaluate("""() => {
            const r = {};

            // 桌名
            const tn = document.querySelector('[class*="topTableName"]')
                    || document.querySelector('[class*="TableName"]')
                    || document.querySelector('[class*="tableName"]');
            r.tableName = tn ? tn.textContent.trim() : '';

            // 局號：從 body innerText 抓所有 G+房間號+序號，取最新（序號最大）
            const bt = document.body.innerText || '';
            const gc = bt.match(/G[A-Z]\\d{2,4}\\d{6,}/g);
            r.allGameCodes = gc || [];
            // 取序號最大的（最新局）
            r.gameCode = gc ? gc.sort().pop() : '';

            // Timer
            const tm = document.querySelector('[class*="PcMainGame_timer"]');
            r.timer = tm ? tm.textContent.trim() : '';

            return r;
        }""")

        info["table_name"] = dom.get("tableName", "")
        info["round_id"] = dom.get("gameCode", "")
        info["timer"] = dom.get("timer", "")

        # 遊戲類型 from 桌名
        tn = info["table_name"]
        if "百家" in tn or "Baccarat" in tn.lower():
            info["game"] = "百家樂"
        elif "骰" in tn or "Sic" in tn:
            info["game"] = "骰寶"
        elif "龍虎" in tn or "龙虎" in tn or "Dragon" in tn:
            info["game"] = "龍虎"
        elif "輪盤" in tn or "轮盘" in tn or "Roulette" in tn:
            info["game"] = "輪盤"
        else:
            info["game"] = tn or "未知"

    except Exception as e:
        print(f"  [analyzer] DOM 掃描失敗: {e}")

    # round_id fallback: 房間號 + 時間戳
    if not info["round_id"]:
        from datetime import datetime
        info["round_id"] = f"{info['room']}_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    return info


# ── 2. 最佳幀選取（OpenCV 清晰度計算）──────────────────────────────────────────

def _frame_sharpness(path: str) -> float:
    """計算單幀清晰度（Laplacian variance）。值越高越清晰。"""
    try:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return 0.0
        return cv2.Laplacian(img, cv2.CV_64F).var()
    except Exception:
        return 0.0


def _frame_has_cards(path: str) -> bool:
    """快速判斷幀中是否有白色牌面區域（連拍早期幀可能還沒發牌）。"""
    try:
        img = cv2.imread(path)
        if img is None:
            return False
        h, w = img.shape[:2]
        # 只看中央牌面區域（y: 50-70%, x: 20-80%）
        roi = img[int(h * 0.50):int(h * 0.70), int(w * 0.20):int(w * 0.80)]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        # 計算白色像素比例
        white_pixels = np.sum(gray > 180)
        total = gray.size
        ratio = white_pixels / total if total > 0 else 0
        # 有牌面時白色比例 > 2%（牌面是白底）
        return ratio > 0.02
    except Exception:
        return False


def find_best_frame(frame_paths: list) -> str:
    """從連拍幀中找到牌面最清晰的幀。

    策略：先過濾有牌面的幀，再按清晰度排序取最高。

    Returns:
        最佳幀的路徑，或空字串。
    """
    if not frame_paths:
        return ""

    # 過濾有牌面的幀
    with_cards = [(p, _frame_sharpness(p)) for p in frame_paths if _frame_has_cards(p)]

    if not with_cards:
        # fallback: 全部幀按清晰度取最高
        all_scored = [(p, _frame_sharpness(p)) for p in frame_paths]
        all_scored.sort(key=lambda x: x[1], reverse=True)
        return all_scored[0][0] if all_scored else ""

    with_cards.sort(key=lambda x: x[1], reverse=True)
    return with_cards[0][0]


# ── 3. Gemini 牌面辨識 ─────────────────────────────────────────────────────────

# 精簡 prompt — 要求純 JSON 輸出，減少 token 消耗
# ── Prompt 定義（按遊戲切換）───────────────────────────────────────────────

CARD_RECOGNIZE_PROMPT = """辨識這張百家樂截圖中的牌面。畫面有兩層：
1. 開牌動畫（前端覆疊的小牌，黑底白牌）
2. 影像串流（荷官桌上的實體牌）

重要：開牌動畫區每一方的顯示順序是「總點數（一個數字）→ 撲克牌（2~3張）」。
總點數不是牌，請忽略它，只辨識後面的撲克牌。
例如看到「8」接著「10♣」「8♣」，代表閒家總點數8、手牌為10♣和8♣。

請分別辨識兩層的牌面，回傳 JSON：
{
  "animation": {
    "player_cards": ["面值花色", ...],
    "banker_cards": ["面值花色", ...]
  },
  "video": {
    "player_cards": ["面值花色", ...],
    "banker_cards": ["面值花色", ...],
    "note": "如有遮擋或看不清請說明"
  }
}
面值: A/2/3/4/5/6/7/8/9/10/J/Q/K
花色: ♠/♥/♣/♦
看不清的牌用 "?" 表示。只回傳 JSON。"""

DICE_RECOGNIZE_PROMPT = """辨識這張骰寶截圖中的三顆骰子。畫面有兩層：
1. 開獎動畫（前端覆疊的骰子動畫）
2. 影像串流（荷官桌上的實體骰寶）

請分別辨識兩層的骰子點數，回傳 JSON：
{
  "animation": {
    "dice": [d1, d2, d3],
    "total": d1+d2+d3
  },
  "video": {
    "dice": [d1, d2, d3],
    "total": d1+d2+d3,
    "note": "如有遮擋或看不清請說明"
  }
}
點數: 1-6。看不清用 0。只回傳 JSON。"""

SUPER_DICE_RECOGNIZE_PROMPT = """辨識這張超倍骰寶截圖。畫面有三層：
1. 開獎動畫（前端覆疊的骰子動畫）
2. 影像串流（荷官桌上的實體骰寶）
3. Lightning 倍率（畫面上的隨機倍率顯示）

回傳 JSON：
{
  "animation": {
    "dice": [d1, d2, d3],
    "total": d1+d2+d3
  },
  "video": {
    "dice": [d1, d2, d3],
    "total": d1+d2+d3,
    "note": "如有遮擋或看不清請說明"
  },
  "lightning": {
    "multiplied_areas": ["區域 倍率", ...],
    "note": ""
  }
}
點數: 1-6。看不清用 0。只回傳 JSON。"""

GAME_PROMPTS = {
    "bac": CARD_RECOGNIZE_PROMPT,
    "sic": DICE_RECOGNIZE_PROMPT,
    "ssic": SUPER_DICE_RECOGNIZE_PROMPT,
}


def recognize_game(frame_path: str, game: str = "bac", gemini_limit: int = 50) -> dict:
    """通用 Gemini 辨識（依 game 自動選 Prompt）。"""
    prompt = GAME_PROMPTS.get(game, CARD_RECOGNIZE_PROMPT)
    return _recognize_with_prompt(frame_path, prompt, gemini_limit)


# 保留舊名稱相容
def recognize_cards(frame_path: str, gemini_limit: int = 50) -> dict:
    return _recognize_with_prompt(frame_path, CARD_RECOGNIZE_PROMPT, gemini_limit)


def _call_claude_fallback(frame_path: str, prompt: str) -> dict:
    """Claude API fallback — Gemini 額度用完時使用。"""
    try:
        import anthropic
        import base64
        from pathlib import Path

        sys.path.insert(0, str(Path(__file__).parent.parent))
        from ai.gemini_vision import load_env
        config = load_env()

        api_key = config.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            return {"error": "no_claude_key", "message": "ANTHROPIC_API_KEY 未設定"}

        model = config.get("CLAUDE_MODEL", "claude-sonnet-4-20250514")
        img_data = Path(frame_path).read_bytes()
        b64 = base64.standard_b64encode(img_data).decode("utf-8")
        suffix = Path(frame_path).suffix.lower()
        mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}.get(suffix, "image/png")

        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": mime, "data": b64}},
                    {"type": "text", "text": prompt},
                ],
            }],
        )
        raw_text = response.content[0].text
        print(f"  [Claude fallback] 辨識完成 (model={model})")
        return _parse_gemini_response(raw_text)

    except ImportError:
        return {"error": "no_anthropic", "message": "anthropic 套件未安裝 (pip install anthropic)"}
    except Exception as e:
        return {"error": "claude_error", "message": str(e)}


def _recognize_with_prompt(frame_path: str, prompt: str, gemini_limit: int = 50) -> dict:
    """通用辨識核心 — Gemini 為主，額度用完自動切 Claude。"""
    global _session_gemini_calls

    if _session_gemini_calls >= gemini_limit:
        print(f"  [Gemini] 本次額度已達上限 ({gemini_limit})，切換 Claude...")
        return _call_claude_fallback(frame_path, prompt)

    try:
        call_api, load_image, check_usage, daily_limit = _get_gemini_module()
    except Exception as e:
        return {"error": "import_failed", "message": str(e)}

    used, can_continue = check_usage()
    if not can_continue:
        print(f"  [Gemini] 今日額度已用完 ({used}/{daily_limit})，切換 Claude...")
        return _call_claude_fallback(frame_path, prompt)

    remaining = daily_limit - used
    session_remaining = gemini_limit - _session_gemini_calls
    print(f"  [Gemini] 額度: 今日 {used}/{daily_limit} | "
          f"本次 {_session_gemini_calls}/{gemini_limit} | "
          f"剩餘 {min(remaining, session_remaining)}")

    if remaining <= 10:
        print(f"  ⚠ Gemini 額度即將用完（剩 {remaining} 次）")

    part, _ = load_image(frame_path)
    if part is None:
        return {"error": "load_failed", "message": f"無法載入: {frame_path}"}

    try:
        raw_text = call_api([prompt, part])
        _session_gemini_calls += 1
    except RuntimeError as e:
        # 所有 Gemini key 額度用完 → fallback Claude
        if "額度" in str(e) or "429" in str(e):
            print(f"  [Gemini] 所有 key 額度用完，切換 Claude...")
            return _call_claude_fallback(frame_path, prompt)
        return {"error": "api_error", "message": str(e)}
    except Exception as e:
        return {"error": "api_error", "message": str(e)}

    return _parse_gemini_response(raw_text)


def _parse_gemini_response(text: str) -> dict:
    """解析 Gemini 回傳的牌面 JSON。"""
    # 嘗試提取 JSON 區塊（可能包在 ```json ... ``` 中）
    json_match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    json_str = json_match.group(1) if json_match else text.strip()

    # 嘗試直接找 { ... }
    brace_match = re.search(r"\{.*\}", json_str, re.DOTALL)
    if brace_match:
        json_str = brace_match.group(0)

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        return {"error": "parse_failed", "raw": text[:500]}

    result = {"raw": text[:300]}

    # 判斷遊戲類型：有 dice → 骰寶；有 player_cards → 百家樂
    is_dice = any("dice" in data.get(layer, {}) for layer in ("animation", "video"))

    for layer in ("animation", "video"):
        if layer not in data:
            continue
        layer_data = data[layer]

        if is_dice:
            # 骰寶：計算總和 + 大小 + 單雙
            dice = layer_data.get("dice", [])
            if dice and all(isinstance(d, int) and d > 0 for d in dice):
                total = sum(dice)
                layer_data["total"] = total
                is_triple = len(set(dice)) == 1
                if is_triple:
                    layer_data["big_small"] = "三同號"
                    layer_data["odd_even"] = "三同號"
                else:
                    layer_data["big_small"] = "大" if total >= 11 else "小"
                    layer_data["odd_even"] = "單" if total % 2 == 1 else "雙"
                layer_data["display"] = f"{layer_data['big_small']} {layer_data['odd_even']} {total}"
        else:
            # 百家樂：計算點數
            for side in ("player_cards", "banker_cards"):
                cards = layer_data.get(side, [])
                total = _calc_bac_total(cards)
                layer_data[f"{side.replace('_cards', '')}_total"] = total
            layer_data["total_cards"] = (
                len(layer_data.get("player_cards", []))
                + len(layer_data.get("banker_cards", []))
            )

        result[layer] = layer_data

    # lightning（超倍骰寶）
    if "lightning" in data:
        result["lightning"] = data["lightning"]

    # 比對
    anim = result.get("animation", {})
    video = result.get("video", {})
    if anim and video:
        if is_dice:
            a_total = anim.get("total", -1)
            v_total = video.get("total", -2)
            if a_total == v_total and a_total > 0:
                result["match"] = "MATCH"
            elif v_total <= 0:
                result["match"] = "VIDEO_UNCLEAR"
            else:
                result["match"] = "MISMATCH"
        else:
            a_pt = anim.get("player_total", -1)
            a_bt = anim.get("banker_total", -1)
            v_pt = video.get("player_total", -2)
            v_bt = video.get("banker_total", -2)
            if a_pt == v_pt and a_bt == v_bt:
                result["match"] = "MATCH"
            elif v_pt == -2 or v_bt == -2:
                result["match"] = "VIDEO_UNCLEAR"
            else:
                result["match"] = "MISMATCH"

    return result


def _card_face_to_point(face: str) -> int:
    """單張牌面值轉百家樂點數。"""
    face = face.strip().upper()
    if face in ("10", "J", "Q", "K", "0"):
        return 0
    if face == "A":
        return 1
    try:
        v = int(face)
        return v if 2 <= v <= 9 else 0
    except ValueError:
        return 0


def _calc_bac_total(cards: list) -> int:
    """計算百家樂點數總和（取個位數）。cards: ["J♥", "6♦", ...]"""
    total = 0
    for c in cards:
        if c == "?":
            return -1  # 有未辨識的牌
        # 提取面值（去掉花色符號）
        face = re.sub(r"[♠♥♣♦]", "", c).strip()
        total += _card_face_to_point(face)
    return total % 10


# ── 4. 額度查詢 ────────────────────────────────────────────────────────────────

def get_gemini_usage(gemini_limit: int = 50) -> dict:
    """回傳目前 Gemini 用量。"""
    try:
        _, _, check_usage, daily_limit = _get_gemini_module()
        used, _ = check_usage()
    except Exception:
        used, daily_limit = 0, 50

    return {
        "daily_used": used,
        "daily_limit": daily_limit,
        "session_used": _session_gemini_calls,
        "session_limit": gemini_limit,
        "remaining": min(daily_limit - used, gemini_limit - _session_gemini_calls),
    }
