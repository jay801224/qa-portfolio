"""
jira_ticket_perf_react.py — Performance Testing Epic（React 階段）場景 helper

職責邊界：
    - 本檔只放「React 階段效能立案的事實內容」（Epic / 5 張 BUG description）
    - 通用流程（create_epic_with_subtasks / attach_evidence / 驗回 / 查重）
      全部呼叫 shared/jira/jira_batch.py（SDK 層）
    - 未來 egret 階段會有姊妹檔 jira_ticket_perf_egret.py，共用同一個 jira_batch SDK

使用：
    python jira_ticket_perf_react.py --check         # read-only 健檢
    python jira_ticket_perf_react.py --create-epic   # 開 Epic
    python jira_ticket_perf_react.py --create-bugs   # 開 5 張子票（需 Epic 已存在）
    python jira_ticket_perf_react.py --attach        # 上傳 6 JSON + observation.md
    python jira_ticket_perf_react.py --patch-epic-env # 補 Epic 測試環境段 + 子票連結
    python jira_ticket_perf_react.py --rename-bugs   # 5 張 BUG summary 加 React|PC -
    python jira_ticket_perf_react.py --verify-all    # GET 驗回 Epic + 5 BUG
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Windows console cp950 編不了 ≤ ≥ — 等，強制 utf-8
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "shared" / "jira"))

# 兩段 load：root 提供 PROJECT_KEY，react/.env 覆蓋（已更新的）token
load_dotenv(ROOT / ".env", override=True)
load_dotenv(ROOT / "react" / ".env", override=True)

from jira_batch import (  # noqa: E402
    create_epic_with_subtasks,
    attach_evidence,
    update_issue_description,
    rename_issue_summary,
    get_issue_fields,
    list_attachments,
    check_token,
    list_visible_projects,
    get_project_issuetypes,
)


# ── 場景常數（事實內容，不該下放到 jira_batch）────────────────────────────────

STATE_DIR = ROOT / ".claude" / "_state" / "perf_react"
EVIDENCE_DIR = ROOT / "react" / "report" / "performance" / "browser" / "performance_baseline_20260507_115737"
OBSERVATION_FILE = ROOT / "react" / "report" / "performance" / "browser" / "perf_baseline_20260507_110830" / "observation.md"

EPIC_SUMMARY = "(自動化測試) Performance Testing"

EPIC_DESCRIPTION_WIKI = """h2. 名詞速查（給非技術讀者）

|| 英文縮寫 || 中文意思 || 通俗解釋 || Web Vitals 標準 ||
| *FCP* | First Contentful Paint（首次內容繪製） | 使用者第一次看到「畫面有東西」的時間 | ≤ 1.8 秒 良好 |
| *LCP* | Largest Contentful Paint（最大內容繪製） | 使用者覺得「主要內容已載完」的時間 | ≤ 2.5 秒 良好 |
| *CLS* | Cumulative Layout Shift（累積版面位移） | 載入過程中「畫面跳動」的累積分數，越低越穩 | ≤ 0.1 良好 |
| *TBT* | Total Blocking Time（總阻塞時間） | 主執行緒被卡住、無法回應點擊的累積時間 | ≤ 200ms 良好 |
| *Long Task* | 長任務 | 一個單獨的 JS 工作做超過 50ms，會卡住點擊回饋 | < 50ms 不算 long |
| *DOM Nodes* | DOM 節點數 | 網頁元件總數，越多越耗記憶體 | < 1500 通常無虞 |
| *Module Federation* | 模組聯邦 | 把一個大網站拆成多個小模組，按需載入；本案 5 個遠端模組 404 = 對應功能直接掛掉 | — |
| *Cold-start* | 冷啟動 | 第一次進網站、沒任何快取的最差情境 | — |
| *mf-manifest* | Module Federation 模組清單檔 | 告訴主站「這個遠端模組有哪些 chunk」的 JSON 檔，404 = 主站找不到該模組 | — |

h2. Epic 範圍

本 Epic（*Performance Testing*）為效能測試長期容器，*跨平台 / 跨技術棧* 收錄所有效能相關問題：

* *第一批（本次 React 階段）*：UAT <ACCOUNT>（v1.2.22）大廳 5 個效能 / 部署問題（B1–B5），證據來源為 2026-05-07 11:44 與 11:57 兩次連續基線量測
* *第二批（後續 egret 階段）*：跑完 egret 平台基線後續加入

所有指標數值皆有完整 JSON 證據可追溯，路徑見每張子票附件。

h2. 量測方法

* 工具：Playwright + PerformanceObserver（headless Chromium 1366×900）
* 三場景：lobby cold-start / baccarat_room N006 / sicbo_room N026
* 每場景獨立 browser context（避免污染）
* 兩 trials 取一致性，stableWaitMs = 8000ms 等 LCP/CLS 穩定
* Collector 腳本：{{react/performance/browser/performance_baseline_collector.py}}

h2. 子票"""


SUBTASK_TITLES = {
    "B1": "5 個 Module Federation Remote 全 404",
    "B2": "大廳 LCP 4.4–5.6 秒",
    "B3": "大廳 TBT 464–728ms + 單一 long task ≥289ms",
    "B4": "大廳 CLS 0.005–0.138 不穩定",
    "B5": "@<PRODUCT>/ui / @<PRODUCT>/core workspace:* 版本協商失敗",
}


def _bug_summary(tag: str, title_body: str) -> str:
    return f"(自動化測試) React|PC - UAT 大廳 {title_body}"


SUBTASKS = [
    {
        "tag": "B1",
        "summary": "(自動化測試) React|PC - UAT 大廳 5 個 Module Federation Remote 全 404，影響 <PRODUCT>/DTW/RWT/DI6/DI6S 遊戲分類",
        "priority": "High",
        "description": """h2. Testing version
<PRODUCT> UAT <ACCOUNT> v1.2.22

h2. Affected platform
PC（headless Chromium 1366×900）

h2. Steps
# 開啟 UAT 大廳：{{https://example.internal/pa/pc/}}
# 開 DevTools Network 過濾 {{mf-manifest}}
# 觀察 5 個 Module Federation Remote 的 manifest 全 404
# Console 出現 5 段 {{[initMF] Remote "X" preload failed}} error

h2. Actual result
五個 Module Federation Remote 的 manifest.json 全 404，伺服器回 HTML 頁，前端 parse 成 JSON 失敗：

* {{modules/<PRODUCT>/v1.0.28/mf-manifest.json}} — 404
* {{modules/DTW/v1.2.21/mf-manifest.json}} — 404
* {{modules/RWT/v1.0.11/mf-manifest.json}} — 404
* {{modules/DI6/v1.2.21/mf-manifest.json}} — 404
* {{modules/DI6S/v1.2.21/mf-manifest.json}} — 404

每個 manifest 在 cold-start + 切兩個 tab 共出現 3 次重試，console errorCount 11 / warningCount 50 主要源自此。

h2. Expected result
五個 Remote manifest 全部 200 OK，或從部署清單移除（如該版本不需要）。

h2. Comment
* Test ID: <PRODUCT>-PERF-B1
* Module: Module Federation
* Can_Auto: Yes（{{performance_baseline_collector.py}}）
* Execution Time: 2026-05-07 11:57
* 本次測試網路環境：TW 辦公室有線網路
* Screenshot path: 附件 11:57 trial_1+2 各場景 JSON 的 {{network.badResponses}} 段
* 三次跑（11:08 / 11:44 / 11:57）皆完全重現 — 證據量分別 29 / 120 / 122 hits
""",
    },
    {
        "tag": "B2",
        "summary": "(自動化測試) React|PC - UAT 大廳 LCP（最大內容繪製）4424–5568ms，超過 Web Vitals \"good\" 標準（≤2500ms）",
        "priority": "High",
        "description": """h2. Testing version
<PRODUCT> UAT <ACCOUNT> v1.2.22

h2. Affected platform
PC（headless Chromium 1366×900）

h2. Steps
# Cold-start 進大廳（無 cache）
# 等 LOBBY_MENU 出現 + stableWaitMs 8000ms 讓 LCP 穩定
# 用 PerformanceObserver 量 LCP

h2. Actual result
*LCP 4424–5568ms，遠超 Web Vitals "good" 標準（≤2500ms）：*

|| Trial || Lobby cold-start LCP || 進房場景 lobby 段 LCP ||
| 11:57 trial_1 | 4424 ms | bac=5432 / sicbo=5536 |
| 11:57 trial_2 | 4892 ms | bac=5568 / sicbo=5484 |

LCP candidate 演進：
* {{<div>}} 870px²（FCP 同期 ~400ms）
* 背景 {{background_pattern.7764eb04.svg}} 404857px²（loadTime ~5000ms）
* *主視覺輪播 {{<img blob:>}} 489570px²*（loadTime ~5300ms，*決定性貢獻*）

h2. Expected result
LCP < 2500ms（Web Vitals good）；至少 < 4000ms（OK 邊界）。

h2. 修法方向
* 主視覺輪播 banner 預載入或拆 critical CSS
* 背景 SVG 改 inline 或縮圖
* 為主視覺與背景預留版面尺寸（aspect-ratio）

h2. Comment
* Test ID: <PRODUCT>-PERF-B2
* Module: LB / Performance
* Can_Auto: Yes
* Execution Time: 2026-05-07 11:57
* 本次測試網路環境：TW 辦公室有線網路
* Screenshot path: 附件 11:57 trial_1+2 lobby/baccarat/sicbo JSON 的 {{snapshot.lcpEntries}} 段
""",
    },
    {
        "tag": "B3",
        "summary": "(自動化測試) React|PC - UAT 大廳 TBT（總阻塞時間）464–728ms，單一 long task 最高 506ms，超過 Web Vitals 標準",
        "priority": "High",
        "description": """h2. Testing version
<PRODUCT> UAT <ACCOUNT> v1.2.22

h2. Affected platform
PC

h2. Steps
# Cold-start 進大廳
# 量 PerformanceObserver longtask + 加總 totalBlockingMs

h2. Actual result
*TBT 464–728ms，最高單一 long task 506ms：*

|| 場景 || trial 1 TBT / max long task || trial 2 TBT / max long task ||
| lobby (11:57) | 591ms / 296ms | 464ms / 289ms |
| baccarat_room lobby 段 | 586ms / 280ms | 683ms / 379ms |
| sicbo_room lobby 段 | *728ms / 506ms* | 731ms / 526ms |

代表使用者點擊大廳元件後，主執行緒最壞會 *卡 506ms 不回應*。

h2. Expected result
TBT < 200ms（good）；至少 < 600ms（OK）。

h2. 修法方向
* Profile 第 ~3 秒區段的 long task 來源（Module Federation remote 解析？React mount？）
* 拆 chunk 到 idle-time
* 重的計算搬到 Web Worker

h2. Comment
* Test ID: <PRODUCT>-PERF-B3
* Module: LB / Performance
* Can_Auto: Yes
* Execution Time: 2026-05-07 11:57
* 本次測試網路環境：TW 辦公室有線網路
* Screenshot path: 附件 11:57 trial_1+2 各場景 JSON 的 {{snapshot.longTasks}} 段（含 entries 陣列）
""",
    },
    {
        "tag": "B4",
        "summary": "(自動化測試) React|PC - UAT 大廳 CLS（累積版面配置偏移）trial 間 0.005–0.138 浮動，主視覺與背景 SVG 載入完成時觸發 5 個連續 shift",
        "priority": "Medium",
        "description": """h2. Testing version
<PRODUCT> UAT <ACCOUNT> v1.2.22

h2. Affected platform
PC

h2. Steps
# Cold-start 進大廳
# 量 PerformanceObserver layout-shift（排除 hadRecentInput）

h2. Actual result
*CLS 跨 trial 浮動 24 倍（0.0057–0.1379）*：

|| 場景 || trial 1 CLS || trial 2 CLS ||
| lobby (11:57) | 0.0057 | 0.1157 |
| baccarat_room lobby 段 | 0.1363 | 0.1257 |
| sicbo_room lobby 段 | 0.1179 | 0.1382 |

5 個連續 shift 集中在 lobby 載入 *第 5–6 秒*（主視覺 blob:img 與背景 pattern SVG 載入完成時）：

* +0.0798（佔 65%）— 主要 shift
* +0.0256
* +0.0109
* +0.0044
* +0.0012

切 tab 後另有 2 個微小 shift（<0.003），不是大問題。

h2. Expected result
* CLS < 0.1（Web Vitals good）
* 跨 trial 應穩定，不該浮動 24 倍

h2. 修法方向（建議）
* 主視覺 {{<img>}} 加 {{width}} / {{height}} attr 或 CSS 預留 aspect-ratio
* 背景 SVG container 預設 fixed dimensions

h2. Comment
* Test ID: <PRODUCT>-PERF-B4
* Module: LB / UI Stability
* Can_Auto: Yes
* Execution Time: 2026-05-07 11:57
* 本次測試網路環境：TW 辦公室有線網路
* Screenshot path: 附件 11:57 trial_1+2 各場景 JSON 的 {{snapshot.clsEntries}} 段
""",
    },
    {
        "tag": "B5",
        "summary": "(自動化測試) React|PC - UAT 大廳 @<PRODUCT>/ui / @<PRODUCT>/core 共享套件 workspace:* 版本協商失敗，console warning 重複 16+ 次",
        "priority": "Low",
        "description": """h2. Testing version
<PRODUCT> UAT <ACCOUNT> v1.2.22

h2. Affected platform
PC

h2. Steps
# Cold-start 進大廳
# 觀察 console warnings 與 Module Federation runtime 訊息

h2. Actual result
console 重複 16+ 次出現 Module Federation 共享套件版本協商失敗 warning：
{noformat}
Shared module "@<PRODUCT>/ui" with required version "workspace:*" not satisfied
Shared module "@<PRODUCT>/core" with required version "workspace:*" not satisfied
{noformat}

* 三次跑都重現：11:08 (31 hits) / 11:44 (174 hits) / 11:57 (174 hits)
* 不影響功能載入，但污染 console + 暗示 Module Federation 共享套件設定錯誤
* {{workspace:*}} 是 monorepo *開發期* 的 protocol（pnpm/yarn），*不該進 production build*；publish 時應替換成實際語意化版本

h2. Expected result
共享套件版本標記應為實際 semver（如 {{^1.0.0}}），不留 {{workspace:*}}。

h2. Related issues（非重複，僅供參考）
* TC_2758 — [aceron-ui] TailwindCSS Migration（aceron 框架本身的 Story）
* TC_134 — L2512 - Game Frontend Framework - Aceron（aceron 框架歷史 Task）

h2. Comment
* Test ID: <PRODUCT>-PERF-B5
* Module: Module Federation / Build
* Can_Auto: Yes
* Execution Time: 2026-05-07 11:57
* 本次測試網路環境：TW 辦公室有線網路
* Screenshot path: 附件 11:57 trial_1+2 各場景 JSON 的 {{console.errors}} 段（warning 級訊息）
""",
    },
]


# ── 場景特殊邏輯：動態組 Epic description（含子票連結 + 測試環境段）──────────

EPIC_TEST_ENV_BLOCK = """

h2. 測試環境

* 網路環境：*TW 辦公室有線網路*
* 量測時間：2026-05-07 11:44 / 11:57（兩次連續基線）
* 平台：PC（headless Chromium 1366×900）
"""


def _build_final_epic_description(sub_keys: dict[str, str]) -> str:
    """把子票連結段動態替換為帶實際 issue key 的版本，並加上測試環境段。"""
    lines = ["", ""]  # h2. 子票 段下空兩行（接在 EPIC_DESCRIPTION_WIKI 結尾）
    for tag in ["B1", "B2", "B3", "B4", "B5"]:
        key = sub_keys.get(tag, "(尚未開立)")
        lines.append(f"* *{tag}* — {SUBTASK_TITLES[tag]} — [{key}]")
    return EPIC_DESCRIPTION_WIKI + "\n" + "\n".join(lines) + EPIC_TEST_ENV_BLOCK


# ── load state helpers ──────────────────────────────────────────────────────

def _load_keys() -> tuple[str, dict[str, str]]:
    """讀 state；回 (epic_key, sub_keys)。沒有就 ("", {})。"""
    epic_file = STATE_DIR / "epic_key"
    sub_file = STATE_DIR / "sub_keys.json"
    epic = epic_file.read_text(encoding="utf-8").strip() if epic_file.exists() else ""
    subs = json.loads(sub_file.read_text(encoding="utf-8")) if sub_file.exists() else {}
    return epic, subs


# ── commands ────────────────────────────────────────────────────────────────

def cmd_check() -> int:
    """環境健檢：token / project / 既有同名 Epic / 子票"""
    print(f"[info] STATE_DIR = {STATE_DIR}")
    me = check_token()
    if not me:
        print("[FAIL] token 無效")
        return 2
    print(f"[OK] token: {me['displayName']} <{me['emailAddress']}>")

    print()
    print("可見 project：")
    for p in list_visible_projects():
        print(f"  {p['key']:8s} {p['name']}")

    print()
    types = get_project_issuetypes()
    print(f"CUI 可建 issuetypes: {types}")
    if "Epic" not in types:
        print("[FAIL] CUI 沒有 Epic")
        return 2
    return 0


def cmd_create_epic() -> int:
    """開 Epic（用 jira_batch.create_epic_with_subtasks 但 subtasks=[]，只開 Epic）。"""
    assignee = os.getenv("JIRA_MY_ACCOUNT_ID", "") or os.getenv("JIRA_SELF_ACCOUNT_ID", "")
    keys = create_epic_with_subtasks(
        epic_summary=EPIC_SUMMARY,
        epic_description=EPIC_DESCRIPTION_WIKI,
        subtasks=[],  # 第一階段只開 Epic，子票留 cmd_create_bugs
        state_dir=STATE_DIR,
        assignee=assignee,
        epic_priority="Medium",
    )
    print(f"\n[OK] Epic key = {keys['epic']}")
    return 0


def cmd_create_bugs() -> int:
    """開 5 張子票（Epic 已開時，補開子票）。"""
    epic_key, _ = _load_keys()
    if not epic_key:
        print("[FAIL] STATE_DIR 沒 epic_key，請先 --create-epic")
        return 2

    assignee = os.getenv("JIRA_MY_ACCOUNT_ID", "") or os.getenv("JIRA_SELF_ACCOUNT_ID", "")

    # create_epic_with_subtasks 傳入 epic_summary 同名會 detect 既有 Epic 後 SKIP，
    # 然後往下開 subtasks（也會逐個查重 SKIP 既有）。實作上是 idempotent
    keys = create_epic_with_subtasks(
        epic_summary=EPIC_SUMMARY,
        epic_description=EPIC_DESCRIPTION_WIKI,
        subtasks=SUBTASKS,
        state_dir=STATE_DIR,
        assignee=assignee,
    )
    print()
    print("結果：")
    for tag in ["epic"] + [s["tag"] for s in SUBTASKS]:
        print(f"  {tag}: {keys.get(tag)}")
    return 0


def cmd_attach() -> int:
    """5 張 BUG 各上傳 6 個 JSON + observation.md"""
    epic_key, sub_keys = _load_keys()
    if not sub_keys:
        print("[FAIL] STATE_DIR 沒 sub_keys.json，請先 --create-bugs")
        return 2

    json_files = []
    for trial in ["trial_1", "trial_2"]:
        for scen in ["lobby.json", "baccarat_room.json", "sicbo_room.json"]:
            p = EVIDENCE_DIR / trial / scen
            if not p.exists():
                print(f"[FAIL] 缺檔: {p}")
                return 2
            json_files.append(p)

    if not OBSERVATION_FILE.exists():
        print(f"[FAIL] 缺 observation.md: {OBSERVATION_FILE}")
        return 2

    issue_keys = [sub_keys[tag] for tag in ["B1", "B2", "B3", "B4", "B5"]]
    files = json_files + [OBSERVATION_FILE]
    result = attach_evidence(
        issue_keys=issue_keys,
        files=files,
        rename_prefix_per_dir=True,  # trial_1_lobby.json / trial_2_lobby.json
        skip_existing=True,
    )
    print()
    for k, names in result.items():
        print(f"  {k}: 新增 {len(names)} 附件")
    return 0


def cmd_patch_epic_env() -> int:
    """更新 Epic description：含子票連結 + 測試環境段"""
    epic_key, sub_keys = _load_keys()
    if not epic_key:
        print("[FAIL] STATE_DIR 沒 epic_key")
        return 2
    new_desc = _build_final_epic_description(sub_keys)
    verify = ["TW 辦公室有線網路", "測試環境"] + [f"[{v}]" for v in sub_keys.values()]
    ok = update_issue_description(epic_key, new_desc, verify_contains=verify)
    if ok:
        print(f"[OK] Epic {epic_key} description 更新 + 驗回通過 ({len(new_desc)} chars)")
        return 0
    return 2


def cmd_rename_bugs() -> int:
    """5 張 BUG summary 從 (自動化測試) <主體> → (自動化測試) React|PC - <主體>。

    本場景 helper 已預設 SUBTASKS 的 summary 含 React|PC -，故跑 --create-bugs 時新建的
    票就是最終格式。本 cmd 的功能用於『歷史已開但沒含 React|PC -』的場景修補。
    """
    _, sub_keys = _load_keys()
    if not sub_keys:
        print("[FAIL] STATE_DIR 沒 sub_keys.json")
        return 2

    INSERT = "React|PC - "
    PREFIX = "(自動化測試) "

    for tag in ["B1", "B2", "B3", "B4", "B5"]:
        issue_key = sub_keys[tag]
        f = get_issue_fields(issue_key, ["summary"])
        cur = f["summary"]
        print(f"[{tag}] {issue_key}: {cur!r}")
        if INSERT in cur:
            print(f"  [SKIP] 已含 React|PC -")
            continue
        if not cur.startswith(PREFIX):
            print(f"  [FAIL] summary 不以 (自動化測試) 開頭，停手")
            return 2
        body = cur[len(PREFIX):]
        new = f"{PREFIX}{INSERT}{body}"
        ok = rename_issue_summary(issue_key, new)
        if not ok:
            return 2
        print(f"  [OK] → {new!r}")
    return 0


def cmd_verify_all() -> int:
    """重 GET Epic + 5 BUG 確認 summary / status / parent / 附件數。"""
    epic_key, sub_keys = _load_keys()
    if not epic_key:
        print("[FAIL] STATE_DIR 沒 epic_key")
        return 2

    print(f"Epic: {epic_key}")
    f = get_issue_fields(epic_key, ["summary", "status", "description"])
    print(f"  summary: {f['summary']}")
    print(f"  status:  {f['status']['name']}")
    desc = f.get("description") or ""
    print(f"  description: {len(desc)} chars / 含 TW 辦公室有線網路: {'TW 辦公室有線網路' in desc}")
    for tag, key in sub_keys.items():
        print(f"  含 [{key}] ({tag}): {f'[{key}]' in desc}")

    print()
    for tag in ["B1", "B2", "B3", "B4", "B5"]:
        if tag not in sub_keys:
            continue
        issue_key = sub_keys[tag]
        f = get_issue_fields(
            issue_key,
            ["summary", "priority", "status", "customfield_10014", "attachment"],
        )
        attach = f.get("attachment", [])
        print(f"\n[{tag}] {issue_key}")
        print(f"  summary: {f['summary']}")
        print(f"  priority: {f['priority']['name']}  status: {f['status']['name']}")
        print(f"  epic_link: {f.get('customfield_10014')}")
        print(f"  attachments: {len(attach)} 個")
        print(f"  含 'React|PC -': {'React|PC - ' in f['summary']}")
    return 0


def cmd_migrate_state() -> int:
    """把舊 _jira_perf_helper 的 state 從 .claude/_state/perf_epic_key 等遷到 perf_react/。"""
    old_state = ROOT / ".claude" / "_state"
    old_epic = old_state / "perf_epic_key"
    old_subs = old_state / "perf_bug_keys.json"

    if not old_epic.exists() and not old_subs.exists():
        print("[info] 無舊 state 可遷移")
        return 0

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    if old_epic.exists():
        epic_key = old_epic.read_text(encoding="utf-8").strip()
        (STATE_DIR / "epic_key").write_text(epic_key, encoding="utf-8")
        print(f"[OK] perf_epic_key → {STATE_DIR / 'epic_key'} ({epic_key})")
    if old_subs.exists():
        subs = old_subs.read_text(encoding="utf-8")
        (STATE_DIR / "sub_keys.json").write_text(subs, encoding="utf-8")
        print(f"[OK] perf_bug_keys.json → {STATE_DIR / 'sub_keys.json'}")
    print(f"[info] 舊檔保留在 {old_state}（你可手動刪除）")
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true", help="環境健檢")
    p.add_argument("--create-epic", action="store_true", help="開 Epic")
    p.add_argument("--create-bugs", action="store_true", help="開 5 張子票（Epic 已存在）")
    p.add_argument("--attach", action="store_true", help="上傳證據附件")
    p.add_argument("--patch-epic-env", action="store_true", help="更新 Epic description 加測試環境段+子票連結")
    p.add_argument("--rename-bugs", action="store_true", help="5 BUG summary 加 React|PC -")
    p.add_argument("--verify-all", action="store_true", help="GET 驗回 Epic + 5 BUG")
    p.add_argument("--migrate-state", action="store_true", help="從舊 _jira_perf_helper state 遷移到 perf_react/")
    args = p.parse_args()

    if args.check:           return cmd_check()
    if args.create_epic:     return cmd_create_epic()
    if args.create_bugs:     return cmd_create_bugs()
    if args.attach:          return cmd_attach()
    if args.patch_epic_env:  return cmd_patch_epic_env()
    if args.rename_bugs:     return cmd_rename_bugs()
    if args.verify_all:      return cmd_verify_all()
    if args.migrate_state:   return cmd_migrate_state()
    p.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())


# ════════════════════════════════════════════════════════════════════════════
# TODO（剩餘 backlog — 已對 Egret 階段重評估）
# ════════════════════════════════════════════════════════════════════════════
#
# 完整重評估見 reports/perf_d2_egret_findings_review.md（2026-05-08）。
# F6 / F8 / F9 / F10 已關閉（done 或 rejected）。剩 3 條：
#
# F5  [HIGH 缺漏]   jira_bot.py 內 attach_screenshot() 副檔名推 mime
#                  （目前都是 PNG 風險低，但若上傳 .jpg 等會錯標 mime）
# F7  [LOW 多餘]    SUBTASKS 5 張票 description 結構重複 ~40%
#                  → 抽 _build_bug_description() 範本函式
#                  （Egret 階段驗證「保留各自獨立」更穩，DEFER 到第三平台再評估）
# F13 [LOW 界定不清]  _load_keys / _build_final_epic_description 是否抽到 jira_batch
#                    → 等下次新平台（如 perf_runner 接 PartnerX）再評估

