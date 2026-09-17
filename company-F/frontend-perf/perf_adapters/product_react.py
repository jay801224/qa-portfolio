"""perf_adapters.product_react — PRODUCT <PRODUCT> UAT React adapter。

從 performance_baseline_collector.py 抽出 React 客製流程：
- get_login_link.py 取 tss URL
- LOBBY_MENU CSS 等大廳 ready
- 進房：click_lobby_tab + enter_room（DOM 點擊）
- 三場景預設：lobby / baccarat_room (N006) / sicbo_room (N026)
"""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from playwright.sync_api import BrowserContext, Page

from .base import AdapterBase, AdapterResult


class ProductReactAdapter(AdapterBase):
    name = "product-react"

    SCENARIOS: list[dict[str, Any]] = [
        {"name": "lobby", "label_zh": "大廳", "type": "lobby_only"},
        {
            "name": "baccarat_room",
            "label_zh": "百家樂房間 N006",
            "type": "lobby_then_room",
            "tab": "百家樂",
            "room": "N006",
        },
        {
            "name": "sicbo_room",
            "label_zh": "骰寶房間 N026",
            "type": "lobby_then_room",
            "tab": "骰寶",
            "room": "N026",
        },
    ]

    GAME_ROOM_READY_UNION = (
        '[class*="PcMainGame_timer"],[class*="PlayTypeText"],'
        '[class*="bet-item-gr"],[class*="timer_container"],'
        '[class*="GameInfo"],[class*="RoadMap"]'
    )

    DEFAULT_LOGIN_TIMEOUT_MS = 60_000

    def navigate_to_lobby(
        self,
        ctx: BrowserContext,
        page: Page,
        url: str | None = None,
        env: str = "uat",
        pid: str = "<ACCOUNT>",
        **kwargs: Any,
    ) -> AdapterResult:
        if not url:
            url = self._get_login_url(env, pid)
        if not url:
            return AdapterResult(error="get_login_link.py failed to produce URL")

        from react_client_selectors import LOBBY_MENU

        timing: dict[str, int] = {}
        t0 = time.time()
        try:
            page.goto(url, wait_until="load", timeout=self.DEFAULT_LOGIN_TIMEOUT_MS)
        except Exception as e:
            return AdapterResult(error=f"goto failed: {e}")
        timing["nav_ms"] = int((time.time() - t0) * 1000)

        try:
            page.wait_for_selector(LOBBY_MENU, timeout=self.DEFAULT_LOGIN_TIMEOUT_MS)
        except Exception as e:
            return AdapterResult(
                timing=timing,
                error=f"LOBBY_MENU ready timeout: {e}",
            )
        timing["ready_ms"] = int((time.time() - t0) * 1000)
        return AdapterResult(timing=timing)

    def list_scenarios(self) -> list[dict[str, Any]]:
        return self.SCENARIOS

    def enter_scenario(
        self,
        ctx: BrowserContext,
        page: Page,
        scenario: dict[str, Any],
    ) -> AdapterResult:
        if scenario["type"] == "lobby_only":
            return AdapterResult()

        from react_client_autobet import click_lobby_tab, enter_room
        from react_client_selectors import GAME_CARD_READY

        timing: dict[str, int] = {}

        t_tab = time.time()
        if not click_lobby_tab(page, scenario["tab"]):
            return AdapterResult(error=f"click_lobby_tab failed for {scenario['tab']}")
        try:
            page.wait_for_selector(GAME_CARD_READY, timeout=15_000)
        except Exception:
            pass
        timing["tab_ms"] = int((time.time() - t_tab) * 1000)

        t_room = time.time()
        if not enter_room(page, scenario["room"]):
            return AdapterResult(
                timing=timing,
                error=f"enter_room({scenario['room']}) failed",
            )
        try:
            page.wait_for_selector(self.GAME_ROOM_READY_UNION, timeout=30_000)
        except Exception as e:
            timing["room_enter_ms"] = int((time.time() - t_room) * 1000)
            return AdapterResult(timing=timing, error=f"room ready timeout: {e}")
        timing["room_enter_ms"] = int((time.time() - t_room) * 1000)
        timing["total_enter_room_ms"] = int((time.time() - t_tab) * 1000)
        return AdapterResult(timing=timing, extra={"room": scenario["room"]})

    @staticmethod
    def _get_login_url(env: str = "uat", pid: str = "<ACCOUNT>") -> str | None:
        here = Path(__file__).resolve().parent.parent
        script = here / "get_login_link.py"
        try:
            proc = subprocess.run(
                [sys.executable, str(script), "--env", env, "--pid", pid],
                capture_output=True, text=True, encoding="utf-8", errors="replace",
                timeout=60,
            )
        except Exception:
            return None
        out = (proc.stdout or "") + "\n" + (proc.stderr or "")
        for line in out.splitlines():
            line = line.strip()
            if line.startswith("https://") and "tss=" in line:
                return line
        return None
