"""perf_adapters.product_egret — PRODUCT <PRODUCT> UAT Egret adapter。

從 performance_baseline_collector_egret.py 抽出 Egret 客製流程：
- example.internal/uatgame/ <PRODUCT> form click
- ctx.expect_page() 抓新分頁（new_page swap 後續用之）
- PCPlaza module wait
- 進房：RootPageStore._instance.enterGameByVid(vid)（vid 從 RoomConfig 動態取）
- 三場景預設：lobby (PCPlaza) / baccarat_room (BAC GameBac) / sicbo_room (SHB GameShb)
"""
from __future__ import annotations

import time
from typing import Any

from playwright.sync_api import BrowserContext, Page

from .base import AdapterBase, AdapterResult


class ProductEgretAdapter(AdapterBase):
    name = "product-egret"

    SCENARIOS: list[dict[str, Any]] = [
        {"name": "lobby", "label_zh": "大廳 (PCPlaza)", "type": "lobby_only",
         "expected_module": "PCPlaza"},
        {"name": "baccarat_room", "label_zh": "百家樂 BAC 第一桌",
         "type": "lobby_then_room", "gmtype": "BAC", "expected_module": "GameBac"},
        {"name": "sicbo_room", "label_zh": "骰寶 SHB 第一桌",
         "type": "lobby_then_room", "gmtype": "SHB", "expected_module": "GameShb"},
    ]

    ENTRY_URL = "https://example.internal/uatgame/"
    DEFAULT_USER = "USER01"
    DEFAULT_PID = "PID01"
    LOBBY_READY_TIMEOUT_MS = 60_000
    ROOM_READY_TIMEOUT_MS = 30_000

    def navigate_to_lobby(
        self,
        ctx: BrowserContext,
        page: Page,
        url: str | None = None,
        user: str = DEFAULT_USER,
        pid: str = DEFAULT_PID,
        **kwargs: Any,
    ) -> AdapterResult:
        # url 參數忽略 — Egret 走 entry form 而非直接 URL
        # （未來支援 --url 直接帶完整 lobby URL 是可能的，但這裡先按現行流程）
        timing: dict[str, int] = {}
        t0 = time.time()
        try:
            entry_page = ctx.new_page()
            entry_page.goto(self.ENTRY_URL, wait_until="load", timeout=60_000)

            # <PRODUCT> 區塊 USER 下拉切到 USER01（如非 default）
            if user != "UAT01":
                entry_page.get_by_role("button", name="USER UAT01").first.click()
                entry_page.get_by_role("option", name=user).first.click()

            if pid != "PID01":
                entry_page.get_by_role("button", name="PID PID01").first.click()
                entry_page.get_by_role("option", name=pid).first.click()

            with ctx.expect_page() as new_pp:
                entry_page.get_by_role("button", name="Enter AGIN").click()
            lobby_page = new_pp.value
            timing["login_ms"] = int((time.time() - t0) * 1000)

            try:
                entry_page.close()
            except Exception:
                pass

        except Exception as e:
            return AdapterResult(timing=timing, error=f"entry login failed: {e}")

        # 等 PCPlaza module ready
        t1 = time.time()
        if not self._wait_module(lobby_page, "PCPlaza", self.LOBBY_READY_TIMEOUT_MS):
            return AdapterResult(
                timing=timing,
                new_page=lobby_page,
                error="PCPlaza module not ready in time",
            )
        timing["ready_ms"] = int((time.time() - t1) * 1000)
        return AdapterResult(timing=timing, new_page=lobby_page)

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

        gmtype = scenario["gmtype"]
        expected_module = scenario["expected_module"]
        timing: dict[str, int] = {}

        t_lookup = time.time()
        vid = self._get_first_vid(page, gmtype)
        timing["vid_lookup_ms"] = int((time.time() - t_lookup) * 1000)
        if not vid:
            return AdapterResult(timing=timing, error=f"no vid found for gmtype={gmtype}")

        t_enter = time.time()
        self._enter_game_by_vid(page, vid)
        if not self._wait_module(page, expected_module, self.ROOM_READY_TIMEOUT_MS):
            timing["room_enter_ms"] = int((time.time() - t_enter) * 1000)
            return AdapterResult(
                timing=timing,
                error=f"{expected_module} not ready after enterGameByVid({vid})",
            )
        timing["room_enter_ms"] = int((time.time() - t_enter) * 1000)
        return AdapterResult(timing=timing, extra={"used_vid": vid, "module": expected_module})

    @staticmethod
    def _wait_module(page: Page, expected: str, timeout: int) -> bool:
        try:
            page.wait_for_function(
                f"() => {{"
                f"  const inst = window.PCPlaza && window.PCPlaza.RootPageStore && "
                f"               window.PCPlaza.RootPageStore._instance;"
                f"  return inst && inst.getCurrentModule && inst.getCurrentModule() === '{expected}';"
                f"}}",
                timeout=timeout,
            )
            return True
        except Exception:
            return False

    @staticmethod
    def _get_first_vid(page: Page, gmtype: str) -> str | None:
        return page.evaluate(
            f"""() => {{
                const rc = window.VideoGameCore && window.VideoGameCore.RoomConfig &&
                           window.VideoGameCore.RoomConfig.instance;
                if (!rc) return null;
                const list = rc.getRoomInfosByType('{gmtype}');
                return Array.isArray(list) && list.length > 0 ? list[0].vid : null;
            }}"""
        )

    @staticmethod
    def _enter_game_by_vid(page: Page, vid: str) -> None:
        page.evaluate(
            f"""() => {{
                const inst = window.PCPlaza.RootPageStore._instance;
                inst.enterGameByVid('{vid}');
            }}"""
        )
