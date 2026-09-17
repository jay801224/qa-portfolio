"""
Gemini Vision — 圖片/影片分析 → Spec + TC 產生器 + QA 截圖描述

用途：
  1. 將截圖或影片透過 Gemini API 分析，產出結構化 Spec 與 TC 定義。
  2. describe_image() — 單張截圖 → 文字描述（供其他腳本 import）。
  3. compare_images() — 比對兩張截圖差異。

費用控制：預設使用 gemini-2.5-flash（免費額度 500 次/天），內建每日上限。

使用方式：
    # 分析單張截圖
    python gemini_vision.py --image screenshot.png

    # 分析多張截圖
    python gemini_vision.py --image img1.png img2.png img3.png

    # 分析影片（每秒切幀由 Gemini 處理）
    python gemini_vision.py --video gameplay.mp4

    # 指定輸出模式
    python gemini_vision.py --image screenshot.png --mode spec    # 只產 Spec
    python gemini_vision.py --image screenshot.png --mode tc      # 只產 TC
    python gemini_vision.py --image screenshot.png --mode both    # Spec + TC（預設）

    # Dry-run（顯示預估用量，不呼叫 API）
    python gemini_vision.py --image screenshot.png --dry-run

    # 描述單張截圖（import 用法）
    from shared.ai.gemini_vision import describe_image
    desc = describe_image("screenshot.png", context="投注頁面")
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, date
from pathlib import Path

# ---------------------------------------------------------------------------
# Encoding fix for Windows terminal
# ---------------------------------------------------------------------------
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DAILY_CALL_LIMIT = 50  # Pro 免費 tier 安全上限（官方 100 RPD，設 50 留餘裕）
USAGE_LOG_FILE = Path(__file__).parent / ".gemini_usage.json"
ENV_FILE = Path(__file__).parent / ".env"

SPEC_PROMPT = """你是一位資深 QA 測試架構師。請根據提供的截圖/影片，產出一份完整的頁面 Spec（規格書）。

要求：
1. **頁面概述**：這個頁面的用途和目標使用者
2. **UI 元素清單**：列出所有可見的 UI 元素（按鈕、輸入框、文字、圖片、表格等），每個元素包含：
   - 元素類型
   - 顯示文字或描述
   - 推測的功能/用途
   - 可能的互動方式（點擊、輸入、拖拽等）
3. **業務規則（可推測的）**：從畫面中能推斷的業務邏輯
4. **狀態與流程**：頁面可能存在的不同狀態（載入中、空資料、錯誤等）
5. **待確認項目**：無法從截圖確認，需要向 PM 確認的規則或行為

輸出格式為 Markdown，使用繁體中文。
"""

TC_PROMPT = """你是一位資深 QA 自動化測試工程師。請根據提供的截圖/影片，產出測試案例（Test Case）清單。

每個 TC 必須包含：
- **TC ID**：TC-XXXX 格式（從 TC_0001 開始）
- **ISTQB Category**：Functional Suitability / Performance Efficiency / Compatibility / Usability / Reliability / Security / Maintainability / Portability 其中之一
- **類別**：功能互動 / 文字UI / 圖片UI / API / 效能 / 安全性 / SEO / 無障礙 等
- **測試案例名稱**：簡述測試目的
- **測試步驟**：編號步驟
- **預期結果**：明確、可驗證的預期行為
- **優先級**：高 / 中 / 低
- **Can_Auto**：Y（可自動化）/ N（需人工）/ P（部分可自動化）

要求：
1. 盡可能多產 TC，覆蓋正向、反向、邊界情境
2. 包含 UI 驗證、功能互動、錯誤處理、效能、安全性
3. 對於不確定的業務規則，產兩個版本的 TC（各假設一種規則），標記「待確認」

輸出格式為 Markdown 表格，使用繁體中文。
"""

BOTH_PROMPT = """你是一位資深 QA 測試架構師兼自動化測試工程師。請根據提供的截圖/影片，依序產出：

## Part 1: 頁面 Spec（規格書）

要求：
1. **頁面概述**：這個頁面的用途和目標使用者
2. **UI 元素清單**：列出所有可見的 UI 元素，每個包含：元素類型、顯示文字、推測功能、互動方式
3. **業務規則（可推測的）**：從畫面能推斷的業務邏輯
4. **狀態與流程**：不同狀態（載入中、空資料、錯誤等）
5. **待確認項目**：需要向 PM 確認的規則或行為

## Part 2: 測試案例（Test Case）

每個 TC 包含：TC ID（TC-XXXX）、ISTQB Category、類別、名稱、步驟、預期結果、優先級、Can_Auto

要求：
1. 盡可能多產 TC，覆蓋正向、反向、邊界
2. 對不確定的業務規則，產兩個版本 TC 並標記「待確認」
3. 涵蓋 UI、功能、錯誤處理、效能、安全性

輸出格式為 Markdown，使用繁體中文。
"""

QA_SCREENSHOT_PROMPT = """你是一位 QA 測試工程師。請仔細觀察這張截圖，產出精確的文字描述。

要求：
1. **頁面狀態**：目前顯示的頁面/畫面是什麼（URL、標題、遊戲狀態等）
2. **可見 UI 元素**：列出主要的按鈕、文字、表格、彈窗等
3. **異常或標註**：
   - 有無紅框、箭頭、螢光筆等人工標註？標註指向什麼位置？
   - 有無錯誤訊息、警告、console error overlay？
   - 有無 UI 錯位、重疊、截斷、空白異常？
4. **數值與文字**：讀出截圖中可辨識的數字、金額、文字內容
5. **整體判斷**：這張截圖是否呈現 BUG？如果是，簡述問題

輸出格式為純文字（非 Markdown），使用繁體中文，精簡但完整。
"""

MIME_MAP = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".mp4": "video/mp4",
    ".mov": "video/quicktime",
    ".webm": "video/webm",
    ".avi": "video/x-msvideo",
}

# 記憶體快取（同一 process 內不重複呼叫）
_describe_cache: dict[str, str] = {}


def load_env():
    """從 .env 載入設定"""
    config = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, val = line.split("=", 1)
                config[key.strip()] = val.strip()
    return config


def check_daily_usage():
    """檢查今日 API 呼叫次數，回傳 (已用次數, 是否可繼續)"""
    today = date.today().isoformat()
    usage = {"date": today, "count": 0}

    if USAGE_LOG_FILE.exists():
        try:
            data = json.loads(USAGE_LOG_FILE.read_text(encoding="utf-8"))
            if data.get("date") == today:
                usage = data
        except (json.JSONDecodeError, KeyError):
            pass

    return usage["count"], usage["count"] < DAILY_CALL_LIMIT


def increment_usage():
    """增加今日呼叫計數"""
    today = date.today().isoformat()
    usage = {"date": today, "count": 0}

    if USAGE_LOG_FILE.exists():
        try:
            data = json.loads(USAGE_LOG_FILE.read_text(encoding="utf-8"))
            if data.get("date") == today:
                usage = data
        except (json.JSONDecodeError, KeyError):
            pass

    usage["count"] += 1
    USAGE_LOG_FILE.write_text(
        json.dumps(usage, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return usage["count"]


def _get_api_keys(config):
    """取得所有可用的 API key（支援多組）"""
    keys = []
    primary = config.get("GEMINI_API_KEY", "")
    if primary:
        keys.append(primary)
    # 支援 GEMINI_API_KEY_2, _3, _4...
    for i in range(2, 10):
        k = config.get(f"GEMINI_API_KEY_{i}", "")
        if k:
            keys.append(k)
    return keys


def _call_gemini_api(parts, model_name=None):
    """共用 API 呼叫 + key 輪換邏輯。

    Args:
        parts: Gemini API 的 content parts（prompt + 圖片/影片）
        model_name: 模型名稱（預設從 .env 讀取）

    Returns:
        API 回傳的文字內容

    Raises:
        RuntimeError: 所有 key 額度用完
        Exception: 其他 API 錯誤
    """
    import google.generativeai as genai

    config = load_env()
    api_keys = _get_api_keys(config)
    if not api_keys:
        raise RuntimeError("GEMINI_API_KEY 未設定，請編輯 shared/.env")

    if not model_name:
        model_name = config.get("GEMINI_MODEL", "gemini-2.5-flash")

    last_error = None
    for idx, key in enumerate(api_keys):
        try:
            genai.configure(api_key=key)
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(parts)

            used = increment_usage()
            if idx > 0:
                print(f"  Key #{idx + 1} 成功（前 {idx} 組已耗盡）")
            print(f"  今日已用: {used}/{DAILY_CALL_LIMIT} 次")
            return response.text

        except Exception as e:
            last_error = e
            err_msg = str(e)
            if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
                print(f"  Key #{idx + 1} 額度用完，切換下一組...")
                continue
            else:
                raise

    raise RuntimeError(
        f"所有 {len(api_keys)} 組 key 額度都用完了。最後錯誤: {last_error}"
    )


def _load_image_part(file_path):
    """載入單張圖片為 Gemini API part dict。回傳 (part_dict, mime) 或 (None, None)。"""
    path = Path(file_path)
    if not path.exists():
        return None, None
    mime = MIME_MAP.get(path.suffix.lower())
    if not mime:
        return None, None
    return {"mime_type": mime, "data": path.read_bytes()}, mime


def _file_hash(file_path):
    """計算檔案 MD5（用於快取 key）"""
    return hashlib.md5(Path(file_path).read_bytes()).hexdigest()


def _cache_path(file_path):
    """快取檔案路徑: {screenshot}.gemini_cache.json"""
    return Path(file_path).with_suffix(
        Path(file_path).suffix + ".gemini_cache.json"
    )


def describe_image(image_path, context=""):
    """單張截圖 → 文字描述（不存檔，帶快取）。

    Args:
        image_path: 圖片路徑
        context: 額外上下文（如「投注頁面」「聊天室」）

    Returns:
        文字描述字串

    Raises:
        FileNotFoundError: 圖片不存在
        RuntimeError: API 額度用完或 key 未設定
    """
    image_path = str(image_path)
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"圖片不存在: {image_path}")

    # 記憶體快取
    if image_path in _describe_cache:
        return _describe_cache[image_path]

    # 檔案快取
    cache_file = _cache_path(image_path)
    file_md5 = _file_hash(image_path)
    if cache_file.exists():
        try:
            cached = json.loads(cache_file.read_text(encoding="utf-8"))
            if cached.get("md5") == file_md5:
                _describe_cache[image_path] = cached["description"]
                return cached["description"]
        except (json.JSONDecodeError, KeyError):
            pass

    # 額度檢查
    _, can_continue = check_daily_usage()
    if not can_continue:
        raise RuntimeError(
            f"今日 Gemini 額度已用完（{DAILY_CALL_LIMIT}/{DAILY_CALL_LIMIT}）"
        )

    # 組裝 prompt
    prompt = QA_SCREENSHOT_PROMPT
    if context:
        prompt += f"\n\n額外上下文：{context}"

    part, _ = _load_image_part(image_path)
    if part is None:
        raise FileNotFoundError(f"無法載入圖片（格式不支援或不存在）: {image_path}")

    parts = [prompt, part]
    print(f"  [Gemini] 分析截圖: {path.name}")
    description = _call_gemini_api(parts)

    # 寫入快取
    _describe_cache[image_path] = description
    cache_file.write_text(
        json.dumps(
            {"md5": file_md5, "description": description, "context": context},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return description


def compare_images(image_a, image_b, context=""):
    """比對兩張截圖，回傳描述與是否相同問題。

    Args:
        image_a: 第一張圖片路徑（如 Jira 截圖）
        image_b: 第二張圖片路徑（如重現截圖）
        context: 額外上下文

    Returns:
        {
            "image_a_desc": str,
            "image_b_desc": str,
            "same_issue": bool | None,  # None = 無法判斷
        }

    Raises:
        FileNotFoundError: 任一圖片不存在
        RuntimeError: API 額度用完
    """
    desc_a = describe_image(image_a, context=context)
    desc_b = describe_image(image_b, context=context)

    # 簡易文字比對判斷（基於描述中的關鍵異常詞）
    same_issue = None
    keywords_a = {w for w in desc_a.split() if len(w) >= 2}
    keywords_b = {w for w in desc_b.split() if len(w) >= 2}
    if keywords_a and keywords_b:
        overlap = len(keywords_a & keywords_b)
        union = len(keywords_a | keywords_b)
        similarity = overlap / union if union > 0 else 0
        if similarity > 0.4:
            same_issue = True
        elif similarity < 0.15:
            same_issue = False

    return {
        "image_a_desc": desc_a,
        "image_b_desc": desc_b,
        "same_issue": same_issue,
    }


def analyze_with_gemini(file_paths, mode="both", model_name=None):
    """呼叫 Gemini API 分析圖片/影片（支援多組 key 自動切換）"""
    config = load_env()
    if not model_name:
        model_name = config.get("GEMINI_MODEL", "gemini-2.5-flash")

    # 準備 prompt
    prompts = {"spec": SPEC_PROMPT, "tc": TC_PROMPT, "both": BOTH_PROMPT}
    prompt = prompts.get(mode, BOTH_PROMPT)

    # 準備檔案（圖片/影片）
    parts = [prompt]
    for fp in file_paths:
        part, _ = _load_image_part(fp)
        if part is None:
            print(f"WARNING: 無法載入檔案，跳過: {fp}")
            continue
        parts.append(part)
        print(f"  已載入: {Path(fp).name} ({len(part['data']) / 1024:.1f} KB)")

    if len(parts) <= 1:
        print("ERROR: 沒有有效的檔案可分析")
        sys.exit(1)

    print(f"\n呼叫 Gemini API（模型: {model_name}）...")
    print(f"  檔案數: {len(parts) - 1}")
    print(f"  模式: {mode}")

    try:
        return _call_gemini_api(parts, model_name)
    except RuntimeError as e:
        print(f"ERROR: {e}")
        sys.exit(1)


def save_output(content, mode, model_name=None, output_dir=None):
    """儲存分析結果"""
    if not output_dir:
        output_dir = Path(__file__).parent.parent / "react" / "reference"
    else:
        output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 模型標記：gemini-2.5-pro → gemini_pro, gemini-2.5-flash → gemini_flash
    model_tag = "gemini"
    if model_name:
        if "pro" in model_name:
            model_tag = "gemini_pro"
        elif "flash" in model_name:
            model_tag = "gemini_flash"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{model_tag}_{mode}_{timestamp}.md"
    filepath = output_dir / filename

    filepath.write_text(content, encoding="utf-8")
    print(f"\n結果已儲存: {filepath}")
    return filepath


def main():
    parser = argparse.ArgumentParser(
        description="Gemini Vision — 圖片/影片分析 → Spec + TC 產生器"
    )
    parser.add_argument(
        "--image", nargs="+", help="圖片檔案路徑（可多張）"
    )
    parser.add_argument("--video", help="影片檔案路徑")
    parser.add_argument(
        "--mode",
        choices=["spec", "tc", "both"],
        default="both",
        help="輸出模式: spec=只產 Spec, tc=只產 TC, both=兩者（預設）",
    )
    parser.add_argument("--output", help="輸出目錄（預設當前目錄）")
    parser.add_argument("--model", help="指定 Gemini 模型（覆蓋 .env）")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="預覽模式，不呼叫 API",
    )

    args = parser.parse_args()

    # 收集檔案
    files = []
    if args.image:
        files.extend(args.image)
    if args.video:
        files.append(args.video)

    if not files:
        parser.error("請提供 --image 或 --video 參數")

    # 檢查用量
    used, can_continue = check_daily_usage()
    print(f"Gemini Vision Analyzer")
    print(f"{'=' * 40}")
    print(f"今日已用: {used}/{DAILY_CALL_LIMIT} 次")
    print(f"待分析檔案: {len(files)} 個")
    print(f"模式: {args.mode}")

    if not can_continue:
        print(f"\nERROR: 今日免費額度已用完（{used}/{DAILY_CALL_LIMIT}）")
        print("明天再試，或在 .env 改用 gemini-2.5-pro（付費）")
        sys.exit(1)

    # Dry-run
    if args.dry_run:
        print(f"\n[DRY-RUN] 預估用量:")
        print(f"  API 呼叫: 1 次")
        print(f"  呼叫後剩餘: {DAILY_CALL_LIMIT - used - 1} 次")
        for f in files:
            p = Path(f)
            if p.exists():
                size = p.stat().st_size / 1024
                print(f"  {p.name}: {size:.1f} KB")
            else:
                print(f"  {p.name}: 檔案不存在")
        print("\n未呼叫 API，結束。")
        return

    # 執行分析
    result = analyze_with_gemini(files, args.mode, args.model)

    # 輸出
    print(f"\n{'=' * 40}")
    print(result)
    print(f"{'=' * 40}")

    # 儲存（帶模型名）
    config = load_env()
    actual_model = args.model or config.get("GEMINI_MODEL", "gemini-2.5-pro")
    save_output(result, args.mode, actual_model, args.output)


if __name__ == "__main__":
    main()
