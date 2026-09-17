"""perf_adapters.generic_url — 純 URL navigate adapter。

適用：任何網址，不進房，只量單頁 cold-start。
list_scenarios 回單一 lobby_only 場景；enter_scenario noop。
"""
from __future__ import annotations

import time
from typing import Any

from playwright.sync_api import BrowserContext, Page

from .base import AdapterBase, AdapterResult


class GenericUrlAdapter(AdapterBase):
    name = "generic-url"

    DEFAULT_READY_TIMEOUT_MS = 60_000

    def navigate_to_lobby(
        self,
        ctx: BrowserContext,
        page: Page,
        url: str | None = None,
        ready_selector: str | None = None,
        **kwargs: Any,
    ) -> AdapterResult:
        if not url:
            return AdapterResult(error="generic-url adapter requires --url")

        timing: dict[str, int] = {}
        t0 = time.time()
        try:
            page.goto(url, wait_until="load", timeout=self.DEFAULT_READY_TIMEOUT_MS)
        except Exception as e:
            return AdapterResult(timing=timing, error=f"goto failed: {e}")
        timing["nav_ms"] = int((time.time() - t0) * 1000)

        if ready_selector:
            try:
                page.wait_for_selector(ready_selector, timeout=self.DEFAULT_READY_TIMEOUT_MS)
            except Exception as e:
                return AdapterResult(
                    timing=timing,
                    error=f"ready_selector '{ready_selector}' timeout: {e}",
                )

        timing["ready_ms"] = int((time.time() - t0) * 1000)
        return AdapterResult(timing=timing)

    def list_scenarios(self) -> list[dict[str, Any]]:
        return [{"name": "page", "type": "lobby_only", "label_zh": "目標頁"}]

    def enter_scenario(
        self,
        ctx: BrowserContext,
        page: Page,
        scenario: dict[str, Any],
    ) -> AdapterResult:
        return AdapterResult()
