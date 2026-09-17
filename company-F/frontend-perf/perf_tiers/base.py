"""perf_tiers.base — Tier ABC。

接口：
    class MyTier(TierBase):
        name = "my-tier"

        def extract_summary_metrics(self, snap: dict, listener_buffer: dict) -> dict:
            # 從 SNAPSHOT_JS 抓的 raw snap + adapter 收的 listener buffer
            # 抽出本 tier 關心的關鍵指標
            return {"lcp": snap["webVitals"]["lcp"], ...}

        def print_scenario_summary(self, scenario_result: dict) -> None:
            # 印簡短或詳細 summary 到 console
            ...
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class TierBase(ABC):
    name: str = "base"

    @abstractmethod
    def extract_summary_metrics(
        self,
        snap: dict[str, Any] | None,
        listener_buffer: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """從 raw snapshot + listener buffer 抽 summary 用的關鍵指標。"""

    def print_scenario_summary(self, scenario_result: dict[str, Any]) -> None:
        """印 trial 結果（預設簡短）。Tier 可 override 自訂格式。"""
        name = scenario_result.get("scenario", "?")
        err = scenario_result.get("error")
        if err:
            print(f"  [{name}] WARN {err}")
        snap = scenario_result.get("snapshot") or {}
        wv = snap.get("webVitals", {}) or {}
        print(
            f"  [{name}] LCP={wv.get('lcp')}  CLS={wv.get('cls')}  "
            f"INP={wv.get('inp')}  tier={self.name}"
        )
