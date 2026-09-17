"""perf_tiers.advanced — Advanced tier：stub（下個 deliverable 實作）。

預計含：
- B1 互動延遲 collector（按鈕點下→反饋 wall-clock）
- E1 跨平台 Dashboard（HTML 產生器吃 N 份 baseline summary）
- E2 多 user / 多 pid 對比
- E3 CDP coverage（unused asset / JS execution profile）

呼叫即 raise NotImplementedError 提示 user 用 Upgrade tier 或等下次 release。
"""
from __future__ import annotations

from typing import Any

from .upgrade import UpgradeTier


class AdvancedTier(UpgradeTier):
    name = "advanced"

    _NOT_READY_MSG = (
        "Advanced tier 尚未實作（B1 互動延遲 / E1 Dashboard / E2 多 user / E3 CDP coverage）。\n"
        "請改用 --tier upgrade，或等下個 deliverable 推出。"
    )

    def extract_summary_metrics(
        self,
        snap: dict[str, Any] | None,
        listener_buffer: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        raise NotImplementedError(self._NOT_READY_MSG)

    def print_scenario_summary(self, scenario_result: dict[str, Any]) -> None:
        # R3: 印訊息而非 raise — extract_summary_metrics 會早爆，這裡只負責顯示
        # 讓 user 跑 advanced tier 時看到清楚 stub 訊息而非堆疊 traceback
        name = scenario_result.get("scenario", "?")
        first_line = self._NOT_READY_MSG.splitlines()[0]
        print(f"  [{name}] (advanced tier — {first_line})")
