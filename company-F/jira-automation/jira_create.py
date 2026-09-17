#!/usr/bin/env python3
"""
jira_create.py — 自動從 testcases.xlsx 的 FAIL 列建立 Jira Bug Ticket

定位（場景專屬）:
  本檔是 *xlsx → 單 Bug* 流程的低階工具：
    - input：pa_react_testcases.xlsx 的 FAIL 列 + screenshots/ 目錄
    - output：每行 FAIL → 1 張 Bug，附 1 張 fail 截圖
  不適合用在批量 Epic + N 子票場景（請改用 jira_batch.py）。

公開 export API（被 jira_bot.py 等檔 import）:
  - JIRA_URL / JIRA_EMAIL / JIRA_API_TOKEN / JIRA_PROJECT_KEY / JIRA_COMPONENT
    / JIRA_ASSIGNEE / JIRA_FIX_VERSION / JIRA_SPRINT_ID — 從 .env 讀的設定常數
  - _auth() — HTTPBasicAuth 物件
  - attach_screenshot(issue_key, file_path, mime="image/png") — 上傳檔（支援任意 mime）
  - build_description / fetch_testing_version / find_fail_screenshot
  - resolve_priority / validate_env

使用方式:
    python jira_create.py --file pa_react_testcases.xlsx
    python jira_create.py --file pa_react_testcases.xlsx --screenshots ./screenshots
    python jira_create.py --file pa_react_testcases.xlsx --dry-run

職責邊界（三層架構）:
  - jira_create.py — 低階單票工具（本檔，xlsx FAIL 場景專屬）
  - jira_bot.py    — 中層 CLI + 部分 SDK
  - jira_batch.py  — 通用批量 SDK，給「Epic + N 子票」場景

何時用本檔 vs jira_batch:
  - 從 xlsx 一行對應一張 Bug：用本檔（jira_bot --action create 內部會調用）
  - 批量開 Epic + N 子票（事實內容由 caller 寫死，非 xlsx）：用 jira_batch

需求套件:
    pip install requests openpyxl python-dotenv

設定:
    複製 .env.example 為 .env，填入 Jira 連線資訊
"""

import argparse
import difflib
import glob
import io
import os
import sys
from pathlib import Path
from typing import Optional

import openpyxl
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# ── Jira 連線設定（從 .env 讀取，禁止 hardcode）─────────────────────────────
JIRA_URL       = os.getenv("JIRA_URL", "").rstrip("/")
JIRA_EMAIL     = os.getenv("JIRA_EMAIL", "")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN", "")

# ── 每個專案可不同的 Jira 欄位（.env 設定）───────────────────────────────────
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY", "")
JIRA_COMPONENT   = os.getenv("JIRA_COMPONENT", "")    # 留空 = 不設定
JIRA_ASSIGNEE    = os.getenv("JIRA_ASSIGNEE", "")     # Jira accountId
JIRA_FIX_VERSION = os.getenv("JIRA_FIX_VERSION", "")  # Fix version name
JIRA_SPRINT_ID   = os.getenv("JIRA_SPRINT_ID", "")    # Sprint ID（整數字串）

# ── Testing Version 來源（優先順序：BAC Lobby QA Entries → URL → 本地檔 → placeholder）──
BAC_LOBBY_URL = os.getenv("BAC_LOBBY_URL", "")
VERSION_URL   = os.getenv("TESTING_VERSION_URL", "")
VERSION_FILE  = os.getenv("TESTING_VERSION_FILE", "testing_version.txt")

# ── 優先級對應表 ──────────────────────────────────────────────────────────────
_PRIORITY_MAP = {"高": "High", "中": "Medium", "低": "Low"}

# 類別智能覆蓋：安全性強制 High；UI 類最高 Medium
_CAT_FORCE_HIGH   = {"安全性", "Security"}
_CAT_CAP_MEDIUM   = {"文字UI", "圖片UI", "Text UI", "Image UI"}


def resolve_priority(xlsx_priority: str, category: str) -> str:
    base = _PRIORITY_MAP.get(str(xlsx_priority or "").strip(), "Medium")
    cat  = str(category or "").strip()
    if cat in _CAT_FORCE_HIGH:
        return "High"
    if cat in _CAT_CAP_MEDIUM:
        return "Medium"
    return base


# ── Testing Version ───────────────────────────────────────────────────────────

def _print_version_diff(before: str, after: str) -> None:
    """命令列顯示版本異動，變更/新增行以紅色標示。"""
    RED   = "\033[91m"
    RESET = "\033[0m"
    SEP   = "*****"

    before_lines = before.splitlines()
    after_lines  = after.splitlines()

    # 找出 after 中有變動（replace / insert）的行索引
    changed: set[int] = set()
    for tag, _i1, _i2, j1, j2 in difflib.SequenceMatcher(
        None, before_lines, after_lines
    ).get_opcodes():
        if tag != "equal":
            changed.update(range(j1, j2))

    print("\n[VERSION CHANGED]")
    print("before:")
    print("\n".join(before_lines) if before_lines else "(empty)")
    print(SEP)
    print("after:")
    for idx, line in enumerate(after_lines):
        if idx in changed:
            print(f"{RED}{line}{RESET}")
        else:
            print(line)
    print(SEP)


def get_qa_version(url: str) -> str:
    """
    用 Playwright 開啟 BAC Lobby（帶 tss token），點擊 QA Entries 入口，
    擷取最新 entry 中從 '@pa/host' 到 'go to latest entry' 按鈕之前的版本資訊。

    對應頁面操作：
        點選 qa_entries | New QA Entries | (Version Inside)
        → 在最後一個 entry 下方找到版本文字
        → 從 host 那行開始，到 'go to latest entry' 按鈕之前結束
    """
    import re

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise RuntimeError(
            "playwright 未安裝，請執行: pip install playwright && playwright install chromium"
        )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            print("[INFO] 開啟 BAC Lobby 取得版本資訊...")
            page.goto(url, wait_until="domcontentloaded", timeout=15000)
            page.wait_for_timeout(2000)

            # 點擊 QA Entries 入口（含 "qa_entries" 字樣的連結）
            page.get_by_text("qa_entries", exact=False).first.click()
            print("[INFO] 已點擊 QA Entries，等待版本資訊載入...")
            page.wait_for_timeout(2000)

            body_text = page.inner_text("body")

            # 擷取從 "@pa/host" 到 "go to latest entry" 之前的版本資訊
            match = re.search(
                r"(@pa/host\b.*?)(?=go\s+to\s+latest\s+entry)",
                body_text,
                re.DOTALL | re.IGNORECASE,
            )
            if match:
                return match.group(1).strip()

            print("[WARN] 無法比對版本區塊，回傳空字串")
            return ""

        finally:
            browser.close()


def fetch_testing_version() -> str:
    """取得 Testing Version：BAC Lobby QA Entries → URL → 本地檔 → placeholder。

    當從遠端（BAC Lobby / URL）取得版本時，會與本地 testing_version.txt 比對：
    - 有異動：命令列顯示 before/after diff（變更行紅色），並自動回寫檔案
    - 無異動：顯示 [INFO] Testing version unchanged
    """
    version_path = Path(VERSION_FILE)
    local_before = version_path.read_text(encoding="utf-8").strip() \
        if version_path.exists() else ""

    fetched: Optional[str] = None

    if BAC_LOBBY_URL:
        try:
            fetched = get_qa_version(BAC_LOBBY_URL) or None
            if fetched:
                print("[INFO] Testing version fetched via QA Entries page")
        except Exception as e:
            print(f"[WARN] get_qa_version 失敗 ({e})，改用備援方式...")

    if fetched is None and VERSION_URL:
        try:
            resp = requests.get(VERSION_URL, timeout=5)
            resp.raise_for_status()
            fetched = resp.text.strip()
            print(f"[INFO] Testing version fetched from {VERSION_URL}")
        except Exception as e:
            print(f"[WARN] Cannot fetch version URL ({e}), checking local file...")

    if fetched is not None:
        if fetched != local_before:
            _print_version_diff(local_before, fetched)
            version_path.write_text(fetched + "\n", encoding="utf-8")
            print(f"[INFO] testing_version.txt updated")
        else:
            print("[INFO] Testing version unchanged")
        return fetched

    if local_before:
        print(f"[INFO] Testing version loaded from {VERSION_FILE}")
        return local_before

    return "(testing version TBD — update testing_version.txt or set BAC_LOBBY_URL)"


# ── Description 組裝 ──────────────────────────────────────────────────────────

def build_description(row: dict, testing_version: str) -> str:
    def safe(key: str) -> str:
        return str(row.get(key) or "").strip()

    return (
        f"本票由自動化開立\n\n"
        f"Testing version\n{testing_version}\n\n"
        f"Affected platform: PC\n\n"
        f"Steps:\n{safe('測試步驟')}\n\n"
        f"Actual result:\n{safe('實際結果備註')}\n\n"
        f"Expected result:\n{safe('預期結果')}\n\n"
        f"Comment:\n"
        f"Test ID: {safe('Test ID')}\n"
        f"Category: {safe('類別')}\n"
        f"Module: {safe('Module')}\n"
        f"Can_Auto: {safe('Can_Auto')}\n"
        f"Execution Time: {safe('執行時間')}\n"
        f"Screenshot path: {safe('截圖路徑')}\n"
    )


# ── 截圖搜尋 ──────────────────────────────────────────────────────────────────

def find_fail_screenshot(tc_id: str, screenshots_dir: str) -> Optional[str]:
    """回傳該 TC 最新一張 FAIL 截圖路徑，找不到回傳 None。"""
    pattern = os.path.join(screenshots_dir, f"testcase{tc_id}_fail_*.png")
    matches = sorted(glob.glob(pattern))
    return matches[-1] if matches else None


# ── Jira API ──────────────────────────────────────────────────────────────────

def _auth() -> HTTPBasicAuth:
    return HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)


def create_issue(summary: str, description: str, priority: str) -> str:
    """建立 Jira Bug，回傳 Issue Key（例: TC_123）。"""
    fields: dict = {
        "project":     {"key": JIRA_PROJECT_KEY},
        "summary":     summary,
        "description": description,
        "issuetype":   {"name": "Bug"},
        "priority":    {"name": priority},
    }
    if JIRA_COMPONENT:
        fields["components"] = [{"name": JIRA_COMPONENT}]
    if JIRA_ASSIGNEE:
        fields["assignee"] = {"accountId": JIRA_ASSIGNEE}
    if JIRA_FIX_VERSION:
        fields["fixVersions"] = [{"name": JIRA_FIX_VERSION}]
    if JIRA_SPRINT_ID:
        # customfield_10020 為 Jira Cloud 標準 Sprint 欄位，部分實例欄位 ID 可能不同
        fields["customfield_10020"] = int(JIRA_SPRINT_ID)

    resp = requests.post(
        f"{JIRA_URL}/rest/api/2/issue",
        json={"fields": fields},
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        auth=_auth(),
    )
    resp.raise_for_status()
    return resp.json()["key"]


def attach_screenshot(issue_key: str, file_path: str, mime: str = "image/png") -> None:
    """將檔案附加到指定 Jira Issue。

    Args:
        mime: MIME type；default `image/png` 維持向後相容。
              JSON 用 `application/json`、Markdown 用 `text/markdown`、
              純文字用 `text/plain`。
    """
    with open(file_path, "rb") as f:
        resp = requests.post(
            f"{JIRA_URL}/rest/api/2/issue/{issue_key}/attachments",
            headers={"X-Atlassian-Token": "no-check"},
            files={"file": (Path(file_path).name, f, mime)},
            auth=_auth(),
        )
    resp.raise_for_status()


# ── 環境變數驗證 ──────────────────────────────────────────────────────────────

def validate_env() -> bool:
    required = {
        "JIRA_URL":        JIRA_URL,
        "JIRA_EMAIL":      JIRA_EMAIL,
        "JIRA_API_TOKEN":  JIRA_API_TOKEN,
        "JIRA_PROJECT_KEY": JIRA_PROJECT_KEY,
    }
    missing = [k for k, v in required.items() if not v]
    if missing:
        print(f"[ERROR] .env 缺少必填變數: {', '.join(missing)}")
        print("        請複製 .env.example 為 .env 並填入正確值")
        return False
    return True


# ── 主流程 ────────────────────────────────────────────────────────────────────

def process(xlsx_path: str, screenshots_dir: str, dry_run: bool,
            tc_filter: Optional[set] = None, platform: str = "PC") -> None:
    """
    tc_filter: 指定 TC ID 集合（例: {"TC_0034", "TC_0035"}）
               有值 → 只處理這些 TC，略過 FAIL 篩選（人工確認為 BUG）
               None → 處理所有 FAIL 列（自動模式）
    platform: 平台標識（PC / MB）
    """
    testing_version = fetch_testing_version()
    print(f"\nTesting version:\n{testing_version}\n")

    if tc_filter:
        print(f"[手動模式] 指定開票: {', '.join(sorted(tc_filter))}\n")
    else:
        print("[自動模式] 開票所有 FAIL 列\n")

    wb = openpyxl.load_workbook(xlsx_path)
    ws = wb.active

    # 讀取表頭（容忍 None cell）
    headers = [str(c.value).strip() if c.value is not None else "" for c in ws[1]]

    # 確保 "Jira Issue Key" 欄存在
    JIRA_KEY_COL = "Jira Issue Key"
    if JIRA_KEY_COL not in headers:
        new_col_idx = len(headers) + 1
        ws.cell(row=1, column=new_col_idx).value = JIRA_KEY_COL
        headers.append(JIRA_KEY_COL)
        print(f"[INFO] 新增欄位 '{JIRA_KEY_COL}' 至 {xlsx_path}\n")

    jira_col_idx = headers.index(JIRA_KEY_COL) + 1  # openpyxl 1-based

    created = skipped = errors = not_found = 0
    tc_filter_remaining = set(tc_filter) if tc_filter else None

    for row_cells in ws.iter_rows(min_row=2):
        # 建立 header → value dict（欄數不足時補 None）
        row: dict = {}
        for i, hdr in enumerate(headers):
            row[hdr] = row_cells[i].value if i < len(row_cells) else None

        tc_id = str(row.get("Test ID") or "").strip()

        if tc_filter:
            # 手動模式：只處理指定的 TC，不看 執行結果
            if tc_id not in tc_filter:
                continue
            tc_filter_remaining.discard(tc_id)
        else:
            # 自動模式：只處理 FAIL
            exec_result = str(row.get("執行結果") or "").strip().upper()
            if exec_result != "FAIL":
                continue

        test_name = str(row.get("測試案例名稱") or "").strip()
        existing  = str(row.get(JIRA_KEY_COL) or "").strip()

        # 防呆：已開過票則跳過
        if existing:
            print(f"  [SKIP]   {tc_id} — 已有 ticket {existing}")
            skipped += 1
            continue

        summary  = f"[{platform}] [自動化測試] {test_name}"
        desc     = build_description(row, testing_version)
        priority = resolve_priority(row.get("優先級"), row.get("類別"))
        shot     = find_fail_screenshot(tc_id, screenshots_dir)

        # Description 結構驗證（品質門禁，警告但不阻擋）
        try:
            from jira_bot import validate_description_structure
            desc_warnings = validate_description_structure(desc)
            if desc_warnings:
                print(f"  [WARN]   {tc_id} Description 結構問題:")
                for w in desc_warnings:
                    print(f"           - {w}")
        except ImportError:
            pass  # jira_bot 不可用時跳過驗證

        print(f"  [CREATE] {tc_id} | {summary}")
        print(f"           Priority: {priority}")
        print(f"           Screenshot: {Path(shot).name if shot else '(none found)'}")

        if dry_run:
            created += 1
            continue

        try:
            key = create_issue(summary, desc, priority)
            print(f"           → Jira: {key}")

            if shot:
                attach_screenshot(key, shot)
                print(f"           → Attached: {Path(shot).name}")

            # 開票成功後寫回 xlsx
            ws.cell(row=row_cells[0].row, column=jira_col_idx).value = key
            created += 1

        except requests.HTTPError as e:
            body = e.response.text[:300] if e.response else ""
            print(f"  [ERROR]  {tc_id}: HTTP {e.response.status_code} — {body}")
            errors += 1
        except Exception as e:
            print(f"  [ERROR]  {tc_id}: {e}")
            errors += 1

    # 手動模式：提示找不到的 TC ID
    if tc_filter_remaining:
        for missing_id in sorted(tc_filter_remaining):
            print(f"  [NOT FOUND] {missing_id} — 在 xlsx 中找不到此 TC ID")
            not_found += 1

    if not dry_run:
        wb.save(xlsx_path)
        print(f"\n已儲存: {xlsx_path}")

    summary_parts = [f"建立: {created}", f"跳過: {skipped}", f"錯誤: {errors}"]
    if not_found:
        summary_parts.append(f"找不到: {not_found}")
    print(f"\n完成 — {',  '.join(summary_parts)}")
    if dry_run:
        print("(dry-run 模式 — 未實際建立任何 Jira ticket)")


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    # 修正 Windows 終端 encoding（避免中文 help 訊息亂碼）
    if sys.stdout.encoding and sys.stdout.encoding.lower() not in ('utf-8', 'utf8'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(
        description="從 testcases.xlsx 的 FAIL 列自動建立 Jira Bug Ticket",
        epilog=(
            "範例:\n"
            "  自動模式（所有 FAIL）:  python jira_create.py --file pa_react_testcases.xlsx\n"
            "  手動模式（指定 TC）:    python jira_create.py --file pa_react_testcases.xlsx --tc TC_0034\n"
            "  多張手動:              python jira_create.py --file pa_react_testcases.xlsx --tc TC_0034,TC_0035\n"
            "  預覽不開票:            python jira_create.py --file pa_react_testcases.xlsx --dry-run"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--file",        required=True,         help="testcases xlsx 路徑")
    parser.add_argument("--screenshots", default="screenshots", help="截圖資料夾（預設: screenshots/）")
    parser.add_argument("--tc",          default="",            help="指定 TC ID，逗號分隔（例: TC_0034 或 TC_0034,TC_0035）")
    parser.add_argument("--platform",    default="PC", choices=["PC", "MB"], help="平台（預設: PC）")
    parser.add_argument("--dry-run",     action="store_true",   help="預覽模式，不實際建立 ticket")
    args = parser.parse_args()

    if not args.dry_run and not validate_env():
        sys.exit(1)

    if not os.path.exists(args.file):
        print(f"[ERROR] 找不到檔案: {args.file}")
        sys.exit(1)

    # 解析 --tc 參數（支援逗號分隔，自動 strip 空白）
    tc_filter = None
    if args.tc:
        tc_filter = {t.strip() for t in args.tc.split(",") if t.strip()}

    process(args.file, args.screenshots, args.dry_run, tc_filter, platform=args.platform)


if __name__ == "__main__":
    main()
