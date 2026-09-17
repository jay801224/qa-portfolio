"""performance_baseline_shared.py — Performance baseline collector engine-agnostic helpers

從 performance_baseline_collector.py 抽出來的共用部分，讓 React / Egret 兩個 collector
邏輯獨立並列、各自 import 此 module，避免緊耦合與漂移。

包含：
- INIT_OBSERVER_JS：PerformanceObserver 注入腳本（LCP / CLS / longTask / event(INP)）
- SNAPSHOT_JS：navigation / paint / resource / memory / web-vitals 一次性快照
- _summarize_console：error/warning 分類
- _summarize_network：badResponse/requestFailure 分類
- _delta：snapshot B - A 增量
- _extract_lobby_metrics：snapshot → 跨 trial summary 用的關鍵指標

不包含（交各 collector 自己實作）：
- 場景定義（SCENARIOS）
- login flow（React: get_login_link.py / Egret: example.internal 表單）
- lobby ready 偵測（React: LOBBY_MENU CSS / Egret: PCPlaza module）
- room enter（React: DOM click / Egret: RootPageStore.enterGameByVid）
- room ready 偵測
- build_summary（每 collector 對自己的 SCENARIOS 寫）
- main / argparse

對應實作驗證見 [perf_shared_techniques.md](./reports/perf_shared_techniques.md)。
"""
from __future__ import annotations

from typing import Any


# ── PerformanceObserver 注入腳本 ──────────────────────────────────────────────
# 必須用 add_init_script 在 navigate 前注入。每個 context 一個獨立 observer，
# 不跨 context、不跨 page，三場景互不污染。
INIT_OBSERVER_JS = r"""
(() => {
  if (window.__perf_collector_installed__) return;
  window.__perf_collector_installed__ = true;

  const state = {
    lcp: null,
    lcpEntries: [],
    cls: 0,
    clsEntries: [],
    longTasks: [],
    inpCandidates: [],
  };
  window.__perf_state__ = state;

  try {
    const lcpObs = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        state.lcpEntries.push({
          startTime: entry.startTime,
          renderTime: entry.renderTime,
          loadTime: entry.loadTime,
          size: entry.size,
          url: entry.url,
          element: entry.element ? entry.element.tagName : null,
        });
        const t = entry.renderTime || entry.loadTime || entry.startTime;
        if (state.lcp === null || t > state.lcp) state.lcp = t;
      }
    });
    lcpObs.observe({ type: 'largest-contentful-paint', buffered: true });
  } catch (e) {}

  try {
    const clsObs = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (!entry.hadRecentInput) {
          state.cls += entry.value;
          state.clsEntries.push({
            value: entry.value,
            startTime: entry.startTime,
          });
        }
      }
    });
    clsObs.observe({ type: 'layout-shift', buffered: true });
  } catch (e) {}

  try {
    const longTaskObs = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        state.longTasks.push({
          startTime: entry.startTime,
          duration: entry.duration,
          name: entry.name,
        });
      }
    });
    longTaskObs.observe({ type: 'longtask', buffered: true });
  } catch (e) {}

  try {
    const eventObs = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (entry.duration > 16) {
          state.inpCandidates.push({
            name: entry.name,
            duration: entry.duration,
            startTime: entry.startTime,
          });
        }
      }
    });
    eventObs.observe({ type: 'event', buffered: true, durationThreshold: 16 });
  } catch (e) {}
})();
"""


# ── Web Vitals + navigation/paint/resource/memory 一次性快照 ─────────────────
SNAPSHOT_JS = r"""
() => {
  const state = window.__perf_state__ || {};
  const nav = performance.getEntriesByType('navigation')[0] || null;
  const navObj = nav ? {
    type: nav.type,
    fetchStart: nav.fetchStart,
    domainLookupStart: nav.domainLookupStart,
    domainLookupEnd: nav.domainLookupEnd,
    connectStart: nav.connectStart,
    connectEnd: nav.connectEnd,
    secureConnectionStart: nav.secureConnectionStart,
    requestStart: nav.requestStart,
    responseStart: nav.responseStart,
    responseEnd: nav.responseEnd,
    domInteractive: nav.domInteractive,
    domContentLoadedEventStart: nav.domContentLoadedEventStart,
    domContentLoadedEventEnd: nav.domContentLoadedEventEnd,
    domComplete: nav.domComplete,
    loadEventStart: nav.loadEventStart,
    loadEventEnd: nav.loadEventEnd,
    transferSize: nav.transferSize,
    encodedBodySize: nav.encodedBodySize,
    decodedBodySize: nav.decodedBodySize,
  } : null;

  const paintEntries = performance.getEntriesByType('paint');
  let fcp = null, fp = null;
  for (const p of paintEntries) {
    if (p.name === 'first-contentful-paint') fcp = p.startTime;
    if (p.name === 'first-paint') fp = p.startTime;
  }

  const resources = performance.getEntriesByType('resource');
  const totalSize = resources.reduce((s, r) => s + (r.transferSize || 0), 0);
  const totalEncoded = resources.reduce((s, r) => s + (r.encodedBodySize || 0), 0);
  const slowest = resources
    .map(r => ({
      name: r.name,
      initiatorType: r.initiatorType,
      duration: r.duration,
      transferSize: r.transferSize,
      encodedBodySize: r.encodedBodySize,
    }))
    .sort((a, b) => b.duration - a.duration)
    .slice(0, 10);

  // ── Step 2 Upgrade tier 新增 metric（A1-A4 + B4 + E4 + E5）─────────────
  // A1+A4: byMimeBucket — 副檔名/initiator 分桶 + per-bucket count/totalKB/avgKB/maxKB/maxFile
  const MIME_PATTERNS = [
    ['image',  /\.(png|jpe?g|gif|webp|svg|ico|bmp|avif)(\?|$)/i],
    ['audio',  /\.(mp3|wav|ogg|m4a|aac|flac)(\?|$)/i],
    ['video',  /\.(mp4|webm|mov|m3u8|ts)(\?|$)/i],
    ['font',   /\.(woff2?|ttf|otf|eot)(\?|$)/i],
    ['js',     /\.(js|mjs|cjs)(\?|$)/i],
    ['css',    /\.css(\?|$)/i],
    ['json',   /\.json(\?|$)/i],
    ['wasm',   /\.wasm(\?|$)/i],
  ];
  const bucketize = (url) => {
    for (const [name, re] of MIME_PATTERNS) if (re.test(url)) return name;
    return 'other';
  };
  const byMime = {};
  for (const r of resources) {
    const k = bucketize(r.name);
    if (!byMime[k]) byMime[k] = { count: 0, totalBytes: 0, maxBytes: 0, maxFile: '' };
    const b = byMime[k];
    const sz = r.transferSize || 0;
    b.count++;
    b.totalBytes += sz;
    if (sz > b.maxBytes) { b.maxBytes = sz; b.maxFile = r.name.split('/').pop().slice(0, 60); }
  }
  for (const k in byMime) {
    const b = byMime[k];
    b.totalKB = +(b.totalBytes / 1024).toFixed(1);
    b.avgKB = b.count ? +(b.totalBytes / b.count / 1024).toFixed(1) : 0;
    b.maxKB = +(b.maxBytes / 1024).toFixed(1);
    delete b.totalBytes; delete b.maxBytes;
  }

  // A2: compressionStats — transferSize/decodedBodySize < 0.9 推測有壓縮（跨 origin transferSize=0 標 unknown）
  let compressed = 0, uncompressed = 0, unknown = 0;
  const uncompressedTop = [];
  for (const r of resources) {
    const t = r.transferSize || 0;
    const d = r.decodedBodySize || 0;
    if (t === 0 && d > 0) { unknown++; continue; }  // CORS：transferSize 被擋
    if (d <= 0) { unknown++; continue; }
    const ratio = t / d;
    // gzip 典型壓縮 ratio ~0.3, brotli ~0.2; 0.85 為「真壓縮」閾值
    // (R1 post-review 校準：原 0.9 太寬鬆會把幾乎沒壓縮的也算 compressed)
    if (ratio < 0.85) compressed++;
    else { uncompressed++; uncompressedTop.push({ url: r.name, transferSize: t, decodedBodySize: d, ratio: +ratio.toFixed(3) }); }
  }
  uncompressedTop.sort((a, b) => b.decodedBodySize - a.decodedBodySize);
  const compressionStats = {
    totalCount: resources.length,
    compressedCount: compressed,
    uncompressedCount: uncompressed,
    unknownCount: unknown,
    uncompressedTop10: uncompressedTop.slice(0, 10),
  };

  // A3: byHost — 按 hostname 分桶
  const byHost = {};
  for (const r of resources) {
    let host = 'unknown';
    try { host = new URL(r.name).hostname || 'unknown'; } catch (e) {}
    byHost[host] = (byHost[host] || 0) + 1;
  }

  // A4: duplicates — 同 URL 出現多次
  const urlCount = {};
  for (const r of resources) urlCount[r.name] = (urlCount[r.name] || 0) + 1;
  const duplicates = Object.entries(urlCount)
    .filter(([_, c]) => c > 1)
    .map(([url, count]) => ({ url, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 10);

  // B4: preloadHitRate — <link rel="preload"> 是否實際被當資源載入
  const preloadLinks = Array.from(document.querySelectorAll('link[rel="preload"]'));
  const preloadHrefs = preloadLinks.map(l => l.href).filter(Boolean);
  const resourceUrls = new Set(resources.map(r => r.name));
  const preloadHits = preloadHrefs.filter(h => resourceUrls.has(h)).length;
  const preloadHitRate = {
    declared: preloadHrefs.length,
    hit: preloadHits,
    rate: preloadHrefs.length ? +(preloadHits / preloadHrefs.length).toFixed(3) : null,
    missedTop10: preloadHrefs.filter(h => !resourceUrls.has(h)).slice(0, 10),
  };

  // E5: serviceWorker — r.workerStart > 0 = 走 SW；r.deliveryType === 'cache-storage' = SW cache
  let swCount = 0, swCacheCount = 0;
  for (const r of resources) {
    if (r.workerStart && r.workerStart > 0) swCount++;
    if (r.deliveryType === 'cache-storage') swCacheCount++;
  }
  const serviceWorker = {
    workerHandledCount: swCount,
    cacheStorageCount: swCacheCount,
    rate: resources.length ? +(swCount / resources.length).toFixed(3) : null,
  };

  const mem = performance.memory ? {
    usedJSHeapSize: performance.memory.usedJSHeapSize,
    totalJSHeapSize: performance.memory.totalJSHeapSize,
    jsHeapSizeLimit: performance.memory.jsHeapSizeLimit,
  } : null;

  const inp = (state.inpCandidates && state.inpCandidates.length)
    ? Math.max(...state.inpCandidates.map(e => e.duration))
    : null;

  return {
    timestamp: Date.now(),
    url: location.href,
    title: document.title,
    domNodes: document.querySelectorAll('*').length,
    paint: { firstPaint: fp, firstContentfulPaint: fcp },
    webVitals: {
      lcp: state.lcp,
      cls: state.cls,
      inp: inp,
    },
    longTasks: {
      count: (state.longTasks || []).length,
      totalBlockingMs: (state.longTasks || []).reduce(
        (s, t) => s + Math.max(0, t.duration - 50), 0
      ),
      maxDurationMs: (state.longTasks || []).length
        ? Math.max(...(state.longTasks).map(t => t.duration))
        : 0,
      entries: (state.longTasks || []).slice(0, 30),
    },
    navigation: navObj,
    resources: {
      count: resources.length,
      totalTransferBytes: totalSize,
      totalEncodedBytes: totalEncoded,
      slowestTop10: slowest,
      byInitiator: resources.reduce((acc, r) => {
        const k = r.initiatorType || 'other';
        acc[k] = (acc[k] || 0) + 1;
        return acc;
      }, {}),
      byMimeBucket: byMime,         // Step 2 新增 (A1+A4)
      compressionStats: compressionStats,  // Step 2 新增 (A2)
      byHost: byHost,                // Step 2 新增 (A3)
      duplicates: duplicates,        // Step 2 新增 (A4)
    },
    memory: mem,
    lcpEntries: (state.lcpEntries || []).slice(-5),
    clsEntries: (state.clsEntries || []).slice(0, 30),
    preloadHitRate: preloadHitRate,  // Step 2 新增 (B4)
    serviceWorker: serviceWorker,    // Step 2 新增 (E5)
  };
}
"""


# ── Console / Network 統整 ──────────────────────────────────────────────────

def _summarize_console(console_msgs: list[dict[str, Any]]) -> dict[str, Any]:
    errors = [m for m in console_msgs if m["type"] in ("error", "warning")]
    return {
        "errorCount": sum(1 for m in console_msgs if m["type"] == "error"),
        "warningCount": sum(1 for m in console_msgs if m["type"] == "warning"),
        "errors": errors[:50],
    }


def _summarize_network(bad_responses: list, request_failures: list) -> dict[str, Any]:
    return {
        "badResponseCount": len(bad_responses),
        "badResponses": bad_responses[:50],
        "requestFailureCount": len(request_failures),
        "requestFailures": request_failures[:50],
    }


# ── Snapshot delta：B - A 的關鍵指標 ──────────────────────────────────────────

def _delta(snap_b: dict[str, Any] | None,
           snap_a: dict[str, Any] | None) -> dict[str, Any]:
    """B - A 的關鍵指標 delta（snap_a/snap_b 任一為 None → 回 None 各項）。"""
    if not snap_a or not snap_b:
        return {}
    a_lt = snap_a.get("longTasks", {}) or {}
    b_lt = snap_b.get("longTasks", {}) or {}
    a_res = snap_a.get("resources", {}) or {}
    b_res = snap_b.get("resources", {}) or {}
    a_wv = snap_a.get("webVitals", {}) or {}
    b_wv = snap_b.get("webVitals", {}) or {}
    a_mem = snap_a.get("memory", {}) or {}
    b_mem = snap_b.get("memory", {}) or {}
    return {
        "longTasksCountDelta": (b_lt.get("count") or 0) - (a_lt.get("count") or 0),
        "totalBlockingMsDelta": (b_lt.get("totalBlockingMs") or 0) - (a_lt.get("totalBlockingMs") or 0),
        "resourceCountDelta": (b_res.get("count") or 0) - (a_res.get("count") or 0),
        "resourceTransferBytesDelta": (b_res.get("totalTransferBytes") or 0) - (a_res.get("totalTransferBytes") or 0),
        "clsDelta": (b_wv.get("cls") or 0) - (a_wv.get("cls") or 0),
        "lcpAfter": b_wv.get("lcp"),  # SPA 切 route 通常不更新 LCP，記原值
        "domNodesAfter": snap_b.get("domNodes"),
        "memoryUsedDeltaMB": ((b_mem.get("usedJSHeapSize") or 0) - (a_mem.get("usedJSHeapSize") or 0)) / 1_000_000,
    }


# ── Listener-based metric helpers（B2 CDN hit / B3 WebSocket count）─────────
# 兩個 helper 從 buffer dict 抽 metric。Buffer 由 adapter.attach_listeners 收。

CDN_HIT_HEADER_HINTS = ("hit", "cached", "fresh")
CDN_MISS_HEADER_HINTS = ("miss", "expired", "stale")


def _summarize_caching(response_buffer: list[dict[str, Any]] | None) -> dict[str, Any]:
    """從 page.on('response') 收的 buffer 推斷 CDN/cache 命中。

    Buffer entry 格式：{"url": str, "status": int, "headers": dict[str, str], "from_disk_cache": bool, ...}
    """
    if not response_buffer:
        return {"fromCache": 0, "fromCDN": 0, "fromOrigin": 0,
                "top10NonCacheable": [], "totalCount": 0}

    from_cache = 0
    from_cdn = 0
    from_origin = 0
    non_cacheable: list[dict[str, Any]] = []

    for r in response_buffer:
        headers = r.get("headers") or {}
        # normalize
        cache_control = (headers.get("cache-control") or headers.get("Cache-Control") or "").lower()
        x_cache = (headers.get("x-cache") or headers.get("X-Cache") or "").lower()
        cf_cache = (headers.get("cf-cache-status") or headers.get("CF-Cache-Status") or "").lower()
        from_disk = bool(r.get("from_disk_cache"))

        if from_disk:
            from_cache += 1
        elif any(hint in x_cache for hint in CDN_HIT_HEADER_HINTS) or \
             any(hint in cf_cache for hint in CDN_HIT_HEADER_HINTS):
            from_cdn += 1
        else:
            from_origin += 1

        if "no-store" in cache_control or "no-cache" in cache_control:
            non_cacheable.append({"url": r.get("url"), "cacheControl": cache_control})

    return {
        "totalCount": len(response_buffer),
        "fromCache": from_cache,
        "fromCDN": from_cdn,
        "fromOrigin": from_origin,
        "top10NonCacheable": non_cacheable[:10],
    }


def _summarize_websocket(ws_buffer: list[dict[str, Any]] | None) -> dict[str, Any]:
    """從 page.on('websocket') 收的 buffer 算連線數 / 重連次數 / top frames。

    Buffer entry 格式：{"url": str, "frames_sent": N, "frames_received": M, "closed": bool, "open_at_ms": int}
    """
    if not ws_buffer:
        return {"connectionCount": 0, "reconnectCount": 0,
                "totalFramesSent": 0, "totalFramesReceived": 0, "top10Connections": []}

    by_url: dict[str, int] = {}
    total_sent = 0
    total_recv = 0
    for w in ws_buffer:
        url = w.get("url") or ""
        by_url[url] = by_url.get(url, 0) + 1
        total_sent += int(w.get("frames_sent") or 0)
        total_recv += int(w.get("frames_received") or 0)
    reconnects = sum(c - 1 for c in by_url.values() if c > 1)
    top_conns = sorted(by_url.items(), key=lambda kv: -kv[1])[:10]

    return {
        "connectionCount": len(ws_buffer),
        "reconnectCount": reconnects,
        "uniqueUrlCount": len(by_url),
        "totalFramesSent": total_sent,
        "totalFramesReceived": total_recv,
        "top10Connections": [{"url": u, "openCount": c} for u, c in top_conns],
    }


# ── Schema validation ──────────────────────────────────────────────────────
# C1：分兩層 validate，per-page snapshot 跟 cross-trial summary。
# Schema mismatch 應 raise（讓 collector 早爆早查），不要 silent fail。

# v1 必須欄位（4 種 PerformanceObserver entry 對應）
REQUIRED_SNAPSHOT_KEYS_V1 = ("webVitals", "longTasks", "resources", "paint")
# v2 額外欄位（perf_runner 之後跑出的 baseline 加 preloadHitRate / serviceWorker）
REQUIRED_SNAPSHOT_KEYS_V2 = REQUIRED_SNAPSHOT_KEYS_V1 + ("preloadHitRate", "serviceWorker")
# 預設 alias 指 v2（向後相容：舊 collector / 舊 baseline 用 schema_version="v1" 覆蓋）
REQUIRED_SNAPSHOT_KEYS = REQUIRED_SNAPSHOT_KEYS_V2
REQUIRED_WEBVITALS_KEYS = ("lcp", "cls", "inp")


def validate_snapshot_schema(
    snap: dict[str, Any] | None,
    *,
    raise_on_fail: bool = True,
    schema_version: str = "v2",
) -> list[str]:
    """檢查 per-page snapshot 結構。Return 缺失欄位 list。

    schema_version="v1" 用 v1 keys（給舊 baseline 既有資料 load 進來 validate 用）；
    schema_version="v2" 用 v2 keys（perf_runner.py 之後跑出的 baseline）。
    """
    if snap is None:
        if raise_on_fail:
            raise ValueError("snapshot is None")
        return ["<snapshot is None>"]
    keys = REQUIRED_SNAPSHOT_KEYS_V1 if schema_version == "v1" else REQUIRED_SNAPSHOT_KEYS_V2
    missing: list[str] = []
    for k in keys:
        if k not in snap:
            missing.append(f"snapshot.{k}")
    wv = snap.get("webVitals", {}) or {}
    for k in REQUIRED_WEBVITALS_KEYS:
        if k not in wv:
            missing.append(f"snapshot.webVitals.{k}")
    if missing and raise_on_fail:
        raise ValueError(
            f"snapshot schema mismatch (schema_version={schema_version}): missing {missing}; "
            f"check INIT_OBSERVER_JS / SNAPSHOT_JS"
        )
    return missing


REQUIRED_SUMMARY_TRIAL_KEYS = ("trial",)  # 至少要有 trial 編號，其他欄位 tier-dependent


def validate_summary_schema(summary: dict[str, Any] | None, *, raise_on_fail: bool = True) -> list[str]:
    """檢查 cross-trial summary 結構。每場景 dict 應有 trials list。"""
    if summary is None:
        if raise_on_fail:
            raise ValueError("summary is None")
        return ["<summary is None>"]
    missing: list[str] = []
    for scen_name, scen in summary.items():
        if not isinstance(scen, dict):
            missing.append(f"summary.{scen_name} (not dict)")
            continue
        if "trials" not in scen:
            missing.append(f"summary.{scen_name}.trials")
            continue
        for i, t in enumerate(scen["trials"]):
            for k in REQUIRED_SUMMARY_TRIAL_KEYS:
                if k not in t:
                    missing.append(f"summary.{scen_name}.trials[{i}].{k}")
    if missing and raise_on_fail:
        raise ValueError(f"summary schema mismatch: missing {missing}")
    return missing


# ── 跨 trial summary 的 metrics 抽取 ─────────────────────────────────────────

def _extract_lobby_metrics(snap: dict[str, Any] | None) -> dict[str, Any]:
    """從一個 snapshot 抽出大廳常用指標（用於 cross-trial summary）。"""
    if not snap:
        return {}
    wv = snap.get("webVitals", {}) or {}
    lt = snap.get("longTasks", {}) or {}
    paint = snap.get("paint", {}) or {}
    res = snap.get("resources", {}) or {}
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
        "memoryUsedMB": (snap.get("memory") or {}).get("usedJSHeapSize", 0) / 1_000_000,
    }
