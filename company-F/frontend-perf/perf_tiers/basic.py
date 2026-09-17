"""perf_tiers.basic — Basic tier：Web Vitals 5 + 基本健康。

包含：
- LCP / CLS / INP / FCP（Web Vitals 4 from PerformanceObserver）
- TBT / longTasks count / maxLongTaskMs（Lighthouse 風格）
- DOM nodes / resource count / resource transfer bytes
- memory used MB
- console error/warning count + 4xx-5xx count
- nav / ready wall clock

不包含：
- byMime / byHost / duplicates / compression（→ Upgrade）
- cacheStats / wsStats（→ Upgrade，listener-based）
- 互動延遲 / CDP coverage（→ Advanced）
"""
from __future__ import annotations

from typing import Any

from .base import TierBase


class BasicTier(TierBase):
    name = "basic"

    def extract_summary_metrics(
        self,
        snap: dict[str, Any] | None,
        listener_buffer: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if not snap:
            return {}
        wv = snap.get("webVitals", {}) or {}
        lt = snap.get("longTasks", {}) or {}
        paint = snap.get("paint", {}) or {}
        res = snap.get("resources", {}) or {}
        mem = snap.get("memory") or {}
        return {
            "lcp": wv.get("lcp"),
            "cls": wv.get("cls"),
            "inp": wv.get("inp"),
            "fcp": paint.get("firstContentfulPaint"),
            "longTasksCount": lt.get("count"),
            "totalBlockingMs": lt.get("totalBlockingMs"),
            "maxLongTaskMs": lt.get("maxDurationMs"),
            "domNodes": snap.get("domNodes"),
            "resourceCount": res.get("count"),
            "resourceTransferBytes": res.get("totalTransferBytes"),
            "memoryUsedMB": mem.get("usedJSHeapSize", 0) / 1_000_000 if mem else None,
        }

    def print_scenario_summary(self, scenario_result: dict[str, Any]) -> None:
        name = scenario_result.get("scenario", "?")
        err = scenario_result.get("error")
        if err:
            print(f"  [{name}] WARN {err}")
        # R5: lobby_only 用 snapshot；lobby_then_room 用 snapshot_a_lobby（進房前那段才是 lobby Web Vitals）
        snap = (scenario_result.get("snapshot")
                or scenario_result.get("snapshot_a_lobby")
                or {})
        if not snap:
            print(f"  [{name}] (no snapshot)")
            return
        wv = snap.get("webVitals", {}) or {}
        lt = snap.get("longTasks", {}) or {}
        paint = snap.get("paint", {}) or {}
        cls = wv.get("cls")
        cls_str = f"{cls:.4f}" if isinstance(cls, (int, float)) else "N/A"
        tbt = lt.get("totalBlockingMs", 0)
        tbt_str = f"{tbt:.0f}" if isinstance(tbt, (int, float)) else "N/A"
        print(
            f"  [{name:22s}] LCP={wv.get('lcp')}  CLS={cls_str}  INP={wv.get('inp')}  "
            f"FCP={paint.get('firstContentfulPaint')}  longTasks={lt.get('count')}  "
            f"TBT~{tbt_str}ms  DOM={snap.get('domNodes')}"
        )
        # console / network stats
        console = scenario_result.get("console", {}) or {}
        network = scenario_result.get("network", {}) or {}
        print(
            f"    console err={console.get('errorCount', 0)} warn={console.get('warningCount', 0)}  "
            f"4xx-5xx={network.get('badResponseCount', 0)}  "
            f"reqFail={network.get('requestFailureCount', 0)}"
        )
