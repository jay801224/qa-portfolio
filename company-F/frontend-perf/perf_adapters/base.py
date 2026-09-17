"""perf_adapters.base — Adapter ABC + AdapterResult dataclass。

設計：adapter 負責 page lifecycle（navigate / 進房 / listener 註冊），
不碰 metric 計算（那是 tier 層的事）。

接口：
    class MyAdapter(AdapterBase):
        name = "my-adapter"

        def navigate_to_lobby(self, ctx, page, url=None) -> AdapterResult:
            # 用 page.goto / wait_for_selector 等等
            return AdapterResult(timing={"login_ms": 1234, "ready_ms": 5678})

        def list_scenarios(self) -> list[dict]:
            return [{"name": "lobby", "type": "lobby_only"}]

        def enter_scenario(self, ctx, page, scenario) -> AdapterResult:
            # 進入 scenario["name"] 對應的子頁/房間
            return AdapterResult(timing={"room_enter_ms": 42})

        def attach_listeners(self, page) -> dict:
            # 可選 — 註冊 page.on('response') / page.on('websocket') 等
            # Return: {"responses": [...], "websockets": [...]} buffer
            return {}
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from playwright.sync_api import BrowserContext, Page


@dataclass
class AdapterResult:
    """Adapter 操作的結果（navigate / enter_scenario）回傳。"""
    timing: dict[str, int] = field(default_factory=dict)  # 各種 wall clock ms
    error: str | None = None
    new_page: Any | None = None  # Egret entry form 流程會 swap 到新分頁；若 None perf_runner 沿用原 page
    extra: dict[str, Any] = field(default_factory=dict)  # adapter 特定欄位（如 used_vid）


class AdapterBase(ABC):
    name: str = "base"

    @abstractmethod
    def navigate_to_lobby(
        self,
        ctx: BrowserContext,
        page: Page,
        url: str | None = None,
        **kwargs: Any,
    ) -> AdapterResult:
        """Navigate 到 lobby（或 generic adapter 的目標 URL）並等 ready。
        url=None 時 adapter 自己決定（如 product-react 跑 get_login_link）。
        """

    @abstractmethod
    def list_scenarios(self) -> list[dict[str, Any]]:
        """Return 此 adapter 支援的場景列表。
        每個 dict 至少含 {"name": str, "type": "lobby_only" | "lobby_then_room"}。
        """

    @abstractmethod
    def enter_scenario(
        self,
        ctx: BrowserContext,
        page: Page,
        scenario: dict[str, Any],
    ) -> AdapterResult:
        """進入指定 scenario（如點 tab + 點房卡）。
        lobby_only 場景：noop 直接 return。
        lobby_then_room 場景：進房後 wait ready，return timing 含 room_enter_ms。
        """

    def attach_listeners(
        self,
        ctx: BrowserContext,
        page: Page,
        buffer: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """註冊 B2/B3 listener（page-level，可重複呼叫對多個 page 共用 buffer）。

        R6 fix: 原本用 ctx.on('response')，但 Playwright Python sync API 的 ctx-level
        response/websocket event 不 fire（實測 cacheStats 永遠 0）。改用 page.on(...)。
        對 Egret swap page 場景，perf_runner 對 new_page 再呼一次 attach_listeners 並
        傳入既有 buffer，讓兩個 page 共用同個 list 累積。

        Return: buffer dict {"responses": list, "websockets": list}
        """
        if buffer is None:
            buffer = {"responses": [], "websockets": []}
        responses: list[dict[str, Any]] = buffer.setdefault("responses", [])
        websockets: list[dict[str, Any]] = buffer.setdefault("websockets", [])

        def _on_response(resp):
            # R6 fix: 用 resp.headers (sync dict 屬性) 而非 resp.header_value() (async)
            # 後者在 ctx.close() race window 內會 raise asyncio.CancelledError → listener 漏收
            # 包 BaseException 是因為 asyncio.CancelledError 在 Python 3.8+ 不繼承 Exception
            try:
                all_headers = getattr(resp, "headers", None) or {}
                # Playwright spec: response.headers 是 lowercase dict
                headers = {}
                for hdr_name in ("cache-control", "x-cache", "cf-cache-status",
                                 "age", "etag", "last-modified", "vary"):
                    val = all_headers.get(hdr_name)
                    if val:
                        headers[hdr_name] = val
                responses.append({
                    "url": resp.url,
                    "status": resp.status,
                    "headers": headers,
                    # R6 root cause: from_service_worker 是 Playwright Response 的 bool 屬性
                    # 不是 method —— 之前寫 `getattr(...)()` 加括號變 bool() 觸發 TypeError，
                    # 全部 31 個 response 進 except 路徑 → cacheStats 永遠 0
                    "from_service_worker": getattr(resp, "from_service_worker", False),
                })
            except BaseException:
                pass

        def _on_ws(ws):
            entry = {
                "url": ws.url,
                "frames_sent": 0,
                "frames_received": 0,
                "closed": False,
            }
            websockets.append(entry)

            def _inc_sent(_payload):
                entry["frames_sent"] += 1

            def _inc_recv(_payload):
                entry["frames_received"] += 1

            def _on_close():
                entry["closed"] = True

            try:
                ws.on("framesent", _inc_sent)
                ws.on("framereceived", _inc_recv)
                ws.on("close", _on_close)
            except Exception:
                pass

        try:
            page.on("response", _on_response)
            page.on("websocket", _on_ws)
        except Exception:
            pass

        return buffer
