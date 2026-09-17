"""jira_ticket_perf_design_candidates.py — 對 3 張「>=90% 認為不是 bug」的 perf 票留言

依 2026-05-08 cross-check 結果（C1~C5 已跑），對下列 3 張票自動留言請研發協助確認：
  - TC_2977（React @<PRODUCT>/* workspace warnings — 95% 認為是 build-time 噪音）
  - TC_3000（Egret CLS 0.3559 POOR  — 92% 認為機制是 canvas resize 設計）
  - TC_3003（Egret GameShb +782 KB  — 95% 認為是不同遊戲資產差異）

證據：[perf_comparison_react_vs_egret_20260507_180000.md](
  perf_comparison_react_vs_egret_20260507_180000.md)
"""
from __future__ import annotations

import sys
from pathlib import Path

from dotenv import load_dotenv

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "shared" / "jira"))

load_dotenv(ROOT / ".env", override=True)
load_dotenv(ROOT / "react" / ".env", override=True)

from jira_bot import add_comment  # noqa: E402


CUI_2977_BODY = """[Claude 自動化交叉驗證 — 2026-05-08]

更新：經過 cross-check 後，我有約 95% 把握認為這張票記錄的現象「不是 runtime bug，而是 monorepo build-time 配置警告」，請研發協助確認。

---

## 一度懷疑的點
workspace:* 警告重複 16+ 次，是否導致實際行為錯誤（例如載入到錯版本套件）。

## Cross-check 結果
- Warning 來自 @<PRODUCT>/ui / @<PRODUCT>/core 的 workspace:* 版本協商，發生在 module bootstrap 階段
- 同一 trial 大廳功能正常進入、tab 切換成功、進房成功；warning 沒對應任何 4xx / 5xx / requestfailed
- console errorCount=18 跨 trial 一致，warning 量隨 React 模組載入量自然成長（trial 1=1210 / trial 2=629），都不影響功能

## 信心度
~95% 認為是 build-time noise 而非 runtime bug。剩 5% 留給「workspace:* 在某些 edge case 是否實際 fallback 到錯版本」的可能。

## 請研發協助確認
1. @<PRODUCT>/ui / @<PRODUCT>/core 的 workspace:* 解析是 build 時 lock，還是 runtime 才 negotiate
2. 若是 build-time lock：建議降為 example.internal 或在 production 抑制以降低噪音
3. 若是 runtime negotiate：才需要進入修復流程

## 對應證據
- reports/performance_baseline_20260507_115737/trial_1/lobby.json 的 console warning 段
- 對比報告：reports/perf_comparison_react_vs_egret_20260507_180000.md
"""


CUI_3000_BODY = """[Claude 自動化交叉驗證 — 2026-05-08]

更新：經過 cross-check 後，我有約 92% 把握認為這張票的 CLS 0.3559 POOR「值是真實的、但機制是設計選擇 (deterministic single canvas resize shift)」，請研發協助評估是否要納入設計改善。

---

## 一度懷疑的點
跨 6 個 fresh browser context × 3 場景，CLS 值差異 < 0.0001，懷疑是 PerformanceObserver 沒裝好或讀取 buffered 重複導致假數據。

## Cross-check 結果
1. **clsEntries 跨 6 trials × 10 個 entry，主 shift 值 bit-for-bit 完全相同** = 0.3558256172839506（16 位小數）→ 數學上不可能是隨機噪音，必為固定 input × 固定公式
2. clsEntries[0].startTime 在 1247-1606ms 之間（每個 ctx 內部一致），落在 canvas mount 時刻
3. 每個 ctx 內 snap_a (lobby) 和 snap_b (after room) 的 clsEntries[0] 時間相同 → 進房沒觸發新 shift
4. 主 shift 之外另有 16 個 sub-3e-5 微 shift（總 < 0.0001），代表 observer 確實在持續監聽，並非鎖死

## 推測機制
Egret canvas 從預留尺寸 → 1920x1080 final 的單次 resize，每次冷啟 100% 必發。

## 信心度
~92% 認為機制是設計選擇。剩 8% 留給 R&D 確認 PCPlaza canvas 初始化流程是否符合此假設。

## 請研發協助確認
1. PCPlaza 大廳 canvas 是否存在「初始預留尺寸 → 1920x1080 final」的單次 resize（如 EgretEngine canvas 自適應流程）
2. 若是設計：是否能改為 SSR 或 inline 設定 viewport，避免 layout shift（因 CLS 0.3559 仍超過 Web Vitals POOR 閾值 0.25，雖機制是設計，但對使用者觀感仍是 perf 問題）
3. 若不是設計：才需要進入修復流程

## 對應證據
- reports/performance_baseline_egret_20260507_171832/trial_1/lobby.json 的 clsEntries 段
- reports/performance_baseline_egret_20260507_171832/observation.md
- 對比報告：reports/perf_comparison_react_vs_egret_20260507_180000.md
"""


CUI_3003_BODY = """[Claude 自動化交叉驗證 — 2026-05-08]

更新：經過 cross-check 後，我有約 95% 把握認為這張票記錄的「GameShb 比 GameBac 多 782 KB」不是 bug，而是兩遊戲資產量本來就不同的設計差異，請研發確認是否能進一步壓縮，否則建議降為 backlog 或關票。

---

## 一度懷疑的點
GameShb module 是否多打包了不該載入的資源（例如重複 dependency 或未壓縮素材）。

## Cross-check 結果
- 跨 4 trials 進房 Δ resource 比對：bac +34 個 / +1009-1115 KB；sicbo +34 個 / +1897 KB
- 主要差距來源：GameShb 的路單 PNG (~320 KB) + 桌面 JPG (~107 KB) — 都是 sicbo 特有需求（骰寶路單呈現方式跟百家樂不同）
- Δ resource count 兩遊戲都是 +34，意味著「資源數量沒多」，只有「個別資源體積較大」

## 信心度
~95% 認為是不同遊戲不同資產的設計差異，非 regression bug。剩 5% 留給 R&D 評估「骰寶路單能否進一步壓縮或改用 SVG」。

## 請研發協助確認
1. 骰寶路單 PNG ~320 KB 是否能改用 SVG 或更小尺寸（路單本質上是格線圖，向量化通常更小）
2. 骰寶桌面 JPG ~107 KB 是否可調整壓縮率（目前可能是 quality=90，可降至 80）
3. 若以上兩項都已最佳化、無優化空間：建議關票或降為 backlog

## 對應證據
- 對比報告：reports/perf_comparison_react_vs_egret_20260507_180000.md 中段 B「進房 Δ 對照（room - lobby）」表
- reports/performance_baseline_egret_20260507_171832/observation.md
"""


CANDIDATES = [
    ("TC_2977", CUI_2977_BODY),
    ("TC_3000", CUI_3000_BODY),
    ("TC_3003", CUI_3003_BODY),
]


def main() -> int:
    print(f"\n[design-candidate comments] 對 {len(CANDIDATES)} 張票留言（skip_duplicate=True）：\n")
    posted = 0
    skipped = 0
    failed = 0
    for key, body in CANDIDATES:
        print(f"  -> {key} ...", end=" ", flush=True)
        try:
            ok = add_comment(key, body, skip_duplicate=True)
            if ok:
                print("posted")
                posted += 1
            else:
                print("skipped (duplicate)")
                skipped += 1
        except Exception as e:
            print(f"FAILED: {e}")
            failed += 1
    print(f"\n結果：posted={posted}, skipped={skipped}, failed={failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
