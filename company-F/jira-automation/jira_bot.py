#!/usr/bin/env python3
"""
jira_bot.py — Jira 互動機器人（CLI + SDK 混用）

定位（重要）:
  本檔 *兼具* CLI 與 SDK 兩種角色：
    - CLI 角色：給人快速開 / 驗票（互動式選單 + --action 模式）
    - SDK 角色：給其他場景 helper（如 jira_ticket_perf_react.py）import 內部函式重用

功能:
  (a) 開票 — 建立 Bug/Task/Epic/Story ticket（自動從報告帶入 FAIL 或手動描述）
  (b) 驗票 — 複驗 Ready for Testing 的票（比對最新報告結果）

公開 export API（可被其他模組 import；簽名變動視為 breaking change）:
  - jql_search(jql, fields)           — 用 v3 API 跑 JQL 查詢，自動分頁
  - create_issue_ext(...)             — 建立 issue（Bug/Task/Epic/Story）
  - validate_description_structure(d) — 驗 description 結構（從 jira_create import）
  - close_issue / reopen_issue / add_comment / transition_issue
  - jql_search 與 create_issue_ext 的下放至 jira_batch.py 是長期目標（待 egret 場景驗證後）

內部函式（_ 開頭，NEVER 跨檔 import）:
  - _check_duplicate_today / _resolve_assignee / _extract_ticket_info ...

使用方式:
  互動模式:      python jira_bot.py
  CLI 開票:      python jira_bot.py --action create --file pa_react_testcases.xlsx
  CLI 開 Epic:   python jira_bot.py --action create --type Epic --file ...
  CLI 驗票:      python jira_bot.py --action verify
  Dry-run:       python jira_bot.py --action create --file pa_react_testcases.xlsx --dry-run

職責邊界（三層架構）:
  - jira_create.py — 低階單票工具，xlsx FAIL → 單 Bug 場景專屬
  - jira_bot.py    — 中層 CLI + 部分 SDK 函式（本檔）
  - jira_batch.py  — 通用批量 SDK，給「Epic + N 子票」批量場景用
  + 場景 helper（jira_ticket_perf_react.py 等）只放事實內容 + orchestration

需求套件:
  pip install requests openpyxl python-dotenv

設定:
  複製 .env.example 為 .env，填入 Jira 連線資訊
"""

import argparse
import io
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

# 重用 jira_create.py 的核心功能
from jira_create import (
    JIRA_URL,
    JIRA_EMAIL,
    JIRA_API_TOKEN,
    JIRA_PROJECT_KEY,
    JIRA_COMPONENT,
    JIRA_ASSIGNEE,
    JIRA_FIX_VERSION,
    JIRA_SPRINT_ID,
    _auth,
    attach_screenshot,
    build_description,
    fetch_testing_version,
    find_fail_screenshot,
    resolve_priority,
    validate_env,
)

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# ── 擴充設定（從 .env 讀取）──────────────────────────────────────────────────

# 自己的 Jira accountId（TASK 票指派給自己）
JIRA_SELF_ACCOUNT_ID = os.getenv("JIRA_SELF_ACCOUNT_ID", "")

# Component → Assignee 對應（JSON 格式）
# 例: {"Frontend": "acc_id_1", "Backend": "acc_id_2", "QA": "acc_id_3"}
_COMP_ASSIGNEE_RAW = os.getenv("JIRA_COMPONENT_ASSIGNEE_MAP", "{}")
try:
    COMPONENT_ASSIGNEE_MAP: dict = json.loads(_COMP_ASSIGNEE_RAW)
except json.JSONDecodeError:
    COMPONENT_ASSIGNEE_MAP = {}
    print(f"[WARN] JIRA_COMPONENT_ASSIGNEE_MAP 格式錯誤，使用空對應")

# 驗票用 JQL 的 assignee（預設 jay-su）
JIRA_VERIFY_ASSIGNEE = os.getenv("JIRA_VERIFY_ASSIGNEE", "jay-su")

# ── 色彩常量 ─────────────────────────────────────────────────────────────────

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


# ══════════════════════════════════════════════════════════════════════════════
#  Description 結構驗證
# ══════════════════════════════════════════════════════════════════════════════

def validate_description_structure(description: str) -> list[str]:
    """檢查 Jira ticket description 是否遵循正確的子標題/子內容結構。

    預期結構:
      - "Steps:" — 內容應為編號步驟 (1. 2. 3. ...) 或步驟描述
      - "Actual result:" — 應描述實際發生的情況
      - "Expected result:" — 應描述預期行為
      - "Comment:" — metadata 區塊

    回傳 warnings 清單（空 = 無問題）。
    """
    warnings: list[str] = []

    if not description or not description.strip():
        warnings.append("Description 為空")
        return warnings

    # 定義必須存在的子標題
    required_sections = {
        "Steps:": None,
        "Actual result:": None,
        "Expected result:": None,
        "Comment:": None,
    }

    # 找出各子標題的位置
    for section in required_sections:
        idx = description.find(section)
        if idx == -1:
            warnings.append(f"缺少必要子標題: '{section}'")
        else:
            required_sections[section] = idx

    # 若有缺少的子標題，無法做順序/內容檢查，提前回傳
    if any(v is None for v in required_sections.values()):
        return warnings

    # 檢查子標題順序: Steps < Actual result < Expected result < Comment
    ordered_sections = ["Steps:", "Actual result:", "Expected result:", "Comment:"]
    positions = [required_sections[s] for s in ordered_sections]
    if positions != sorted(positions):
        warnings.append("子標題順序錯誤，預期: Steps → Actual result → Expected result → Comment")

    # 提取各區塊內容並驗證非空
    section_pairs = list(zip(ordered_sections, ordered_sections[1:]))
    for section, next_section in section_pairs:
        start = required_sections[section] + len(section)
        end = required_sections[next_section]
        content = description[start:end].strip()
        if not content or content in ("-", "null", '""', "N/A"):
            warnings.append(f"'{section}' 內容為空或無意義")

    # Comment 區塊（到結尾）
    comment_start = required_sections["Comment:"] + len("Comment:")
    comment_content = description[comment_start:].strip()
    if not comment_content or comment_content in ("-", "null", '""'):
        warnings.append("'Comment:' 內容為空或無意義")

    # 檢查 Steps 內容是否包含步驟 (數字編號或步驟描述)
    steps_start = required_sections["Steps:"] + len("Steps:")
    steps_end = required_sections["Actual result:"]
    steps_content = description[steps_start:steps_end].strip()
    if steps_content and not re.search(r'\d+[\.\)、]', steps_content):
        warnings.append("'Steps:' 內容未包含編號步驟 (預期 1. 2. 3. 等格式)")

    # 檢查內容錯置: Steps 區塊不應包含 "Actual result" 或 "Expected result" 的特徵
    if steps_content:
        if re.search(r'(?:actual|expected)\s+result', steps_content, re.IGNORECASE):
            warnings.append("'Steps:' 區塊中疑似包含 Actual/Expected result 內容（可能錯置）")

    return warnings


# ══════════════════════════════════════════════════════════════════════════════
#  開票前置檢查
# ══════════════════════════════════════════════════════════════════════════════

def check_xlsx_locked(xlsx_path: str) -> bool:
    """檢查 xlsx 是否被其他程式鎖定。回傳 True = 可用，False = 被鎖定。"""
    try:
        with open(xlsx_path, "r+b"):
            pass
        return True
    except (PermissionError, OSError):
        return False


def check_excel_html_sync(xlsx_path: str, html_path: str = "") -> list[str]:
    """比對 xlsx 與 HTML 報告的 TC 結果是否一致。

    回傳不一致的項目清單（空 = 一致）。
    """
    import openpyxl
    import html as _html_mod

    if not html_path:
        html_path = os.path.join(os.path.dirname(xlsx_path) or ".", "react_pa_test_report.html")

    if not os.path.exists(html_path):
        return [f"HTML 報告不存在: {html_path}"]

    # 讀取 xlsx 結果
    wb = openpyxl.load_workbook(xlsx_path, read_only=True)
    ws = wb.active
    headers = [str(c.value).strip() if c.value else "" for c in ws[1]]
    xlsx_results = {}
    for row_cells in ws.iter_rows(min_row=2):
        row = {}
        for i, hdr in enumerate(headers):
            row[hdr] = row_cells[i].value if i < len(row_cells) else None
        tc_id = str(row.get("Test ID") or "").strip()
        result = str(row.get("執行結果") or "").strip().upper()
        if tc_id and result:
            xlsx_results[tc_id] = result
    wb.close()

    # 讀取 HTML 結果
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    html_results = {}
    tr_blocks = re.findall(r'<tr[^>]*>(.*?)</tr>', html_content, re.DOTALL)
    for block in tr_blocks:
        tds = re.findall(r'<td[^>]*>(.*?)</td>', block, re.DOTALL)
        if len(tds) < 5:
            continue
        tid = _html_mod.unescape(tds[1].strip()) if len(tds) > 1 else ""
        if not re.match(r'(TC|CTC|<PRODUCT>-TC|STREAM-TC)-\d+', tid):
            continue
        status_m = re.search(r'class="badge (\w+)"', tds[4] if len(tds) > 4 else "")
        if status_m:
            html_results[tid] = status_m.group(1).upper()

    # 比對
    diffs = []
    for tc_id, xlsx_val in xlsx_results.items():
        html_val = html_results.get(tc_id)
        if html_val and xlsx_val != html_val:
            diffs.append(f"  {tc_id}: Excel={xlsx_val}, HTML={html_val}")

    return diffs


def pre_create_checks(xlsx_path: str) -> bool:
    """開票前置檢查（硬擋）。回傳 True = 通過，False = 中止。"""
    print(f"\n  {BOLD}[前置檢查]{RESET}\n")

    # 1. Excel 鎖定檢查
    if not check_xlsx_locked(xlsx_path):
        print(f"  {RED}✗ Excel 被鎖定{RESET} — 請先關閉 {xlsx_path} 再執行")
        return False
    print(f"  {GREEN}✓{RESET} Excel 未鎖定")

    # 2. Excel / HTML 同步檢查
    diffs = check_excel_html_sync(xlsx_path)
    if diffs:
        print(f"  {RED}✗ Excel 與 HTML 報告不一致:{RESET}")
        for d in diffs:
            print(f"    {d}")
        print(f"\n  請先重新產生報告確保同步，再執行開票。")
        return False
    print(f"  {GREEN}✓{RESET} Excel 與 HTML 報告一致")

    print()
    return True


# ══════════════════════════════════════════════════════════════════════════════
#  開票功能（擴充版：支援 TASK / BUG 分流 + Component → Assignee 對應）
# ══════════════════════════════════════════════════════════════════════════════

def _resolve_assignee(issue_type: str, component: str = "") -> str:
    """依票型和 component 決定 assignee。

    - TASK → 自己 (JIRA_SELF_ACCOUNT_ID)
    - BUG  → 依 component 對應表，找不到用預設 JIRA_ASSIGNEE
    """
    if issue_type.upper() == "TASK":
        return JIRA_SELF_ACCOUNT_ID or JIRA_ASSIGNEE

    # BUG: 查 component → assignee 對應
    comp = str(component or "").strip()
    if comp and comp in COMPONENT_ASSIGNEE_MAP:
        return COMPONENT_ASSIGNEE_MAP[comp]

    return JIRA_ASSIGNEE


def _check_duplicate_today(summary: str) -> str | None:
    """查詢今天是否已有相同摘要的票。有則回傳 Issue Key，無則回傳 None。

    內部走 v3 jql_search（v2 /rest/api/2/search 已 deprecated 回 410 Gone）。

    Note: jql_search 定義在本檔下方（grep `def jql_search`），這是 forward
          reference，Python 動態 lookup 沒問題（runtime 才查 jql_search），但
          IDE static analyzer 可能標警告。下次大重構時把通用函式集中前置。
    """
    from datetime import date
    today = date.today().strftime("%Y-%m-%d")
    jql = (
        f'project = "{JIRA_PROJECT_KEY}" '
        f'AND summary ~ "\\"{summary}\\"" '
        f'AND created >= "{today}"'
    )
    try:
        issues = jql_search(jql, fields="summary")
        if issues:
            return issues[0]["key"]
    except Exception as e:
        print(f"  [WARN] 查重失敗: {e}")
    return None


def create_issue_ext(
    summary: str,
    description: str,
    priority: str,
    issue_type: str = "Bug",
    component: str = "",
    assignee_override: str = "",
    parent: str = "",
    sprint_id: str = "",
) -> str:
    """建立 Jira Issue（支援 Bug / Task），回傳 Issue Key。
    建票前自動查重：今天已有相同摘要的票則跳過。

    Args:
        parent: 父票 Issue Key（例: TC_100），設定 Epic Link (customfield_10014)
        sprint_id: Sprint ID（整數字串），覆蓋 .env 的 JIRA_SPRINT_ID
    """
    # 查重：今天同摘要 → 跳過
    dup_key = _check_duplicate_today(summary)
    if dup_key:
        print(f"  [SKIP] 今天已有同名票: {dup_key}，跳過建票")
        return dup_key

    assignee = assignee_override or _resolve_assignee(issue_type, component)

    fields: dict = {
        "project": {"key": JIRA_PROJECT_KEY},
        "summary": summary,
        "description": description,
        "issuetype": {"name": issue_type},
        "priority": {"name": priority},
    }

    comp_name = component or JIRA_COMPONENT
    if comp_name:
        fields["components"] = [{"name": comp_name}]
    if assignee:
        fields["assignee"] = {"accountId": assignee}
    if JIRA_FIX_VERSION:
        fields["fixVersions"] = [{"name": JIRA_FIX_VERSION}]

    # Sprint: CLI 參數 > .env 設定
    effective_sprint = sprint_id or JIRA_SPRINT_ID
    if effective_sprint:
        fields["customfield_10020"] = int(effective_sprint)

    # Parent / Epic Link
    if parent:
        fields["customfield_10014"] = parent

    resp = requests.post(
        f"{JIRA_URL}/rest/api/2/issue",
        json={"fields": fields},
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        auth=_auth(),
    )
    resp.raise_for_status()
    return resp.json()["key"]


def create_tickets_from_xlsx(
    xlsx_path: str,
    screenshots_dir: str,
    dry_run: bool,
    tc_filter: Optional[set] = None,
    issue_type: str = "Bug",
    component: str = "",
    parent: str = "",
    sprint_id: str = "",
    platform: str = "PC",
) -> dict:
    """從 xlsx 開票，回傳統計 dict。"""
    import openpyxl

    # 前置檢查（非 dry-run 時強制執行）
    if not dry_run:
        if not pre_create_checks(xlsx_path):
            return {"created": 0, "skipped": 0, "errors": 0, "not_found": 0}

    testing_version = fetch_testing_version()
    print(f"\nTesting version:\n{testing_version}\n")

    mode_label = "手動" if tc_filter else "自動"
    type_label = f"{issue_type} 票"
    print(f"[{mode_label}模式] 開立 {type_label}")
    if tc_filter:
        print(f"  指定 TC: {', '.join(sorted(tc_filter))}")
    print()

    wb = openpyxl.load_workbook(xlsx_path)
    ws = wb.active

    headers = [str(c.value).strip() if c.value is not None else "" for c in ws[1]]

    JIRA_KEY_COL = "Jira Issue Key"
    if JIRA_KEY_COL not in headers:
        new_col_idx = len(headers) + 1
        ws.cell(row=1, column=new_col_idx).value = JIRA_KEY_COL
        headers.append(JIRA_KEY_COL)
        print(f"[INFO] 新增欄位 '{JIRA_KEY_COL}' 至 {xlsx_path}\n")

    jira_col_idx = headers.index(JIRA_KEY_COL) + 1

    stats = {"created": 0, "skipped": 0, "errors": 0, "not_found": 0}
    tc_filter_remaining = set(tc_filter) if tc_filter else None

    for row_cells in ws.iter_rows(min_row=2):
        row: dict = {}
        for i, hdr in enumerate(headers):
            row[hdr] = row_cells[i].value if i < len(row_cells) else None

        tc_id = str(row.get("Test ID") or "").strip()

        if tc_filter:
            if tc_id not in tc_filter:
                continue
            tc_filter_remaining.discard(tc_id)
        else:
            exec_result = str(row.get("執行結果") or "").strip().upper()
            if exec_result != "FAIL":
                continue

        test_name = str(row.get("測試案例名稱") or "").strip()
        existing = str(row.get(JIRA_KEY_COL) or "").strip()

        if existing:
            print(f"  [SKIP]   {tc_id} — 已有 ticket {existing}")
            stats["skipped"] += 1
            continue

        summary = f"[{platform}] [自動化測試] {test_name}"
        desc = build_description(row, testing_version)
        priority = resolve_priority(row.get("優先級"), row.get("類別"))
        shot = find_fail_screenshot(tc_id, screenshots_dir)

        # 截圖硬擋：沒截圖不開票
        if not shot:
            print(f"  {RED}[NO SCREENSHOT]{RESET} {tc_id} — 沒有截圖，跳過不開票")
            stats["skipped"] += 1
            continue

        # Description 結構驗證（品質門禁，警告但不阻擋）
        desc_warnings = validate_description_structure(desc)
        if desc_warnings:
            print(f"  [WARN]   {tc_id} Description 結構問題:")
            for w in desc_warnings:
                print(f"           - {w}")

        # 決定 component（從 row 取或用全域設定）
        row_component = component or str(row.get("Component") or "").strip()

        print(f"  [CREATE] {tc_id} | {summary}")
        print(f"           Type: {issue_type} | Priority: {priority}")
        assignee_id = _resolve_assignee(issue_type, row_component)
        print(f"           Assignee: {assignee_id[:20]}..." if len(assignee_id) > 20 else f"           Assignee: {assignee_id or '(unassigned)'}")
        if parent:
            print(f"           Parent: {parent}")
        if sprint_id:
            print(f"           Sprint: {sprint_id}")
        print(f"           Screenshot: {Path(shot).name if shot else '(none found)'}")

        if dry_run:
            stats["created"] += 1
            continue

        try:
            key = create_issue_ext(summary, desc, priority, issue_type, row_component,
                                   parent=parent, sprint_id=sprint_id)
            print(f"           → Jira: {key}")

            if shot:
                attach_screenshot(key, shot)
                print(f"           → Attached: {Path(shot).name}")

            ws.cell(row=row_cells[0].row, column=jira_col_idx).value = key
            stats["created"] += 1

        except requests.HTTPError as e:
            body = e.response.text[:300] if e.response else ""
            print(f"  [ERROR]  {tc_id}: HTTP {e.response.status_code} — {body}")
            stats["errors"] += 1
        except Exception as e:
            print(f"  [ERROR]  {tc_id}: {e}")
            stats["errors"] += 1

    if tc_filter_remaining:
        for missing_id in sorted(tc_filter_remaining):
            print(f"  [NOT FOUND] {missing_id} — 在 xlsx 中找不到此 TC ID")
            stats["not_found"] += 1

    if not dry_run:
        wb.save(xlsx_path)
        print(f"\n已儲存: {xlsx_path}")

    parts = [f"建立: {stats['created']}", f"跳過: {stats['skipped']}", f"錯誤: {stats['errors']}"]
    if stats["not_found"]:
        parts.append(f"找不到: {stats['not_found']}")
    print(f"\n完成 — {',  '.join(parts)}")
    if dry_run:
        print("(dry-run 模式 — 未實際建立任何 Jira ticket)")

    return stats


# ══════════════════════════════════════════════════════════════════════════════
#  驗票功能
# ══════════════════════════════════════════════════════════════════════════════

def jql_search(jql: str, fields: str = "summary,status,description,components") -> list:
    """執行 JQL 查詢（v3 API），回傳 issue list。"""
    results = []
    start_at = 0
    max_results = 50

    while True:
        resp = requests.get(
            f"{JIRA_URL}/rest/api/3/search/jql",
            params={
                "jql": jql,
                "startAt": start_at,
                "maxResults": max_results,
                "fields": fields,
            },
            headers={"Accept": "application/json"},
            auth=_auth(),
        )
        resp.raise_for_status()
        data = resp.json()
        results.extend(data.get("issues", []))
        if start_at + max_results >= data.get("total", 0):
            break
        start_at += max_results

    return results


def _extract_ticket_info(description: str) -> dict:
    """從 Jira ticket description 提取 TC ID / Game / Room / Currency。"""
    info = {}

    # Test ID
    m = re.search(r"Test ID:\s*((?:<PRODUCT>-)?(?:CTC-|TC-|STREAM-TC-)\d+)", description or "", re.IGNORECASE)
    if m:
        info["tc_id"] = m.group(1).strip()

    # Game
    m = re.search(r"Game:\s*(.+?)(?:\n|$)", description or "")
    if m:
        info["game"] = m.group(1).strip()

    # Room
    m = re.search(r"Room:\s*(\w+)", description or "")
    if m:
        info["room"] = m.group(1).strip()

    # Currency
    m = re.search(r"Currency:\s*(\w+)", description or "")
    if m:
        info["currency"] = m.group(1).strip().upper()

    # Category
    m = re.search(r"Category:\s*(.+?)(?:\n|$)", description or "")
    if m:
        info["category"] = m.group(1).strip()

    return info


def _load_report_results() -> list:
    """載入所有可用的測試報告結果（xlsx + json）。

    回傳 list of dict，每筆含 tc_id / game / room / currency / result 等欄位。
    """
    results = []

    # 1. 讀取 xlsx 報告
    try:
        import openpyxl
    except ImportError:
        print("[WARN] openpyxl 未安裝，無法讀取 xlsx 報告")
        return results

    xlsx_files = list(Path(".").glob("*_testcases.xlsx")) + list(Path(".").glob("all_currencies*.xlsx"))

    for xlsx_path in xlsx_files:
        try:
            wb = openpyxl.load_workbook(str(xlsx_path), read_only=True)
            ws = wb.active
            headers = [str(c.value).strip() if c.value else "" for c in ws[1]]

            for row_cells in ws.iter_rows(min_row=2):
                row = {}
                for i, hdr in enumerate(headers):
                    row[hdr] = row_cells[i].value if i < len(row_cells) else None

                tc_id = str(row.get("Test ID") or "").strip()
                exec_result = str(row.get("執行結果") or row.get("Result") or "").strip().upper()

                if tc_id and exec_result:
                    results.append({
                        "tc_id": tc_id,
                        "result": exec_result,
                        "game": str(row.get("Game") or row.get("遊戲") or "").strip(),
                        "room": str(row.get("Room") or row.get("房間") or "").strip(),
                        "currency": str(row.get("Currency") or row.get("幣別") or "").strip().upper(),
                        "source": str(xlsx_path),
                        "note": str(row.get("實際結果備註") or row.get("Note") or "").strip(),
                    })
            wb.close()
        except Exception as e:
            print(f"[WARN] 無法讀取 {xlsx_path}: {e}")

    # 2. 讀取 JSON 報告
    json_files = list(Path(".").glob("*_report.json")) + list(Path("shared/report").glob("*_report.json"))
    for json_path in json_files:
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
            findings = data if isinstance(data, list) else data.get("findings", [])
            for f in findings:
                tc_id = str(f.get("tc_id") or f.get("Test ID") or "").strip()
                result = str(f.get("result") or f.get("classification") or "").strip().upper()
                if tc_id and result:
                    results.append({
                        "tc_id": tc_id,
                        "result": result,
                        "game": str(f.get("game") or "").strip(),
                        "room": str(f.get("room") or "").strip(),
                        "currency": str(f.get("currency") or "").strip().upper(),
                        "source": str(json_path),
                        "note": str(f.get("note") or f.get("context") or "").strip(),
                    })
        except Exception as e:
            print(f"[WARN] 無法讀取 {json_path}: {e}")

    return results


def _match_ticket_to_report(ticket_info: dict, report_results: list) -> Optional[dict]:
    """比對 ticket 資訊與報告結果。

    匹配優先序:
      1. TC ID 完全匹配
      2. Game + Room + Currency 組合匹配
    """
    tc_id = ticket_info.get("tc_id", "")

    # 優先: TC ID 匹配
    if tc_id:
        matches = [r for r in report_results if r["tc_id"] == tc_id]
        if matches:
            # 取最新的（list 最後一筆）
            return matches[-1]

    # 次要: Game + Room + Currency 組合
    game = ticket_info.get("game", "")
    room = ticket_info.get("room", "")
    currency = ticket_info.get("currency", "")

    if game and room and currency:
        matches = [
            r for r in report_results
            if r["game"] == game and r["room"] == room and r["currency"] == currency
        ]
        if matches:
            return matches[-1]

    return None


def set_resolution(issue_key: str, resolution: str = "Done") -> bool:
    """設定 issue 的 resolution（必須在 transition 之前呼叫）。"""
    resp = requests.put(
        f"{JIRA_URL}/rest/api/2/issue/{issue_key}",
        json={"fields": {"resolution": {"name": resolution}}},
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        auth=_auth(),
    )
    if resp.status_code == 204:
        return True
    print(f"  [WARN] {issue_key}: 設定 resolution '{resolution}' 失敗: {resp.status_code}")
    return False


def transition_issue(issue_key: str, transition_name: str) -> bool:
    """將 issue 轉換狀態（依 transition_name 精確比對，不區分大小寫）。"""
    resp = requests.get(
        f"{JIRA_URL}/rest/api/2/issue/{issue_key}/transitions",
        headers={"Accept": "application/json"},
        auth=_auth(),
    )
    resp.raise_for_status()
    transitions = resp.json().get("transitions", [])

    # 精確比對 transition name（不區分大小寫）
    target = None
    for t in transitions:
        if t["name"].lower() == transition_name.lower():
            target = t
            break

    if not target:
        available = [t["name"] for t in transitions]
        print(f"  [WARN] {issue_key}: 找不到 '{transition_name}' transition，可用: {available}")
        return False

    resp = requests.post(
        f"{JIRA_URL}/rest/api/2/issue/{issue_key}/transitions",
        json={"transition": {"id": target["id"]}},
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        auth=_auth(),
    )
    resp.raise_for_status()
    return True


def close_issue(issue_key: str, resolution: str = "Done") -> bool:
    """完整關閉流程：先設 resolution → 再 transition 到 Closed。"""
    set_resolution(issue_key, resolution)
    return transition_issue(issue_key, "Closed")


def reopen_issue(issue_key: str) -> bool:
    """將 issue 轉換到 REOPEN 狀態。"""
    return transition_issue(issue_key, "REOPEN")


def add_comment(issue_key: str, body: str, *, skip_duplicate: bool = True) -> bool:
    """在 issue 新增留言。skip_duplicate=True 時，若已有相同內容則跳過。回傳是否實際留言。"""
    if skip_duplicate:
        resp = requests.get(
            f"{JIRA_URL}/rest/api/2/issue/{issue_key}/comment",
            headers={"Accept": "application/json"},
            auth=_auth(),
        )
        if resp.ok:
            for c in resp.json().get("comments", []):
                if c.get("body", "").strip() == body.strip():
                    return False
    resp = requests.post(
        f"{JIRA_URL}/rest/api/2/issue/{issue_key}/comment",
        json={"body": body},
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        auth=_auth(),
    )
    resp.raise_for_status()
    return True


def verify_tickets(dry_run: bool = False) -> dict:
    """驗票主流程：
    1. 抓取 Ready for Testing 票
    2. 批次轉為 In Testing
    3. 比對報告結果
    4. PASS → Closed (with comment)
    5. FAIL → REOPEN (with comment)
    6. 無法比對 → 退回 Ready For Testing
    """
    jql = f'assignee = "{JIRA_VERIFY_ASSIGNEE}" AND status = "Ready for Testing"'
    print(f"\n[驗票] JQL: {jql}\n")

    issues = jql_search(jql)
    if not issues:
        print("  沒有待驗票。")
        return {"total": 0, "passed": 0, "failed": 0, "unmatched": 0}

    print(f"  找到 {len(issues)} 張待驗票：\n")
    for i, iss in enumerate(issues, 1):
        key = iss["key"]
        summary = iss["fields"]["summary"]
        print(f"  ({i}) {key}: {summary}")

    print()

    # 載入報告結果
    report_results = _load_report_results()
    if not report_results:
        print("  [WARN] 找不到任何測試報告結果，無法自動比對。")
        print("         請確認目錄下有 *_testcases.xlsx 或 *_report.json。")
        return {"total": len(issues), "passed": 0, "failed": 0, "unmatched": len(issues)}

    print(f"  已載入 {len(report_results)} 筆報告結果\n")

    # 讀取 testing version
    version_file = Path(os.getenv("TESTING_VERSION_FILE", "testing_version.txt"))
    testing_version = version_file.read_text(encoding="utf-8").strip() if version_file.exists() else "(unknown)"

    # ── Step 1: 批次轉為 In Testing ──
    if not dry_run:
        print(f"  [Step 1] 將 {len(issues)} 張票轉為 In Testing...")
        for iss in issues:
            key = iss["key"]
            try:
                ok = transition_issue(key, "In Testing")
                if ok:
                    print(f"     {CYAN}→ {key} → In Testing{RESET}")
                else:
                    print(f"     {YELLOW}⚠ {key}: 無法轉為 In Testing（可能已在該狀態或 transition 不存在）{RESET}")
            except Exception as e:
                print(f"     {RED}✗ {key}: 轉 In Testing 失敗 — {e}{RESET}")
        print()
    else:
        print(f"  [Step 1] (dry-run) 跳過 In Testing 轉換\n")

    # ── Step 2: 比對報告結果 ──
    stats = {"total": len(issues), "passed": 0, "failed": 0, "unmatched": 0}
    passed_issues = []
    failed_issues = []
    unmatched_issues = []

    for iss in issues:
        key = iss["key"]
        summary = iss["fields"]["summary"]
        desc = iss["fields"].get("description") or ""

        # v3 API 的 description 可能是 ADF (dict) 而非純文字
        if isinstance(desc, dict):
            # 嘗試從 ADF 中提取純文字
            def _extract_adf_text(node) -> str:
                if isinstance(node, str):
                    return node
                if isinstance(node, dict):
                    text = node.get("text", "")
                    children = node.get("content", [])
                    return text + "".join(_extract_adf_text(c) for c in children)
                if isinstance(node, list):
                    return "".join(_extract_adf_text(c) for c in node)
                return ""
            desc = _extract_adf_text(desc)

        ticket_info = _extract_ticket_info(desc)
        match = _match_ticket_to_report(ticket_info, report_results)

        if not match:
            unmatched_issues.append((key, summary, ticket_info))
            stats["unmatched"] += 1
            continue

        if match["result"] in ("PASS", "CONFIRMED", "OK", "SUCCESS"):
            passed_issues.append((key, summary, match))
            stats["passed"] += 1
        else:
            failed_issues.append((key, summary, match))
            stats["failed"] += 1

    # ── Step 3: 輸出比對結果 ──
    if passed_issues:
        print(f"\n  {GREEN}驗證通過（{len(passed_issues)} 張）:{RESET}")
        for key, summary, match in passed_issues:
            print(f"     {key}: {summary}")
            print(f"       報告: {match['result']} | 來源: {match['source']}")

    if failed_issues:
        print(f"\n  {RED}仍未通過（{len(failed_issues)} 張）:{RESET}")
        for key, summary, match in failed_issues:
            print(f"     {key}: {summary}")
            print(f"       報告: {match['result']} | {match.get('note', '')[:80]}")

    if unmatched_issues:
        print(f"\n  {YELLOW}無法自動比對（{len(unmatched_issues)} 張）:{RESET}")
        for key, summary, info in unmatched_issues:
            print(f"     {key}: {summary}")
            print(f"       擷取資訊: {info or '(description 無法解析)'}")

    # ── Step 4: 執行 transition（需使用者確認）──
    action_summary = []
    if passed_issues:
        action_summary.append(f"Close {len(passed_issues)} 張通過的票")
    if failed_issues:
        action_summary.append(f"REOPEN {len(failed_issues)} 張未通過的票")
    if unmatched_issues:
        action_summary.append(f"退回 {len(unmatched_issues)} 張無法比對的票至 Ready For Testing")

    if action_summary and not dry_run:
        print(f"\n  即將執行：")
        for a in action_summary:
            print(f"    - {a}")
        confirm = input(f"\n  確認執行？(y/N): ").strip().lower()
        if confirm == "y":
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 通過 → Closed
            for key, summary, match in passed_issues:
                comment_body = (
                    f"驗證通過\n\n"
                    f"Testing version: {testing_version}\n"
                    f"Testing environment: QA\n"
                    f"驗證方式: AI 自動化複驗（Agent: Ticket Verifier）\n"
                    f"驗證時間: {now}\n"
                    f"對應報告: {match['source']}\n\n"
                    f"※ 本次驗證由 AI 自動執行，如有疑義請重新開啟。"
                )
                try:
                    add_comment(key, comment_body)
                    close_issue(key, resolution="Done")
                    print(f"     {GREEN}✓ {key} → Closed (Resolution: Done){RESET}")
                except Exception as e:
                    print(f"     {RED}✗ {key}: {e}{RESET}")

            # 未通過 → REOPEN
            for key, summary, match in failed_issues:
                comment_body = (
                    f"驗證未通過\n\n"
                    f"Testing version: {testing_version}\n"
                    f"Testing environment: QA\n"
                    f"驗證方式: AI 自動化複驗（Agent: Ticket Verifier）\n"
                    f"驗證時間: {now}\n"
                    f"報告結果: {match['result']} — {match.get('note', '')[:120]}\n"
                    f"對應報告: {match['source']}\n\n"
                    f"※ 本次驗證由 AI 自動執行，問題仍存在，已重新開啟。"
                )
                try:
                    add_comment(key, comment_body)
                    reopen_issue(key)
                    print(f"     {RED}✓ {key} → REOPEN{RESET}")
                except Exception as e:
                    print(f"     {RED}✗ {key}: {e}{RESET}")

            # 無法比對 → 退回 Ready For Testing
            for key, summary, info in unmatched_issues:
                try:
                    transition_issue(key, "Ready For Testing")
                    print(f"     {YELLOW}✓ {key} → Ready For Testing (無法比對，退回){RESET}")
                except Exception as e:
                    print(f"     {RED}✗ {key}: {e}{RESET}")

        else:
            print("  已取消操作。")
            # 退回所有票到 Ready For Testing（因為已經轉到 In Testing）
            print("  將所有票退回 Ready For Testing...")
            for iss in issues:
                key = iss["key"]
                try:
                    transition_issue(key, "Ready For Testing")
                    print(f"     {YELLOW}← {key} → Ready For Testing (已退回){RESET}")
                except Exception:
                    pass
    elif action_summary and dry_run:
        print(f"\n  (dry-run 模式 — 不會實際執行任何 transition)")

    return stats


# ══════════════════════════════════════════════════════════════════════════════
#  自動驗票功能
# ══════════════════════════════════════════════════════════════════════════════

VERIFY_FAIL_COUNT_COL = "驗證失敗次數"
MAX_FAIL_BEFORE_REOPEN = 3


def _collect_tracked_issues(xlsx_path: str) -> list[dict]:
    """從 xlsx 收集所有有 Jira Issue Key 的 TC，回傳 list of dict。"""
    import openpyxl

    wb = openpyxl.load_workbook(xlsx_path, read_only=True)
    ws = wb.active
    headers = [str(c.value).strip() if c.value else "" for c in ws[1]]

    jira_col = "Jira Issue Key"
    if jira_col not in headers:
        wb.close()
        return []

    tracked = []
    for row_cells in ws.iter_rows(min_row=2):
        row = {}
        for i, hdr in enumerate(headers):
            row[hdr] = row_cells[i].value if i < len(row_cells) else None

        issue_key = str(row.get(jira_col) or "").strip()
        tc_id = str(row.get("Test ID") or "").strip()
        if issue_key and tc_id:
            fail_count = 0
            if VERIFY_FAIL_COUNT_COL in headers:
                try:
                    fail_count = int(row.get(VERIFY_FAIL_COUNT_COL) or 0)
                except (ValueError, TypeError):
                    fail_count = 0
            tracked.append({
                "issue_key": issue_key,
                "tc_id": tc_id,
                "fail_count": fail_count,
                "row_num": row_cells[0].row,
            })

    wb.close()
    return tracked


def _query_issue_status(issue_key: str) -> Optional[str]:
    """查詢單張 Jira ticket 的狀態名稱。"""
    try:
        resp = requests.get(
            f"{JIRA_URL}/rest/api/2/issue/{issue_key}",
            params={"fields": "status"},
            headers={"Accept": "application/json"},
            auth=_auth(),
        )
        resp.raise_for_status()
        return resp.json()["fields"]["status"]["name"]
    except Exception as e:
        print(f"  [WARN] 無法查詢 {issue_key} 狀態: {e}")
        return None


def _ensure_verify_count_col(xlsx_path: str) -> None:
    """確保 xlsx 有「驗證失敗次數」欄，沒有就新增。"""
    import openpyxl

    wb = openpyxl.load_workbook(xlsx_path)
    ws = wb.active
    headers = [str(c.value).strip() if c.value else "" for c in ws[1]]

    if VERIFY_FAIL_COUNT_COL not in headers:
        new_col = len(headers) + 1
        ws.cell(row=1, column=new_col).value = VERIFY_FAIL_COUNT_COL
        wb.save(xlsx_path)
        print(f"  [INFO] 新增欄位「{VERIFY_FAIL_COUNT_COL}」至 {xlsx_path}")
    else:
        wb.close()


def _update_verify_count(xlsx_path: str, row_num: int, new_count: int) -> None:
    """更新 xlsx 指定列的驗證失敗次數。"""
    import openpyxl

    wb = openpyxl.load_workbook(xlsx_path)
    ws = wb.active
    headers = [str(c.value).strip() if c.value else "" for c in ws[1]]

    if VERIFY_FAIL_COUNT_COL in headers:
        col_idx = headers.index(VERIFY_FAIL_COUNT_COL) + 1
        ws.cell(row=row_num, column=col_idx).value = new_count
        wb.save(xlsx_path)


def auto_verify_tickets(xlsx_path: str, dry_run: bool = False) -> dict:
    """自動驗票主流程。"""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'═' * 60}")
    print(f"  自動驗票 — {now_str}")
    print(f"{'═' * 60}\n")

    if not dry_run:
        _ensure_verify_count_col(xlsx_path)

    tracked = _collect_tracked_issues(xlsx_path)
    if not tracked:
        print("  [INFO] xlsx 中沒有已開票的 TC，跳過。")
        return {"total": 0, "passed": 0, "failed": 0, "reopened": 0}

    print(f"  [Step 1] 找到 {len(tracked)} 張已開票的 TC\n")

    ready_tickets = []
    for t in tracked:
        status = _query_issue_status(t["issue_key"])
        if status and status.lower() in ("ready for testing", "ready for test"):
            t["status"] = status
            ready_tickets.append(t)
            print(f"    {CYAN}✓{RESET} {t['issue_key']} ({t['tc_id']}) — {status}")
        elif status:
            print(f"    - {t['issue_key']} ({t['tc_id']}) — {status} (跳過)")

    if not ready_tickets:
        print(f"\n  [INFO] 沒有 Ready for Testing 的票，本次跳過。")
        return {"total": 0, "passed": 0, "failed": 0, "reopened": 0}

    print(f"\n  [Step 2] {len(ready_tickets)} 張待驗票\n")

    report_results = _load_report_results()
    if not report_results:
        print("  [WARN] 找不到測試報告結果，無法比對。")
        return {"total": len(ready_tickets), "passed": 0, "failed": 0, "reopened": 0}

    version_path = Path(os.getenv("TESTING_VERSION_FILE", "testing_version.txt"))
    testing_version = version_path.read_text(encoding="utf-8").strip() if version_path.exists() else "(unknown)"

    stats = {"total": len(ready_tickets), "passed": 0, "failed": 0, "reopened": 0}

    for t in ready_tickets:
        key = t["issue_key"]
        tc_id = t["tc_id"]
        fail_count = t["fail_count"]

        ticket_info = {"tc_id": tc_id}
        match = _match_ticket_to_report(ticket_info, report_results)

        if not match:
            print(f"  [SKIP] {key} ({tc_id}) — 報告中找不到對應結果")
            continue

        result = match["result"]

        if result in ("PASS", "CONFIRMED", "OK", "SUCCESS"):
            print(f"  {GREEN}[PASS]{RESET} {key} ({tc_id}) — 驗證通過")
            if not dry_run:
                comment_body = (
                    f"Testing version: {testing_version}\n"
                    f"Testing environment: QA\n"
                    f"驗證方式: AI 自動測試"
                )
                try:
                    add_comment(key, comment_body)
                    close_issue(key, resolution="Done")
                    _update_verify_count(xlsx_path, t["row_num"], 0)
                    print(f"         → Closed (留言已新增)")
                except Exception as e:
                    print(f"         {RED}✗ Close 失敗: {e}{RESET}")
            stats["passed"] += 1

        else:
            new_count = fail_count + 1
            if new_count >= MAX_FAIL_BEFORE_REOPEN:
                print(f"  {RED}[FAIL x{new_count}]{RESET} {key} ({tc_id}) — 連續 {MAX_FAIL_BEFORE_REOPEN} 次未通過 → Reopen")
                if not dry_run:
                    comment_body = (
                        f"Testing version: {testing_version}\n"
                        f"Testing environment: QA\n"
                        f"驗證方式: AI 自動測試\n"
                        f"結果: FAIL（連續 {MAX_FAIL_BEFORE_REOPEN} 次未通過）"
                    )
                    try:
                        add_comment(key, comment_body)
                        reopen_issue(key)
                        _update_verify_count(xlsx_path, t["row_num"], 0)
                        print(f"         → Reopen (計數歸零)")
                    except Exception as e:
                        print(f"         {RED}✗ Reopen 失敗: {e}{RESET}")
                stats["reopened"] += 1
            else:
                print(f"  {YELLOW}[FAIL x{new_count}]{RESET} {key} ({tc_id}) — 等下次排程再驗")
                if not dry_run:
                    _update_verify_count(xlsx_path, t["row_num"], new_count)
                stats["failed"] += 1

    print(f"\n{'─' * 60}")
    print(f"  結果: 通過={stats['passed']}, 未通過={stats['failed']}, Reopen={stats['reopened']}")
    if dry_run:
        print(f"  (dry-run 模式 — 未實際執行任何操作)")
    print(f"{'─' * 60}\n")

    return stats


def auto_verify_schedule(xlsx_path: str, interval_seconds: int = 3600, dry_run: bool = False) -> None:
    """排程模式：每隔 interval_seconds 執行一次自動驗票。"""
    print(f"\n[排程模式] 每 {interval_seconds // 60} 分鐘執行一次自動驗票")
    print(f"  xlsx: {xlsx_path}")
    print(f"  按 Ctrl+C 停止\n")

    while True:
        try:
            auto_verify_tickets(xlsx_path, dry_run=dry_run)
        except Exception as e:
            print(f"\n  [ERROR] 自動驗票執行異常: {e}\n")

        next_run = datetime.now().strftime("%H:%M:%S")
        print(f"  [SCHEDULE] 下次執行: {interval_seconds // 60} 分鐘後 (目前 {next_run})")
        time.sleep(interval_seconds)


# ══════════════════════════════════════════════════════════════════════════════
#  更新票功能
# ══════════════════════════════════════════════════════════════════════════════

def _get_issue_attachments(issue_key: str) -> list[str]:
    """取得 Jira ticket 的附件檔名清單。"""
    try:
        resp = requests.get(
            f"{JIRA_URL}/rest/api/2/issue/{issue_key}",
            params={"fields": "attachment"},
            headers={"Accept": "application/json"},
            auth=_auth(),
        )
        resp.raise_for_status()
        attachments = resp.json()["fields"].get("attachment", [])
        return [a["filename"] for a in attachments]
    except Exception as e:
        print(f"  [WARN] 無法取得 {issue_key} 附件: {e}")
        return []


def update_tickets(xlsx_path: str, screenshots_dir: str, dry_run: bool = False,
                   tc_filter: Optional[set] = None) -> dict:
    """更新既有 ticket：補截圖、更新 Description。"""
    import openpyxl

    print(f"\n{'═' * 60}")
    print(f"  更新票 — 補截圖 / 更新內容")
    print(f"{'═' * 60}\n")

    wb = openpyxl.load_workbook(xlsx_path, read_only=True)
    ws = wb.active
    headers = [str(c.value).strip() if c.value else "" for c in ws[1]]

    jira_col = "Jira Issue Key"
    if jira_col not in headers:
        print("  [INFO] xlsx 中沒有 Jira Issue Key 欄，無票可更新。")
        wb.close()
        return {"updated": 0, "skipped": 0, "errors": 0}

    stats = {"updated": 0, "skipped": 0, "errors": 0}
    updates_needed = []

    for row_cells in ws.iter_rows(min_row=2):
        row = {}
        for i, hdr in enumerate(headers):
            row[hdr] = row_cells[i].value if i < len(row_cells) else None

        tc_id = str(row.get("Test ID") or "").strip()
        issue_key = str(row.get(jira_col) or "").strip()

        if not issue_key or not tc_id:
            continue

        if tc_filter and tc_id not in tc_filter:
            continue

        shot = find_fail_screenshot(tc_id, screenshots_dir)
        if not shot:
            continue

        # 檢查 Jira 是否已有附件
        existing_attachments = _get_issue_attachments(issue_key)
        shot_name = Path(shot).name

        # 如果已有任何截圖附件，跳過
        has_screenshot = any(a.endswith(".png") for a in existing_attachments)
        if has_screenshot:
            print(f"  [SKIP] {issue_key} ({tc_id}) — 已有截圖附件")
            stats["skipped"] += 1
            continue

        updates_needed.append({
            "issue_key": issue_key,
            "tc_id": tc_id,
            "screenshot": shot,
        })

    wb.close()

    if not updates_needed:
        print("  [INFO] 沒有需要補截圖的票。")
        return stats

    print(f"  找到 {len(updates_needed)} 張票需要補截圖：\n")
    for u in updates_needed:
        print(f"    {u['issue_key']} ({u['tc_id']}) → {Path(u['screenshot']).name}")

    if dry_run:
        print(f"\n  (dry-run 模式 — 不實際上傳)")
        return {"updated": len(updates_needed), "skipped": stats["skipped"], "errors": 0}

    print()
    for u in updates_needed:
        try:
            attach_screenshot(u["issue_key"], u["screenshot"])
            print(f"  {GREEN}✓{RESET} {u['issue_key']} — 已補截圖: {Path(u['screenshot']).name}")
            stats["updated"] += 1
        except Exception as e:
            print(f"  {RED}✗{RESET} {u['issue_key']} — 上傳失敗: {e}")
            stats["errors"] += 1

    print(f"\n  完成 — 更新: {stats['updated']}, 跳過: {stats['skipped']}, 錯誤: {stats['errors']}")
    return stats


# ══════════════════════════════════════════════════════════════════════════════
#  互動式選單
# ══════════════════════════════════════════════════════════════════════════════

def interactive_menu():
    """互動式 Jira 機器人選單。"""
    print(f"\n{BOLD}{'═' * 50}{RESET}")
    print(f"{BOLD}  Jira 機器人 — 請選擇操作{RESET}")
    print(f"{'═' * 50}")
    print(f"\n  {CYAN}(a){RESET} 開票 — 建立 Bug / Task ticket")
    print(f"  {CYAN}(b){RESET} 驗票 — 複驗 Ready for Testing 的票")
    print(f"  {CYAN}(c){RESET} 自動驗票 — 排程自動驗票")
    print(f"  {CYAN}(d){RESET} 更新票 — 補截圖 / 更新既有 ticket")
    print(f"  {CYAN}(q){RESET} 離開\n")

    choice = input("  請選擇 (a/b/c/d/q): ").strip().lower()

    if choice == "a":
        interactive_create()
    elif choice == "b":
        interactive_verify()
    elif choice == "c":
        interactive_auto_verify()
    elif choice == "d":
        interactive_update()
    elif choice == "q":
        print("  再見！")
    else:
        print(f"  無效選項: {choice}")


def interactive_create():
    """互動式開票流程。"""
    print(f"\n{BOLD}{'─' * 50}{RESET}")
    print(f"{BOLD}  開票模式{RESET}")
    print(f"{'─' * 50}")

    # Step 1: 選擇票型
    print(f"\n  票型：")
    print(f"  {CYAN}(1){RESET} Bug  — 指派給對應 component 負責人")
    print(f"  {CYAN}(2){RESET} Task — 指派給自己\n")

    type_choice = input("  請選擇 (1/2): ").strip()
    issue_type = "Task" if type_choice == "2" else "Bug"

    # Step 2: 選擇開票模式
    print(f"\n  開票來源：")
    print(f"  {CYAN}(1){RESET} 自動 — 從 xlsx 報告帶入 FAIL 項目")
    print(f"  {CYAN}(2){RESET} 手動 — 指定 TC ID 開票\n")

    mode_choice = input("  請選擇 (1/2): ").strip()

    # Step 3: 選擇 xlsx 檔案
    xlsx_files = sorted(Path(".").glob("*_testcases.xlsx"))
    if not xlsx_files:
        print("\n  [ERROR] 找不到任何 *_testcases.xlsx 檔案")
        return

    print(f"\n  可用報告：")
    for i, f in enumerate(xlsx_files, 1):
        print(f"  {CYAN}({i}){RESET} {f.name}")

    if len(xlsx_files) == 1:
        xlsx_path = str(xlsx_files[0])
        print(f"\n  自動選擇: {xlsx_files[0].name}")
    else:
        file_choice = input(f"\n  請選擇 (1-{len(xlsx_files)}): ").strip()
        try:
            xlsx_path = str(xlsx_files[int(file_choice) - 1])
        except (ValueError, IndexError):
            print("  無效選項")
            return

    # Step 4: Component（Bug 票才問）
    component = ""
    if issue_type == "Bug" and COMPONENT_ASSIGNEE_MAP:
        print(f"\n  可用 Component（影響 Assignee）：")
        comp_list = list(COMPONENT_ASSIGNEE_MAP.keys())
        for i, c in enumerate(comp_list, 1):
            print(f"  {CYAN}({i}){RESET} {c}")
        print(f"  {CYAN}(0){RESET} 使用預設 ({JIRA_COMPONENT or 'none'})\n")

        comp_choice = input("  請選擇: ").strip()
        if comp_choice != "0":
            try:
                component = comp_list[int(comp_choice) - 1]
            except (ValueError, IndexError):
                pass

    # Step 5: Platform
    print(f"\n  平台：")
    print(f"  {CYAN}(1){RESET} PC")
    print(f"  {CYAN}(2){RESET} MB（Mobile Browser）\n")
    platform_choice = input("  請選擇 (1/2，預設 1): ").strip()
    platform = "MB" if platform_choice == "2" else "PC"

    # Step 6: Parent（Epic Link）
    parent = input("\n  父票 Issue Key（Epic Link，例: TC_100，留空跳過）: ").strip()

    # Step 7: Sprint
    sprint_id = input("  Sprint ID（整數，留空跳過）: ").strip()

    # Step 8: TC Filter（手動模式）
    tc_filter = None
    if mode_choice == "2":
        tc_input = input("\n  指定 TC ID（逗號分隔，例: TC_0034,TC_0035）: ").strip()
        if tc_input:
            tc_filter = {t.strip() for t in tc_input.split(",") if t.strip()}

    # Step 9: Dry-run 確認
    dry_run_choice = input("\n  先預覽不送出？(y/N): ").strip().lower()
    dry_run = dry_run_choice == "y"

    # 執行
    if not dry_run and not validate_env():
        return

    create_tickets_from_xlsx(
        xlsx_path=xlsx_path,
        screenshots_dir="screenshots",
        dry_run=dry_run,
        tc_filter=tc_filter,
        issue_type=issue_type,
        component=component,
        parent=parent,
        sprint_id=sprint_id,
        platform=platform,
    )


def interactive_verify():
    """互動式驗票流程。"""
    print(f"\n{BOLD}{'─' * 50}{RESET}")
    print(f"{BOLD}  驗票模式{RESET}")
    print(f"{'─' * 50}")

    dry_run_choice = input("\n  先預覽不 Close？(y/N): ").strip().lower()
    dry_run = dry_run_choice == "y"

    if not dry_run and not validate_env():
        return

    verify_tickets(dry_run=dry_run)


def interactive_auto_verify():
    """互動式自動驗票。"""
    print(f"\n{BOLD}{'─' * 50}{RESET}")
    print(f"{BOLD}  自動驗票模式{RESET}")
    print(f"{'─' * 50}")

    xlsx_files = sorted(Path(".").glob("*_testcases.xlsx"))
    if not xlsx_files:
        print("\n  [ERROR] 找不到任何 *_testcases.xlsx 檔案")
        return

    if len(xlsx_files) == 1:
        xlsx_path = str(xlsx_files[0])
        print(f"\n  自動選擇: {xlsx_files[0].name}")
    else:
        print(f"\n  可用報告：")
        for i, f in enumerate(xlsx_files, 1):
            print(f"  {CYAN}({i}){RESET} {f.name}")
        file_choice = input(f"\n  請選擇 (1-{len(xlsx_files)}): ").strip()
        try:
            xlsx_path = str(xlsx_files[int(file_choice) - 1])
        except (ValueError, IndexError):
            print("  無效選項")
            return

    schedule_choice = input("\n  啟動排程模式？每小時自動執行 (y/N): ").strip().lower()

    if not validate_env():
        return

    if schedule_choice == "y":
        auto_verify_schedule(xlsx_path)
    else:
        auto_verify_tickets(xlsx_path)


def interactive_update():
    """互動式更新票。"""
    print(f"\n{BOLD}{'─' * 50}{RESET}")
    print(f"{BOLD}  更新票模式{RESET}")
    print(f"{'─' * 50}")

    xlsx_files = sorted(Path(".").glob("*_testcases.xlsx"))
    if not xlsx_files:
        print("\n  [ERROR] 找不到任何 *_testcases.xlsx 檔案")
        return

    if len(xlsx_files) == 1:
        xlsx_path = str(xlsx_files[0])
        print(f"\n  自動選擇: {xlsx_files[0].name}")
    else:
        print(f"\n  可用報告：")
        for i, f in enumerate(xlsx_files, 1):
            print(f"  {CYAN}({i}){RESET} {f.name}")
        file_choice = input(f"\n  請選擇 (1-{len(xlsx_files)}): ").strip()
        try:
            xlsx_path = str(xlsx_files[int(file_choice) - 1])
        except (ValueError, IndexError):
            print("  無效選項")
            return

    tc_input = input("\n  指定 TC ID（逗號分隔，留空=全部）: ").strip()
    tc_filter = None
    if tc_input:
        tc_filter = {t.strip() for t in tc_input.split(",") if t.strip()}

    dry_run_choice = input("\n  先預覽不執行？(y/N): ").strip().lower()
    dry_run = dry_run_choice == "y"

    if not dry_run and not validate_env():
        return

    update_tickets(xlsx_path, "screenshots", dry_run=dry_run, tc_filter=tc_filter)


# ══════════════════════════════════════════════════════════════════════════════
#  CLI Entry Point
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    # 修正 Windows 終端 encoding（避免中文 help 訊息亂碼）
    if sys.stdout.encoding and sys.stdout.encoding.lower() not in ('utf-8', 'utf8'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(
        description="Jira 互動機器人 — 開票 + 驗票",
        epilog=(
            "範例:\n"
            "  互動模式:          python jira_bot.py\n"
            "  CLI 開 Bug 票:     python jira_bot.py --action create --file pa_react_testcases.xlsx\n"
            "  CLI 開 Task 票:    python jira_bot.py --action create --file pa_react_testcases.xlsx --type Task\n"
            "  CLI 指定 TC:       python jira_bot.py --action create --file pa_react_testcases.xlsx --tc TC_0034\n"
            "  CLI 指定 Component:python jira_bot.py --action create --file pa_react_testcases.xlsx --component Frontend\n"
            "  CLI 指定父票:      python jira_bot.py --action create --file pa_react_testcases.xlsx --parent TC_100\n"
            "  CLI 指定 Sprint:   python jira_bot.py --action create --file pa_react_testcases.xlsx --sprint 42\n"
            "  CLI 驗票:          python jira_bot.py --action verify\n"
            "  Dry-run:           python jira_bot.py --action create --file pa_react_testcases.xlsx --dry-run"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--action", choices=["create", "verify", "auto-verify", "update"], help="操作：create=開票, verify=驗票, auto-verify=自動驗票, update=更新票（省略=互動選單）")
    parser.add_argument("--file", default="", help="testcases xlsx 路徑（開票用）")
    parser.add_argument("--screenshots", default="screenshots", help="截圖資料夾（預設: screenshots/）")
    parser.add_argument("--tc", default="", help="指定 TC ID，逗號分隔")
    parser.add_argument("--type", default="Bug", choices=["Bug", "Task", "Epic", "Story"], help="票型（預設: Bug）")
    parser.add_argument("--component", default="", help="Component 名稱（影響 Assignee 對應）")
    parser.add_argument("--parent", default="", help="父票 Issue Key（Epic Link，例: TC_100）")
    parser.add_argument("--sprint", default="", help="Sprint ID（整數，覆蓋 .env 設定）")
    parser.add_argument("--platform", default="PC", choices=["PC", "MB"], help="平台（預設: PC）")
    parser.add_argument("--schedule", action="store_true", help="排程模式，每小時自動執行（搭配 auto-verify）")
    parser.add_argument("--interval", type=int, default=3600, help="排程間隔秒數（預設: 3600=1小時）")
    parser.add_argument("--dry-run", action="store_true", help="預覽模式，不實際操作")

    args = parser.parse_args()

    if args.action is None:
        # 互動模式
        interactive_menu()
        return

    if args.action == "create":
        if not args.file:
            print("[ERROR] 開票需要 --file 參數")
            sys.exit(1)

        if not os.path.exists(args.file):
            print(f"[ERROR] 找不到檔案: {args.file}")
            sys.exit(1)

        if not args.dry_run and not validate_env():
            sys.exit(1)

        tc_filter = None
        if args.tc:
            tc_filter = {t.strip() for t in args.tc.split(",") if t.strip()}

        create_tickets_from_xlsx(
            xlsx_path=args.file,
            screenshots_dir=args.screenshots,
            dry_run=args.dry_run,
            tc_filter=tc_filter,
            issue_type=args.type,
            component=args.component,
            parent=args.parent,
            sprint_id=args.sprint,
            platform=args.platform,
        )

    elif args.action == "verify":
        if not args.dry_run and not validate_env():
            sys.exit(1)

        verify_tickets(dry_run=args.dry_run)

    elif args.action == "auto-verify":
        if not args.file:
            print("[ERROR] 自動驗票需要 --file 參數")
            sys.exit(1)
        if not os.path.exists(args.file):
            print(f"[ERROR] 找不到檔案: {args.file}")
            sys.exit(1)
        if not args.dry_run and not validate_env():
            sys.exit(1)

        if args.schedule:
            auto_verify_schedule(args.file, interval_seconds=args.interval, dry_run=args.dry_run)
        else:
            auto_verify_tickets(args.file, dry_run=args.dry_run)

    elif args.action == "update":
        if not args.file:
            print("[ERROR] 更新票需要 --file 參數")
            sys.exit(1)
        if not os.path.exists(args.file):
            print(f"[ERROR] 找不到檔案: {args.file}")
            sys.exit(1)
        if not args.dry_run and not validate_env():
            sys.exit(1)

        tc_filter = None
        if args.tc:
            tc_filter = {t.strip() for t in args.tc.split(",") if t.strip()}

        update_tickets(args.file, args.screenshots, dry_run=args.dry_run, tc_filter=tc_filter)


if __name__ == "__main__":
    main()
