# shared/jira — Jira 開票工具三層架構

> **版本**：v1（2026-05-07，建立 baseline）
> **目的**：給未來新人 / 場景 helper 設計師看 — 釐清 4 個 Python 檔的職責邊界，避免重複造輪。

---

## 三層架構（從上到下）

```
                ┌─────────────────────────────────────┐
                │  scenario helper（場景專屬層）       │
                │                                      │←── 只放「這次測試的事實內容」
                │  jira_ticket_perf_react.py          │    （Epic title / BUG description /
                │  ↓ import jira_batch                 │     測試環境註記等）
                └─────────────────────────────────────┘
                                ↓
                ┌─────────────────────────────────────┐
                │  jira_batch.py（通用批量 SDK）       │←── 跨技術棧 / 跨平台 批量
                │  ↓ import jira_bot, jira_create     │    Epic + N 子票流程
                └─────────────────────────────────────┘
                                ↓
                ┌─────────────────────────────────────┐
                │  jira_bot.py（CLI + 部分 SDK）      │←── xlsx 開票 + 公開 jql_search /
                │  ↓ import jira_create                │    create_issue_ext 給上層用
                └─────────────────────────────────────┘
                                ↓
                ┌─────────────────────────────────────┐
                │  jira_create.py（最低階）           │←── .env 設定 + _auth +
                │                                      │    attach_screenshot
                └─────────────────────────────────────┘
                                ↓
                            Jira Cloud REST API
```

---

## 4 檔職責對照表

| 檔案 | 路徑 | 角色 / 層級 | 做什麼 | 不做什麼 | 何時用它 |
|---|---|---|---|---|---|
| **jira_create.py** | `shared/jira/` | **最低階工具** | 1. 從 `.env` 讀 Jira 連線設定（URL / token / project_key 等常數）<br>2. `_auth()` 提供 HTTPBasicAuth 物件<br>3. `attach_screenshot(key, path, mime)` 上傳檔案<br>4. `build_description` / `find_fail_screenshot` / `resolve_priority` 等 xlsx 流程小工具<br>5. 自帶 CLI（從 xlsx FAIL 列開 Bug） | 不開 Epic / 不批量 / 不驗票 / 不互動選單 | 純粹當「.env loader + 共用設定常數的家」被別人 import；單獨跑只服務 xlsx → 1 Bug 場景 |
| **jira_bot.py** | `shared/jira/` | **中層 CLI + 部分 SDK** | 1. CLI：`--action create/verify/auto-verify/update`，從 xlsx 自動開票（Bug / Task / Epic / Story）<br>2. 互動選單：人工逐張開票 / 驗票<br>3. **公開 SDK 函式**（被 jira_batch import）：<br>   - `jql_search(jql, fields)` — v3 JQL 自動分頁<br>   - `create_issue_ext(...)` — 建任意 issuetype<br>4. 驗票 / 自動驗票（5 分鐘排程）<br>5. 補截圖 / 比對最新報告 | 不批量 Epic + N 子票（會散落在多個 xlsx 行）<br>不負責場景專屬內容 | 兩種用法：<br>(a) 給人快速開票 / 驗票（CLI / 互動）<br>(b) 給其他 helper import 它的 jql_search / create_issue_ext |
| **jira_batch.py** | `shared/jira/` | **通用批量 SDK** | 1. `create_epic_with_subtasks(epic, subtasks, state_dir, ...)` — 1 Epic + N 子票一氣呵成<br>2. `attach_evidence(keys, files)` — N 張票 × M 個檔，自動 mime 推導 + rename + skip 重複<br>3. `update_issue_description` / `rename_issue_summary` / `get_issue_fields` / `list_attachments`<br>4. `check_token` / `list_visible_projects` / `get_project_issuetypes`（環境健檢） | **完全不寫死任何場景知識**（不知道什麼是 LCP / TBT / Epic title）<br>不做 CLI 也不有互動選單 | 任何「開 1 個 Epic + 一堆子票」的場景：本次 React 效能立案、未來 Egret 效能立案、跨平台批量回報等 |
| **jira_ticket_perf_react.py** | `react/python/` | **場景 helper（React 階段）** | 1. **寫死 React 階段事實內容**：<br>   - `EPIC_DESCRIPTION_WIKI`（中文名詞表 + 量測方法）<br>   - `SUBTASKS`（5 張 BUG 完整 description，含 React\|PC + 測試環境註記）<br>   - `_build_final_epic_description`（場景專屬：子票連結段 + 測試環境段）<br>2. CLI：`--check / --create-epic / --create-bugs / --attach / --patch-epic-env / --rename-bugs / --verify-all / --migrate-state`<br>3. orchestration：呼叫 jira_batch 各函式的順序與時機 | 不放任何通用工具（那是 jira_batch 的職責）<br>不處理 Egret 階段內容（那是 jira_ticket_perf_egret.py 的職責）| 跑「(自動化測試) Performance Testing — React 階段」的批量立案唯一入口 |

---

## 三個關鍵原則（給未來新 helper 的設計師）

1. **場景內容寫在 scenario helper（最上層）** — 不能下放到 jira_batch（那是通用 SDK）
2. **批量流程（create / attach / update / 查重 / 驗回）寫在 jira_batch** — 不能寫進 helper（每個 helper 都要重寫一次）
3. **API 連線設定（.env / _auth / mime mapping）只能在 jira_create** — 別人都從這邊 import，避免 .env 解析散落

---

## 未來 Egret 階段範例

寫 `react/performance/browser/jira_ticket_perf_egret.py`（預估 ~300 行，跟 React 版差不多大），只填：

```python
from dotenv import load_dotenv
load_dotenv(ROOT / ".env", override=True)
load_dotenv(ROOT / "react" / ".env", override=True)

from jira_batch import create_epic_with_subtasks, attach_evidence, ...

EPIC_SUMMARY = "(自動化測試) Performance Testing"  # 同一個 Epic 容器
EPIC_DESCRIPTION_APPEND = "..."  # 追加到既有 Epic description 的 Egret 段
SUBTASKS = [
    {"tag": "B6", "summary": "(自動化測試) Egret|PC - ...", ...},
    ...
]
STATE_DIR = ROOT / ".claude" / "_state" / "perf_egret"
```

剩下流程邏輯全部 `import` 自 `jira_batch`。

> **注意**：若 Egret 要把票加到既有 Epic TC_2972 而非開新 Epic，需先做 backlog **F9**（jira_batch.create_epic_with_subtasks 加 update_existing_epic 參數）。屆時再評估。

---

## 已知問題與待辦

完整 backlog 寫在 `react/performance/browser/jira_ticket_perf_react.py` 末尾「TODO（egret 場景再評估）」段，9 個 finding 已在 [perf_d2_egret_findings_review.md](../../react/python/reports/perf_d2_egret_findings_review.md) 重新評估。

理由（使用者明示）：Egret 是完全不同的前端架構（登入流程、遊戲結構不同）；現在硬抽跨 React/Egret 抽象可能反而綁住設計，等真實 Egret 案例跑過後再決定哪些抽象真的成立。

---

## 演進歷程（git log 索引）

| Commit | 主題 |
|---|---|
| `903591a` | feat(perf): UAT 大廳效能基線 — TC_2972 Epic + 5 BUG + collector + helper |
| `adf935e` | refactor(jira): 修 attach_screenshot mime / _check_duplicate_today v2→v3 / CLI 補 Epic Story |
| `096c954` | refactor(jira): 抽 jira_batch 通用層；helper 改名 jira_performance_react.py 並重構走 jira_batch |
| `65f5149` | docs(jira): 補職責邊界 docstring + 修 jira_batch 子票查重誤判 + F5-F13 TODO backlog |
| `df44e64` | docs(jira): R-4 改 TODO backlog 不依賴 line 編號 |
| _本次_ | docs(jira): shared/jira/README.md v1 — 三層架構圖 + 4 檔職責對照表 |
