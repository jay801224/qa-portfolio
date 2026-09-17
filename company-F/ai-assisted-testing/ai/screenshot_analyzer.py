"""
screenshot_analyzer.py — TC FAIL 截圖分析工具

用途：供 TC fail repair 流程使用，透過 Gemini Vision 分析 FAIL 截圖，
      回傳結構化的異常描述，協助判定真 BUG 或腳本問題。

使用方式（import）：
    from shared.ai.screenshot_analyzer import analyze_fail_screenshot

    result = analyze_fail_screenshot(
        tc_id="<PRODUCT>-TC_0027",
        screenshot_path="screenshots/testcase0027_fail_20260315.png",
        tc_name="投注後餘額未更新",
        expected_result="投注後餘額應減少對應金額",
    )
    # result = {
    #     "tc_id": "<PRODUCT>-TC_0027",
    #     "description": "截圖顯示...",
    #     "anomalies": ["餘額數值未變動", ...],
    #     "matches_expected": False,
    # }
"""

import sys
from pathlib import Path

# ── Windows 終端編碼防護 ─────────────────────────────────────────────────────
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

try:
    from shared.ai.gemini_vision import describe_image
    _GEMINI_OK = True
except ImportError:
    try:
        from gemini_vision import describe_image
        _GEMINI_OK = True
    except ImportError:
        _GEMINI_OK = False


def analyze_fail_screenshot(tc_id, screenshot_path,
                            tc_name="", expected_result=""):
    """分析 TC FAIL 截圖，回傳結構化分析結果。

    Args:
        tc_id: TC 編號（如 <PRODUCT>-TC_0027）
        screenshot_path: 截圖檔案路徑
        tc_name: TC 名稱（提供更好的上下文）
        expected_result: 預期結果（用於比對）

    Returns:
        {
            "tc_id": str,
            "description": str,    # Gemini 產出的截圖描述
            "anomalies": list,     # 偵測到的異常列表
            "matches_expected": bool | None,  # 截圖是否符合預期
        }

    Raises:
        FileNotFoundError: 截圖不存在
        RuntimeError: Gemini API 額度用完或未設定
    """
    path = Path(screenshot_path)
    if not path.exists():
        raise FileNotFoundError(f"截圖不存在: {screenshot_path}")

    if not _GEMINI_OK:
        raise RuntimeError(
            "gemini_vision 模組無法載入，請確認 google-generativeai 已安裝"
        )

    # 組裝上下文
    context_parts = [f"TC FAIL 截圖分析 — {tc_id}"]
    if tc_name:
        context_parts.append(f"TC 名稱: {tc_name}")
    if expected_result:
        context_parts.append(f"預期結果: {expected_result}")
    context = "。".join(context_parts)

    description = describe_image(str(screenshot_path), context=context)

    # 從描述中提取異常
    anomalies = _extract_anomalies(description)

    # 判斷是否符合預期
    matches_expected = None
    if expected_result and description:
        matches_expected = _check_matches_expected(
            description, expected_result
        )

    return {
        "tc_id": tc_id,
        "description": description,
        "anomalies": anomalies,
        "matches_expected": matches_expected,
    }


def _extract_anomalies(description):
    """從 Gemini 描述中提取異常關鍵詞。"""
    anomaly_keywords = [
        "錯誤", "異常", "錯位", "重疊", "截斷", "空白",
        "不正確", "缺失", "遺失", "消失", "未顯示", "未更新",
        "BUG", "bug", "error", "Error", "警告", "失敗",
        "不符", "不一致", "亂碼",
    ]
    anomalies = []
    for keyword in anomaly_keywords:
        if keyword in description:
            # 取包含關鍵詞的那句話
            for sentence in description.replace("\n", "。").split("。"):
                if keyword in sentence and sentence.strip():
                    cleaned = sentence.strip()
                    if cleaned not in anomalies:
                        anomalies.append(cleaned)
    return anomalies


def _check_matches_expected(description, expected_result):
    """簡易判斷截圖描述是否符合預期結果。"""
    desc_lower = description.lower()
    expected_lower = expected_result.lower()

    # 從預期結果提取關鍵詞
    keywords = [w for w in expected_lower.split() if len(w) >= 2]
    if not keywords:
        return None

    matched = sum(1 for k in keywords if k in desc_lower)
    ratio = matched / len(keywords)

    if ratio > 0.5:
        return True
    elif ratio < 0.2:
        return False
    return None
