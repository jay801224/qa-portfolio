"""
jira_batch.py — 批量 Jira 操作通用層（SDK）

定位：
    - jira_create.py：低階「單票 + 截圖」工具，主要服務 xlsx FAIL 流程
    - jira_bot.py：中層 CLI（xlsx 開票 / 驗票 / 自動驗票 / 更新票）
    - jira_batch.py：**通用批量 SDK**，給「批量 Epic + N 子票」場景用
                    （Performance Testing 等跨技術棧效能立案、跨平台批量回報等）

職責邊界：
    - jira_batch 只提供原子函式：create / update / attach / rename / verify
    - 不寫死任何 BUG description / 場景知識；那些屬於 caller（場景 helper）
    - caller 負責 load_dotenv + 餵 hardcoded content 進來

何時用 attach_evidence vs jira_create.attach_screenshot：
    - attach_evidence：批量上傳 N 張票 × M 個檔，支援 rename（避免 trial_1/lobby.json
      與 trial_2/lobby.json 同名衝突）+ 自動 mime 推導 + skip_existing 重複檢測
    - attach_screenshot：單檔上傳，無 rename 能力，default mime=image/png
      （適合 xlsx FAIL → 1 張 fail screenshot 場景）
    - 簡單原則：要 rename 或一張票對多附件 → attach_evidence；
                xlsx FAIL 一對一 → attach_screenshot

使用模式（典型 caller — react/performance/browser/jira_ticket_perf_react.py）：

    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
    load_dotenv(ROOT / "react" / ".env", override=True)

    from shared.jira import jira_batch

    result = jira_batch.create_epic_with_subtasks(
        epic_summary="(自動化測試) Performance Testing",
        epic_description="<wiki markup>",
        subtasks=[
            {"tag": "B1", "summary": "...", "description": "...", "priority": "High"},
            ...
        ],
        state_dir=Path(".claude/_state"),  # 跨步驟通信
        assignee="712020:37d58e68-...",
    )
    # result: {"epic": "TC_2972", "B1": "TC_2973", ...}

    jira_batch.attach_evidence(
        issue_keys=["TC_2973", "TC_2974", ...],
        files=[Path("trial_1/lobby.json"), ...],
        rename_prefix="trial_1_",  # 避免同名衝突
    )
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import requests

# 從 jira_create 借 .env-loaded constants 與 _auth
from jira_create import (
    JIRA_URL,
    JIRA_PROJECT_KEY,
    _auth,
    attach_screenshot,
)
# 從 jira_bot 借 jql_search（v3）與 create_issue_ext
from jira_bot import jql_search, create_issue_ext


# ── MIME 對照表（caller 不傳 mime 時用副檔名猜）────────────────────────────────
_MIME_BY_EXT = {
    ".json": "application/json",
    ".md":   "text/markdown",
    ".txt":  "text/plain",
    ".log":  "text/plain",
    ".csv":  "text/csv",
    ".html": "text/html",
    ".png":  "image/png",
    ".jpg":  "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif":  "image/gif",
    ".pdf":  "application/pdf",
    ".zip":  "application/zip",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}


def _guess_mime(path: Path) -> str:
    return _MIME_BY_EXT.get(path.suffix.lower(), "application/octet-stream")


# ════════════════════════════════════════════════════════════════════════════
# Issue CRUD
# ════════════════════════════════════════════════════════════════════════════

def get_issue_fields(issue_key: str, fields: list[str] | None = None) -> dict[str, Any]:
    """GET /rest/api/2/issue/{key}，回傳 fields dict。"""
    params = {}
    if fields:
        params["fields"] = ",".join(fields)
    resp = requests.get(
        f"{JIRA_URL}/rest/api/2/issue/{issue_key}",
        params=params,
        headers={"Accept": "application/json"},
        auth=_auth(),
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json().get("fields", {})


def update_issue_description(
    issue_key: str,
    new_description: str,
    verify_contains: list[str] | None = None,
) -> bool:
    """PUT 更新 description；可選 verify_contains 驗回確認指定字串都進去。"""
    resp = requests.put(
        f"{JIRA_URL}/rest/api/2/issue/{issue_key}",
        json={"fields": {"description": new_description}},
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        auth=_auth(),
        timeout=10,
    )
    resp.raise_for_status()

    if verify_contains:
        f = get_issue_fields(issue_key, ["description"])
        desc = f.get("description") or ""
        for s in verify_contains:
            if s not in desc:
                print(f"  [FAIL] description 缺 {s!r}")
                return False
    return True


def rename_issue_summary(issue_key: str, new_summary: str) -> bool:
    """PUT 改 summary + GET 驗回。"""
    resp = requests.put(
        f"{JIRA_URL}/rest/api/2/issue/{issue_key}",
        json={"fields": {"summary": new_summary}},
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        auth=_auth(),
        timeout=10,
    )
    resp.raise_for_status()

    f = get_issue_fields(issue_key, ["summary"])
    if f.get("summary") != new_summary:
        print(f"  [FAIL] 改名驗回 mismatch: 預期 {new_summary!r} 實際 {f.get('summary')!r}")
        return False
    return True


def list_attachments(issue_key: str) -> list[dict[str, Any]]:
    """讀 issue 既有附件清單。"""
    f = get_issue_fields(issue_key, ["attachment"])
    return f.get("attachment", []) or []


# ════════════════════════════════════════════════════════════════════════════
# 批量 Epic + 子票
# ════════════════════════════════════════════════════════════════════════════

def create_epic_with_subtasks(
    epic_summary: str,
    epic_description: str,
    subtasks: list[dict[str, Any]],
    *,
    project_key: str | None = None,
    state_dir: Path | None = None,
    assignee: str | None = None,
    epic_priority: str = "Medium",
    dry_run: bool = False,
) -> dict[str, str]:
    """開 1 Epic + N 子票，每張立刻 GET 驗回。回傳 {"epic": <key>, <tag>: <key>, ...}。

    Args:
        epic_summary: Epic 標題
        epic_description: Epic 內文（wiki markup）
        subtasks: list of dict，每個含：
            tag (必填，識別用)、summary (必填)、description (必填)、priority (必填)
            issue_type (選填，default "Bug")
        project_key: 預設讀 .env 的 JIRA_PROJECT_KEY
        state_dir: 若給，會在 state_dir/epic_key 與 state_dir/sub_keys.json 寫入結果，
                   重跑時可從 state 續跑（避免重複建票）
        assignee: accountId
        dry_run: 只列計畫不實際呼叫 API

    Raises:
        Exception: 任何步驟錯誤都 raise，caller 自己決定要不要 retry
    """
    pk = project_key or JIRA_PROJECT_KEY
    keys: dict[str, str] = {}

    # ── 1. Epic 開立前查重（同名 Epic）──
    # Epic 查重用完整 summary（與下方子票查重一致策略）
    escaped_epic = epic_summary.replace('"', '\\"')
    epic_jql = f'project = {pk} AND issuetype = Epic AND summary ~ "\\"{escaped_epic}\\""'
    print(f"[batch] Epic 查重 JQL: {epic_jql}")
    existing = jql_search(epic_jql, fields="summary,status")  # 無結果回 []，if existing 判 False
    if existing:
        print(f"[batch] 已有同名 Epic，跳過建立：")
        for e in existing:
            print(f"  - {e['key']:10s} [{e['fields']['status']['name']}] {e['fields']['summary']}")
        keys["epic"] = existing[0]["key"]
    else:
        if dry_run:
            print(f"[batch][dry-run] 將建 Epic: {epic_summary}")
            keys["epic"] = "<EPIC-DRY-RUN>"
        else:
            print(f"[batch] 建立 Epic: {epic_summary}")
            keys["epic"] = create_issue_ext(
                summary=epic_summary,
                description=epic_description,
                priority=epic_priority,
                issue_type="Epic",
                assignee_override=assignee or "",
            )
            # 立刻 GET 驗回
            f = get_issue_fields(keys["epic"], ["summary", "issuetype", "project"])
            assert f["summary"] == epic_summary, f"Epic summary mismatch: {f['summary']!r}"
            assert f["issuetype"]["name"] == "Epic", f"Epic issuetype mismatch"
            assert f["project"]["key"] == pk, f"Epic project mismatch"
            print(f"[batch] Epic 驗證通過: {keys['epic']}")

    # 寫 state
    if state_dir and not dry_run:
        state_dir.mkdir(parents=True, exist_ok=True)
        (state_dir / "epic_key").write_text(keys["epic"], encoding="utf-8")

    # ── 2. 開 N 子票，每張查重 + 驗回 ──
    for st in subtasks:
        tag = st["tag"]
        summary = st["summary"]
        description = st["description"]
        priority = st["priority"]
        issue_type = st.get("issue_type", "Bug")

        # 子票查重（用完整 summary，不截斷）
        # 注意：JQL `summary ~ "..."` 是 Lucene fuzzy match，雙引號內容需 \-escape
        # 避免引號破壞 JQL 語法。前 N 字截斷曾被考慮但會誤判（前綴相同的 BUG
        # 會互相 SKIP），實測 5 張 BUG 前 40 字都是「(自動化測試) React|PC - UAT 大廳」
        # 完全相同，截斷會導致只開第一張。
        escaped_summary = summary.replace('"', '\\"')
        sub_jql = (
            f'project = {pk} AND summary ~ "\\"{escaped_summary}\\""'
        )
        existing = jql_search(sub_jql, fields="summary")
        if existing:
            keys[tag] = existing[0]["key"]
            print(f"[batch] [{tag}] 同名票已存在: {keys[tag]}（跳過建立）")
            continue

        if dry_run:
            print(f"[batch][dry-run] [{tag}] 將建 {issue_type}: {summary[:60]}")
            keys[tag] = f"<{tag}-DRY-RUN>"
            continue

        print(f"[batch] [{tag}] 建立 {issue_type}（priority={priority}）")
        try:
            issue_key = create_issue_ext(
                summary=summary,
                description=description,
                priority=priority,
                issue_type=issue_type,
                parent=keys["epic"],  # customfield_10014 設 Epic Link
                assignee_override=assignee or "",
            )
            keys[tag] = issue_key

            # 立刻 GET 驗回
            f = get_issue_fields(
                issue_key,
                ["summary", "issuetype", "priority", "customfield_10014"],
            )
            epic_link = f.get("customfield_10014")
            assert f["issuetype"]["name"] == issue_type
            assert f["priority"]["name"] == priority
            if epic_link != keys["epic"]:
                print(f"  [WARN] [{tag}] Epic Link 不對：預期 {keys['epic']} 實際 {epic_link}")
            else:
                print(f"  [OK] [{tag}] {issue_key} 驗證通過")
        except Exception as e:
            # 已開的 keys 寫入 state 後再 raise（避免 caller 重跑時又開一遍）
            if state_dir and not dry_run:
                _save_subtask_keys(state_dir, keys)
            raise

    # 寫 state
    if state_dir and not dry_run:
        _save_subtask_keys(state_dir, keys)

    return keys


def _save_subtask_keys(state_dir: Path, keys: dict[str, str]) -> None:
    state_dir.mkdir(parents=True, exist_ok=True)
    (state_dir / "sub_keys.json").write_text(
        json.dumps({k: v for k, v in keys.items() if k != "epic"}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def update_existing_epic(
    epic_key: str,
    subtasks: list[dict[str, Any]],
    *,
    project_key: str | None = None,
    state_dir: Path | None = None,
    assignee: str | None = None,
    epic_description_append: str | None = None,
    dry_run: bool = False,
) -> dict[str, str]:
    """掛 N 子票到既有 Epic 下（不建新 Epic）。回傳 {"epic": <epic_key>, <tag>: <key>, ...}。

    對應原 plan F9 backlog — 為 Egret 階段把 BUG 票掛 React 階段已開的 TC_2972 Epic 下而設計。

    Args:
        epic_key: 既有 Epic key（如 "TC_2972"）。會 GET 驗證存在。
        subtasks: 同 create_epic_with_subtasks 的 subtasks 格式
        project_key: 預設讀 .env JIRA_PROJECT_KEY
        state_dir: 寫 sub_keys.json（不寫 epic_key 因為已存在）
        assignee: accountId
        epic_description_append: 若非 None，會 GET 既有 description → append 此字串 →
                                 update_issue_description（**append 模式不覆寫**）
        dry_run: 只列計畫不呼 API

    Raises:
        AssertionError: Epic 不存在 / 不是 Epic type
    """
    pk = project_key or JIRA_PROJECT_KEY
    keys: dict[str, str] = {"epic": epic_key}

    # ── 1. 驗 Epic 存在且 type=Epic ──
    f = get_issue_fields(epic_key, ["summary", "issuetype", "project"])
    assert f["issuetype"]["name"] == "Epic", (
        f"{epic_key} 不是 Epic（實際 {f['issuetype']['name']}）"
    )
    assert f["project"]["key"] == pk, (
        f"{epic_key} 不在 project {pk}（實際 {f['project']['key']}）"
    )
    print(f"[batch] 既有 Epic 驗證通過: {epic_key} — {f['summary']}")

    # ── 2. 開 N 子票（reuse create_epic_with_subtasks 的邏輯）──
    for st in subtasks:
        tag = st["tag"]
        summary = st["summary"]
        description = st["description"]
        priority = st["priority"]
        issue_type = st.get("issue_type", "Bug")

        # 子票查重
        escaped_summary = summary.replace('"', '\\"')
        sub_jql = f'project = {pk} AND summary ~ "\\"{escaped_summary}\\""'
        existing = jql_search(sub_jql, fields="summary")
        if existing:
            keys[tag] = existing[0]["key"]
            print(f"[batch] [{tag}] 同名票已存在: {keys[tag]}（跳過建立）")
            continue

        if dry_run:
            print(f"[batch][dry-run] [{tag}] 將建 {issue_type}: {summary[:60]}")
            keys[tag] = f"<{tag}-DRY-RUN>"
            continue

        print(f"[batch] [{tag}] 建立 {issue_type}（priority={priority}）掛 {epic_key} 下")
        try:
            issue_key = create_issue_ext(
                summary=summary,
                description=description,
                priority=priority,
                issue_type=issue_type,
                parent=epic_key,  # customfield_10014 設 Epic Link
                assignee_override=assignee or "",
            )
            keys[tag] = issue_key

            # 立刻 GET 驗回
            f2 = get_issue_fields(
                issue_key,
                ["summary", "issuetype", "priority", "customfield_10014"],
            )
            epic_link = f2.get("customfield_10014")
            assert f2["issuetype"]["name"] == issue_type
            assert f2["priority"]["name"] == priority
            if epic_link != epic_key:
                print(f"  [WARN] [{tag}] Epic Link 不對：預期 {epic_key} 實際 {epic_link}")
            else:
                print(f"  [OK] [{tag}] {issue_key} 驗證通過")
        except Exception:
            if state_dir and not dry_run:
                _save_subtask_keys(state_dir, keys)
            raise

    # ── 3. 寫 state（不寫 epic_key，因為已存在）──
    if state_dir and not dry_run:
        _save_subtask_keys(state_dir, keys)

    # ── 4. 可選：append Epic description ──
    if epic_description_append and not dry_run:
        existing_desc = (
            get_issue_fields(epic_key, ["description"]).get("description") or ""
        )
        new_desc = existing_desc + "\n\n" + epic_description_append
        ok = update_issue_description(epic_key, new_desc, verify_contains=[
            epic_description_append[:50].strip(),
        ])
        if ok:
            print(f"[batch] Epic {epic_key} description appended（{len(new_desc)} chars）")
        else:
            print(f"[batch] [WARN] Epic {epic_key} description append 驗回失敗")

    return keys


# ════════════════════════════════════════════════════════════════════════════
# 批量附件
# ════════════════════════════════════════════════════════════════════════════

def attach_evidence(
    issue_keys: list[str],
    files: list[Path] | list[tuple[Path, str]],
    *,
    rename_prefix_per_dir: bool = True,
    skip_existing: bool = True,
) -> dict[str, list[str]]:
    """批量上傳 files 到每個 issue。

    為什麼不走 jira_create.attach_screenshot：
        attach_screenshot 用 `Path(file_path).name` 寫死作為 Jira 附件名，
        無法 rename。本函式需要把 trial_1/lobby.json 和 trial_2/lobby.json 同時
        上傳到同一張票（兩個都叫 lobby.json 會 Jira 內部衝突），所以必須能 rename。
        TODO（egret 場景再評估）：把 attach_screenshot 加 display_name 參數，
        讓本函式的 multipart 邏輯統一改走 attach_screenshot。

    Args:
        files: list of Path 或 (Path, mime_override) tuple；mime 不給則自動猜
        rename_prefix_per_dir: True → 把檔案的父資料夾名 prepend 到附件名
                              （避免 trial_1/lobby.json 跟 trial_2/lobby.json 衝突）
        skip_existing: True → 同名附件已存在就跳過

    回傳 {issue_key: [上傳成功的附件名]}。
    """
    result: dict[str, list[str]] = {k: [] for k in issue_keys}

    for issue_key in issue_keys:
        existing_names: set[str] = set()
        if skip_existing:
            existing_names = {a["filename"] for a in list_attachments(issue_key)}

        for item in files:
            if isinstance(item, tuple):
                path, mime = item
            else:
                path = item
                mime = _guess_mime(path)

            # 決定附件名
            if rename_prefix_per_dir and path.parent.name:
                upload_name = f"{path.parent.name}_{path.name}"
            else:
                upload_name = path.name

            if upload_name in existing_names:
                print(f"  [SKIP] {issue_key} 已有附件 {upload_name!r}")
                continue

            # 用 attach_screenshot（Stage A1 已加 mime 參數）
            # 但 attach_screenshot 用的是 file_path.name，無法 rename
            # 所以改寫一段直接 multipart upload
            try:
                with open(path, "rb") as f:
                    resp = requests.post(
                        f"{JIRA_URL}/rest/api/2/issue/{issue_key}/attachments",
                        headers={"X-Atlassian-Token": "no-check"},
                        files={"file": (upload_name, f, mime)},
                        auth=_auth(),
                        timeout=60,
                    )
                resp.raise_for_status()
                result[issue_key].append(upload_name)
                print(f"  [OK] {issue_key} ← {upload_name} ({path.stat().st_size} bytes)")
            except Exception as e:
                print(f"  [FAIL] {issue_key} ← {upload_name}: {e}")

    return result


# ════════════════════════════════════════════════════════════════════════════
# 環境健檢（debug 用）
# ════════════════════════════════════════════════════════════════════════════

def check_token() -> dict[str, str]:
    """GET /myself 驗 token 有效。失敗回 {}，成功回 {accountId, displayName, emailAddress}。"""
    try:
        resp = requests.get(
            f"{JIRA_URL}/rest/api/3/myself",
            headers={"Accept": "application/json"},
            auth=_auth(),
            timeout=10,
        )
        resp.raise_for_status()
        d = resp.json()
        return {
            "accountId": d.get("accountId", ""),
            "displayName": d.get("displayName", ""),
            "emailAddress": d.get("emailAddress", ""),
        }
    except Exception:
        return {}


def list_visible_projects() -> list[dict[str, str]]:
    """token 可見的所有 project。"""
    resp = requests.get(
        f"{JIRA_URL}/rest/api/3/project/search",
        params={"maxResults": 50},
        headers={"Accept": "application/json"},
        auth=_auth(),
        timeout=10,
    )
    resp.raise_for_status()
    return [
        {"key": p["key"], "id": p["id"], "name": p["name"]}
        for p in resp.json().get("values", [])
    ]


def get_project_issuetypes(project_key: str | None = None) -> list[str]:
    """取得 project 可建立的 issuetypes。"""
    pk = project_key or JIRA_PROJECT_KEY
    resp = requests.get(
        f"{JIRA_URL}/rest/api/3/issue/createmeta",
        params={"projectKeys": pk},
        headers={"Accept": "application/json"},
        auth=_auth(),
        timeout=10,
    )
    resp.raise_for_status()
    projects = resp.json().get("projects", [])
    if not projects:
        return []
    return [t["name"] for t in projects[0].get("issuetypes", [])]
