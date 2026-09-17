"""perf_tiers — 量測指標範圍（cumulative tier）。

Basic    → Web Vitals 5 + DOM/resource count + memory + console + 4xx + nav wall clock
Upgrade  → Basic + 進房 Δ + byMime + byHost + duplicates + compression + cacheStats + wsStats
                  + preloadHitRate + memoryGrowth + SW 介入率
Advanced → Upgrade + 互動延遲 + CDP coverage + Dashboard + 多 user 對比（stub，下次做）

每個 tier 負責：
- extract_summary_metrics(snap, listener_buffer) → dict — 從 raw snapshot 抽 cross-trial summary 用的關鍵指標
- print_scenario_summary(scenario_result) → None — 印 trial 結果到 console

不負責：
- snapshot 取值（perf_runner 統一呼叫 SNAPSHOT_JS）
- listener 註冊（adapter 層）
"""
from __future__ import annotations

from .base import TierBase
from .basic import BasicTier
from .upgrade import UpgradeTier
from .advanced import AdvancedTier

TIERS: dict[str, type[TierBase]] = {
    "basic": BasicTier,
    "upgrade": UpgradeTier,
    "advanced": AdvancedTier,
}


def get_tier(name: str) -> TierBase:
    cls = TIERS.get(name)
    if cls is None:
        raise ValueError(f"unknown tier: {name}; available: {list(TIERS)}")
    return cls()


__all__ = ["TierBase", "TIERS", "get_tier"]
