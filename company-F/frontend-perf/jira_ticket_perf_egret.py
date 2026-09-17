"""jira_ticket_perf_egret.py — Performance Testing Epic（Egret 階段）場景 helper

姊妹檔對齊 jira_ticket_perf_react.py 結構，但簡化（不需 cmd_create_epic / cmd_migrate_state）：
    - 不開新 Epic — 把 EB1-EB5 掛 React 階段已開的 TC_2972 Performance Testing Epic 下
    - 走 jira_batch.update_existing_epic（plan F9 backlog 實作完成）
    - 5 張 BUG 票對齊 React B1-B5 的 description 結構

使用：
    python jira_ticket_perf_egret.py --check          # read-only 健檢
    python jira_ticket_perf_egret.py --create-bugs    # 立 EB1-EB5 掛 TC_2972 Epic 下
    python jira_ticket_perf_egret.py --attach         # 上傳 17 檔 × 5 票（6 JSON + observation.md + 10 PNG）
    python jira_ticket_perf_egret.py --patch-epic-desc # 補 TC_2972 description Egret 段
    python jira_ticket_perf_egret.py --verify-all     # GET 驗回 5 BUG 含 Egret|PC - prefix
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Windows console cp950 編不了 ≤ ≥ ⏱ ⚠️ — 強制 utf-8
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "shared" / "jira"))

# 兩段 load：root .env + react/.env override
load_dotenv(ROOT / ".env", override=True)
load_dotenv(ROOT / "react" / ".env", override=True)

from jira_batch import (  # noqa: E402
    update_existing_epic,
    attach_evidence,
    update_issue_description,
    rename_issue_summary,
    get_issue_fields,
    list_attachments,
    check_token,
    list_visible_projects,
    get_project_issuetypes,
)


# ── 場景常數 ─────────────────────────────────────────────────────────────────

EPIC_KEY = "TC_2972"  # React 階段已開的 Performance Testing Epic
STATE_DIR = ROOT / ".claude" / "_state" / "perf_egret"
EVIDENCE_DIR = ROOT / "react" / "report" / "performance" / "browser" / "performance_baseline_egret_20260507_171832"

EGRET_SUBTASKS = [
    {
        "tag": "EB1",
        "summary": "(自動化測試) Egret|PC - UAT 大廳 CLS（累積版面配置偏移）跨場景固定 0.3559 (POOR)，跨 6 trials 差 < 0.0001 顯示為單次 deterministic shift（疑為 stage size 預留→1920x1080 final 調整）",
        "priority": "High",
        "description": """h2. Testing version
<PRODUCT> UAT Egret 5.4.1（example.internal/uatgame/ → example.internal:81/pc/pcv1/）

h2. Affected platform
PC（Playwright Chromium 1920×1080，non-headless）

h2. Steps
# 開啟 example.internal/uatgame/，<PRODUCT> 區塊填 USER=<ACCOUNT> / PID=<ACCOUNT> / GAMETYPE=<PRODUCT>大廳-0
# 點 Enter AGIN → 新分頁進大廳
# 等 stage.numChildren > 0 + getCurrentModule() === 'PCPlaza' 確認大廳 ready
# stableWaitMs 8000ms 等 LCP/CLS 穩定
# 用 PerformanceObserver layout-shift（buffered:true）量 CLS

h2. Actual result
*CLS 0.3559 跨 6 trials 差異 < 0.0001*（lobby trial1=0.3559 / lobby trial2=0.3559 / baccarat.lobby trial1=0.3559 / baccarat.lobby trial2=0.3558 / sicbo.lobby trial1=0.3559 / sicbo.lobby trial2=0.3559）

性質為 *單次 deterministic 大 shift*，非隨機累積（跟 React 階段 TC_2976 的 0.005-0.138 trial 跨度大不同）。

最可能原因：*Egret canvas size 從初始預留尺寸 → 1920x1080 final size 的單次調整*。observation.md §3.2 詳述。

h2. Expected result
* CLS ≤ 0.1（Web Vitals good）
* 至少 ≤ 0.25（OK 邊界）

h2. 修法方向（需開發釐清）
* 是否可在 Egret 初始化時預先設定正確 stage 尺寸避免 resize？
* 是否是 Egret runtime 引擎本身行為（非 <PRODUCT> 大廳 module 問題）？
* canvas 容器 CSS 預留 aspect-ratio 是否可消除 layout shift？

h2. Comment
* Test ID: <PRODUCT>-PERF-EB1
* Module: Egret runtime / PCPlaza
* Can_Auto: Yes（{{performance_baseline_collector_egret.py}}）
* Execution Time: 2026-05-07 17:18
* 本次測試網路環境：TW 辦公室有線網路
* Screenshot path: 附件 trial_1+2 各場景 JSON 的 {{snapshot.clsEntries}} 段 + lobby.png/baccarat_room_a_lobby.png/sicbo_room_a_lobby.png
* 跨 6 trials × 3 場景 100% 重現
""",
    },
    {
        "tag": "EB2",
        "summary": "(自動化測試) Egret|PC - UAT 大廳 TBT（總阻塞時間）2309-5396ms (POOR)，超 Web Vitals 標準（≤600ms OK）4-9 倍",
        "priority": "High",
        "description": """h2. Testing version
<PRODUCT> UAT Egret 5.4.1

h2. Affected platform
PC

h2. Steps
# Cold-start 進大廳（流程同 EB1）
# PerformanceObserver longtask（buffered:true）累積
# stableWaitMs 8000ms 後計算 TBT = sum(max(0, duration - 50))

h2. Actual result
*TBT 2309-5396ms（POOR）跨 6 trials*：

|| 場景 || trial 1 TBT || trial 2 TBT ||
| lobby (cold-start) | 4782ms | 2309ms |
| baccarat_room.lobby 段 | 3425ms | 3044ms |
| sicbo_room.lobby 段 | 2658ms | 2625ms |

跨 trials 平均 ~3500ms，比 React 階段（TC_2975 TBT 464-728ms）嚴重 4-10 倍。

代表使用者點擊大廳元件後，主執行緒會 *卡 2-5 秒不回應*。

h2. Expected result
* TBT ≤ 200ms（Web Vitals good）
* 至少 ≤ 600ms（OK 邊界）

h2. 修法方向（需開發 profile）
* 哪個環節貢獻長 task？候選：Egret runtime startup / Cube-Loader 模組初始化 / 圖片解壓 / WebSocket handshake
* 拆 chunk 到 idle-time、重的計算搬 Web Worker
* 是否能 lazy-load 部分 Egret module 而非啟動時全載

h2. Comment
* Test ID: <PRODUCT>-PERF-EB2
* Module: Egret runtime startup
* Can_Auto: Yes
* Execution Time: 2026-05-07 17:18
* 本次測試網路環境：TW 辦公室有線網路
* Screenshot path: 附件 trial_1+2 各場景 JSON 的 {{snapshot.longTasks.entries}} 段（含每筆 long task 的 startTime + duration）
""",
    },
    {
        "tag": "EB3",
        "summary": "(自動化測試) Egret|PC - UAT 大廳 Cube-Loader.min.js 兩條 TypeError 100% 必現（bind / _platformtype undefined），跨 6 trials × 3 場景重現",
        "priority": "Medium",
        "description": """h2. Testing version
<PRODUCT> UAT Egret 5.4.1（Cube-Loader.min.js?v=28）

h2. Affected platform
PC

h2. Steps
# 跑任一 Egret 場景 cold-start
# 觀察 console errors

h2. Actual result
兩條 TypeError 每場景每 trial *100% 重現*（共 6 trials × 3 場景）：

{noformat}
TypeError: Cannot read properties of undefined (reading 'bind')
    at eval (eval at <anonymous> (Cube-Loader.min.js?v=28:22:15493), <anonymous>:1:955077)

TypeError: Cannot read properties of undefined (reading '_platformtype')
    at t.onStoreChange (Cube-Loader.min.js, <anonymous>:1:446545)
    at t.onAddToStage (Cube-Loader.min.js, <anonymous>:1:6217)
    at r.$notifyListener (Cube-Loader.min.js, <anonymous>:1:2646)
    [...stack 8 層...]
{noformat}

不影響功能（三場景全進房成功，namedNodes / GameBac / GameShb module 都正常載入），但污染 console + 暗示 Cube-Loader 模組初始化某環節有問題。

h2. Expected result
* 0 console TypeError
* 或至少不 100% 必現（若是某些 race condition 應該 sporadic）

h2. 待開發釐清
* 是 Cube 框架 known issue（已修補但 <PRODUCT> 大廳沒升級）？
* 還是 <PRODUCT> 大廳 module 載入順序錯（Cube-Loader 期待某個 dependency 先載入但實際後）？
* 是否影響任何隱藏功能（日誌上報 / 分析 / 等）？

h2. Comment
* Test ID: <PRODUCT>-PERF-EB3
* Module: Cube-Loader / Egret runtime
* Can_Auto: Yes
* Execution Time: 2026-05-07 17:18
* 本次測試網路環境：TW 辦公室有線網路
* Screenshot path: 附件 trial_1+2 各場景 JSON 的 {{console.errors}} 段
""",
    },
    {
        "tag": "EB4",
        "summary": "(自動化測試) Egret|PC - UAT 大廳 GameShb 載入比 GameBac 多 +782 KB（路單 PNG 320KB + 桌面 JPG 107KB），增量資源 +34 個",
        "priority": "Low",
        "description": """h2. Testing version
<PRODUCT> UAT Egret 5.4.1

h2. Affected platform
PC

h2. Steps
# Cold-start 進大廳（snapshot_a）
# enterGameByVid('D051') 進百家樂 → snapshot_b → delta_baccarat
# 同 fresh ctx 跑 enterGameByVid('D010') 進骰寶 → snapshot_b → delta_sicbo
# 比對 delta resourceTransferBytesDelta

h2. Actual result
百家樂 vs 骰寶 module 載入差異跨 trials 一致：

|| Module || Δ resource count || Δ transferSize ||
| GameBac (D051) | +34 個 | +1009-1115 KB（trial 1+2 平均 1062 KB） |
| GameShb (D010) | +34 個 | +1897 KB（兩 trials 一致） |

差值 ~782-888 KB 主要來自 GameShb 獨家資源：
* {{GameShb/assets/v2/road_result.8c745f6c.png}} *320 KB*（路單視覺資產）
* {{GameShb/assets/background_pt_mid.d947064d.jpg}} *107 KB*（桌面背景）
* {{GameShb/assets/v2/bet_table.b947521f.json}} 1.5 KB
* {{GameShb/assets/v2/road_result.13c953eb.json}} 2.3 KB
* {{GameShb/assets/v2/shb_number_font.dd091fcb.fnt}} 1.9 KB
* {{GameShb/localize/GameShb_hans.2d7eae0f.json}} 0.9 KB

h2. Expected result
* 評估骰寶 PNG 路單 320KB 是否可壓縮（WebP / 漸進式 JPEG / 縮圖）
* 桌面 JPG 107KB 是否可 lazy-load（用戶實際進入後才載）

h2. 待 reviewer 評估
* 此差異是合理的「不同 module 內容差異」？
* 還是該優化（同樣是百家樂 / 骰寶 module 應該大小相近）？

h2. Comment
* Test ID: <PRODUCT>-PERF-EB4
* Module: GameShb assets
* Can_Auto: Yes
* Execution Time: 2026-05-07 17:18
* 本次測試網路環境：TW 辦公室有線網路
* Screenshot path: 附件 trial_1+2 baccarat_room.json + sicbo_room.json 的 {{delta_room_vs_lobby}} 段
""",
    },
    {
        "tag": "EB5",
        "summary": "(自動化測試) Egret|PC - UAT 大廳 <ACCOUNT>.config.js / survey API 404，環境配置缺漏（<ACCOUNT> / <ACCOUNT> 雙帳號重現）",
        "priority": "Low",
        "description": """h2. Testing version
<PRODUCT> UAT Egret 5.4.1

h2. Affected platform
PC

h2. Steps
# Cold-start 進大廳
# 觀察 Network panel 4xx-5xx responses

h2. Actual result
跨 6 trials × 3 場景 100% 重現：

* {{http://example.internal:81/pc/pcv1/resource/config/hosts/userhosts/<ACCOUNT>.config.js}} → *404*
* {{https://example.internal/api/v1/survey/player/pid/<ACCOUNT>/account/<ACCOUNT>}} → *404*

<ACCOUNT> 帳號跑 baseline 時也有同樣 404（<ACCOUNT>.config.js / .../<ACCOUNT>）— 表示是 *UAT 環境配置缺漏*，不限特定帳號。

不影響功能（Egret 大廳仍正常載入 + 進房成功），但污染 network panel + 影響使用者個人化（若 config.js 提供 per-user 設定的話）。

h2. Expected result
* <ACCOUNT>.config.js 應該存在（或設計上不該 fetch）
* survey API 應該 200（或 UAT 不啟用就移除前端呼叫）

h2. 可能歸屬
* 環境配置 / ops 問題（infra team 補 UAT 配置檔）
* 或前端應該 graceful handle 404（不該每場景持續 fetch）

h2. Comment
* Test ID: <PRODUCT>-PERF-EB5
* Module: Environment / config
* Can_Auto: Yes
* Execution Time: 2026-05-07 17:18
* 本次測試網路環境：TW 辦公室有線網路
* Screenshot path: 附件 trial_1+2 各場景 JSON 的 {{network.badResponses}} 段
""",
    },
]

EPIC_DESCRIPTION_APPEND = """
h2. Egret 階段（第二批，2026-05-07 17:18 量測）

對齊 React 階段 5 BUG 範式，跨平台 React vs Egret 對比：

|| 指標 || React (TC_2972 第一批) || Egret (本批 EB1-EB5) || Δ ||
| LCP | 4424-5568 ms POOR | 1408-1900 ms GOOD | -2.6× Egret 快 |
| CLS | 0.005-0.138 OK | 0.3559 跨場景固定 POOR | +3-30× Egret 嚴重 (EB1) |
| TBT | 464-728 ms OK 邊界 | 2309-5396 ms POOR | +4-10× Egret 嚴重 (EB2) |
| Cube-Loader errors | N/A (React 無此 lib) | 100% 重現 (EB3) | — |
| 模組大小差異 | N/A | GameShb +782 KB vs GameBac (EB4) | — |
| 環境 4xx | N/A | <ACCOUNT>/survey 404 (EB5) | — |

* *EB1* — UAT 大廳 CLS 0.3559 (POOR) — High
* *EB2* — UAT 大廳 TBT 2309-5396 ms (POOR) — High
* *EB3* — Cube-Loader.min.js 兩條 TypeError — Medium
* *EB4* — GameShb 比 GameBac 多 +782 KB — Low
* *EB5* — <ACCOUNT>.config.js / survey API 404 — Low

Collector：{{react/performance/browser/performance_baseline_collector_egret.py}}（commit e0c8856）
進房技術：{{PCPlaza.RootPageStore._instance.enterGameByVid(vid)}}（單行 store API call，零座標）
跨平台對比報告：{{react/report/performance/browser/perf_comparison_react_vs_egret_20260507_180000.md}}
"""


# ── load state ──────────────────────────────────────────────────────────────

def _load_keys() -> dict[str, str]:
    """讀 sub_keys.json；回 {tag: key, ...}。沒有就回 {}。"""
    sub_file = STATE_DIR / "sub_keys.json"
    return json.loads(sub_file.read_text(encoding="utf-8")) if sub_file.exists() else {}


# ── commands ────────────────────────────────────────────────────────────────

def cmd_check() -> int:
    """環境健檢：token / project / 既有 Epic TC_2972"""
    print(f"[info] STATE_DIR = {STATE_DIR}")
    print(f"[info] EPIC_KEY = {EPIC_KEY}")
    print(f"[info] EVIDENCE_DIR = {EVIDENCE_DIR}")
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
    if "Bug" not in types:
        print("[FAIL] CUI 沒有 Bug type")
        return 2

    # 驗 EPIC 存在
    f = get_issue_fields(EPIC_KEY, ["summary", "issuetype", "status"])
    print(f"\n既有 Epic {EPIC_KEY}: {f['summary']} [{f['status']['name']}]")
    if f["issuetype"]["name"] != "Epic":
        print(f"[FAIL] {EPIC_KEY} 不是 Epic")
        return 2
    return 0


def cmd_create_bugs() -> int:
    """立 EB1-EB5 掛 TC_2972 既有 Epic 下"""
    assignee = os.getenv("JIRA_MY_ACCOUNT_ID", "") or os.getenv("JIRA_SELF_ACCOUNT_ID", "")
    keys = update_existing_epic(
        epic_key=EPIC_KEY,
        subtasks=EGRET_SUBTASKS,
        state_dir=STATE_DIR,
        assignee=assignee,
    )
    print()
    print("結果：")
    for tag in ["epic"] + [s["tag"] for s in EGRET_SUBTASKS]:
        print(f"  {tag}: {keys.get(tag)}")
    return 0


def cmd_attach() -> int:
    """5 張 EB 各上傳 17 檔（6 trial JSON + observation.md + 10 PNG）"""
    sub_keys = _load_keys()
    if not sub_keys:
        print("[FAIL] STATE_DIR 沒 sub_keys.json，請先 --create-bugs")
        return 2

    # 6 trial JSON
    json_files: list[Path] = []
    png_files: list[Path] = []
    for trial in ["trial_1", "trial_2"]:
        for scen in ["lobby", "baccarat_room", "sicbo_room"]:
            p = EVIDENCE_DIR / trial / f"{scen}.json"
            if not p.exists():
                print(f"[FAIL] 缺 JSON: {p}")
                return 2
            json_files.append(p)
        # 10 PNG（每 trial 5 張）
        for png in ["lobby.png", "baccarat_room_a_lobby.png", "baccarat_room_b_room.png",
                    "sicbo_room_a_lobby.png", "sicbo_room_b_room.png"]:
            p = EVIDENCE_DIR / trial / png
            if not p.exists():
                print(f"[FAIL] 缺 PNG: {p}")
                return 2
            png_files.append(p)

    # observation.md
    obs = EVIDENCE_DIR / "observation.md"
    if not obs.exists():
        print(f"[FAIL] 缺 observation.md: {obs}")
        return 2

    issue_keys = [sub_keys[tag] for tag in ["EB1", "EB2", "EB3", "EB4", "EB5"]]
    files = json_files + png_files + [obs]
    print(f"[info] 將上傳 {len(files)} 檔 × {len(issue_keys)} 票")

    result = attach_evidence(
        issue_keys=issue_keys,
        files=files,
        rename_prefix_per_dir=True,  # trial_1_lobby.json / trial_2_lobby.json 等
        skip_existing=True,
    )
    print()
    for k, names in result.items():
        print(f"  {k}: 新增 {len(names)} 附件")
    return 0


def cmd_patch_epic_desc() -> int:
    """補 TC_2972 description Egret 段（append 模式不覆寫）"""
    sub_keys = _load_keys()
    if not sub_keys:
        print("[FAIL] STATE_DIR 沒 sub_keys.json，請先 --create-bugs")
        return 2

    # 把 sub_keys 的實際 issue key 動態填入 description（替換 EB1-EB5 placeholder）
    desc = EPIC_DESCRIPTION_APPEND
    for tag in ["EB1", "EB2", "EB3", "EB4", "EB5"]:
        key = sub_keys.get(tag, "(尚未開立)")
        desc = desc.replace(f"*{tag}* —", f"*{tag}* ([{key}]) —")

    existing = get_issue_fields(EPIC_KEY, ["description"]).get("description") or ""
    if "Egret 階段" in existing:
        print(f"[SKIP] {EPIC_KEY} description 已含 'Egret 階段' 段，跳過 append")
        return 0

    new_desc = existing + "\n\n" + desc
    ok = update_issue_description(EPIC_KEY, new_desc, verify_contains=[
        "Egret 階段", "EB1", "EB2", "EB3", "EB4", "EB5",
    ])
    if ok:
        print(f"[OK] Epic {EPIC_KEY} description Egret 段 append 通過 ({len(new_desc)} chars)")
        return 0
    return 2


def cmd_verify_all() -> int:
    """重 GET 5 BUG 確認 summary / status / parent / 附件數"""
    sub_keys = _load_keys()
    if not sub_keys:
        print("[FAIL] STATE_DIR 沒 sub_keys.json")
        return 2

    print(f"Epic: {EPIC_KEY}")
    f = get_issue_fields(EPIC_KEY, ["summary", "status", "description"])
    print(f"  summary: {f['summary']}")
    print(f"  status:  {f['status']['name']}")
    desc = f.get("description") or ""
    print(f"  description: {len(desc)} chars / 含 Egret 階段: {'Egret 階段' in desc}")

    print()
    for tag in ["EB1", "EB2", "EB3", "EB4", "EB5"]:
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
        print(f"  epic_link: {f.get('customfield_10014')} (預期 {EPIC_KEY})")
        print(f"  attachments: {len(attach)} 個 (預期 17)")
        print(f"  含 'Egret|PC -': {'Egret|PC - ' in f['summary']}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true", help="環境健檢 + 驗 EPIC_KEY 存在")
    p.add_argument("--create-bugs", action="store_true", help="立 EB1-EB5 掛 TC_2972 Epic 下")
    p.add_argument("--attach", action="store_true", help="上傳 17 檔 × 5 票")
    p.add_argument("--patch-epic-desc", action="store_true", help="補 TC_2972 description Egret 段")
    p.add_argument("--verify-all", action="store_true", help="GET 驗回 5 BUG")
    args = p.parse_args()

    if args.check:           return cmd_check()
    if args.create_bugs:     return cmd_create_bugs()
    if args.attach:          return cmd_attach()
    if args.patch_epic_desc: return cmd_patch_epic_desc()
    if args.verify_all:      return cmd_verify_all()
    p.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
