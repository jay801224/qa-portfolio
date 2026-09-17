"""perf_tiers.upgrade — Upgrade tier：Basic + 進房 Δ + 資源分桶 + listener-based metric。

Basic 之上新增：
- A1 byMimeBucket per-MIME { count / totalKB / avgKB / maxKB / maxFile }
- A2 compressionStats { totalCount / compressedCount / uncompressedTop10 }
- A3 byHost { hostname: count }
- A4 duplicates [{ url, count }] top 10
- B2 cacheStats { fromCache / fromCDN / fromOrigin / top10NonCacheable } — listener
- B3 wsStats { connectionCount / reconnectCount / top10Frames } — listener
- B4 preloadHitRate
- E4 memoryGrowthMB（cross-trial 計算）
- E5 SW 介入率
- 進房 Δ（room - lobby snapshot diff，由 perf_runner 算）

注意：byMime / byHost / dup / compression / preloadHitRate / SW 由 SNAPSHOT_JS extras 取（Step 2 加進去）；
cacheStats / wsStats 由 adapter.attach_listeners 收 buffer，本 tier 從 buffer 抽（Step 3 加 helper）。
"""
from __future__ import annotations

from typing import Any

from performance_baseline_shared import _summarize_caching, _summarize_websocket

from .basic import BasicTier


class UpgradeTier(BasicTier):
    name = "upgrade"

    def extract_summary_metrics(
        self,
        snap: dict[str, Any] | None,
        listener_buffer: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        out = super().extract_summary_metrics(snap, listener_buffer)
        if snap:
            res = snap.get("resources", {}) or {}
            out["byMimeBucket"] = res.get("byMimeBucket")
            out["byHost"] = res.get("byHost")
            out["duplicates"] = res.get("duplicates")
            out["compressionStats"] = res.get("compressionStats")
            out["preloadHitRate"] = snap.get("preloadHitRate")
            out["serviceWorker"] = snap.get("serviceWorker")
        # Listener buffer → cacheStats / wsStats（B2/B3）
        if listener_buffer:
            out["cacheStats"] = _summarize_caching(listener_buffer.get("responses"))
            out["wsStats"] = _summarize_websocket(listener_buffer.get("websockets"))
        return out

    def print_scenario_summary(self, scenario_result: dict[str, Any]) -> None:
        super().print_scenario_summary(scenario_result)
        # R5: 同 basic.py — lobby_then_room 用 snapshot_a_lobby
        snap = (scenario_result.get("snapshot")
                or scenario_result.get("snapshot_a_lobby")
                or {})
        res = snap.get("resources", {}) or {}
        # 顯示資源分桶摘要
        by_mime = res.get("byMimeBucket")
        if by_mime:
            top_buckets = sorted(
                ((k, v.get("count", 0), v.get("totalKB", 0)) for k, v in by_mime.items()),
                key=lambda x: -x[1],
            )[:3]
            mime_str = ", ".join(f"{k}={c}/{kb:.0f}KB" for k, c, kb in top_buckets)
            print(f"    byMime top3: {mime_str}")
        comp = res.get("compressionStats")
        if comp:
            print(
                f"    compression: {comp.get('compressedCount', 0)}/{comp.get('totalCount', 0)} "
                f"compressed; uncompressed top10 hidden in raw"
            )
        # 進房 Δ
        delta = scenario_result.get("delta_room_vs_lobby")
        if delta:
            cls_d = delta.get("clsDelta", 0)
            tbt_d = delta.get("totalBlockingMsDelta", 0)
            res_d = delta.get("resourceCountDelta", 0)
            kb_d = (delta.get("resourceTransferBytesDelta", 0) or 0) / 1024
            mem_d = delta.get("memoryUsedDeltaMB", 0)
            print(
                f"    Δ room vs lobby: TBT +{tbt_d}ms / longTasks +{delta.get('longTasksCountDelta', 0)} / "
                f"resource +{res_d}/+{kb_d:.0f}KB / CLSΔ={cls_d:+.4f} / memΔ={mem_d:+.2f}MB"
            )
