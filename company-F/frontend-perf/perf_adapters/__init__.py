"""perf_adapters — 進入測試頁面的方式抽象。

每個 adapter 負責：
- navigate（取得 URL → goto → 等 ready）
- list_scenarios（這個 adapter 要測幾個場景）
- enter_scenario（進入指定場景，例如進房）
- attach_listeners（可選，B2/B3 listener-based metric 用）

不負責：
- metric 計算（那是 tier 層的事）
- snapshot JS 注入（那是 perf_runner 統一做）

支援的 adapter：
- generic-url    — 純 navigate，無進房（任何網址）
- product-react  — <PRODUCT> UAT React 流程（tss URL → click_lobby_tab → enter_room）
- product-egret  — <PRODUCT> UAT Egret 流程（entry form → RootPageStore.enterGameByVid）
"""
from __future__ import annotations

from .base import AdapterBase, AdapterResult
from .generic_url import GenericUrlAdapter
from .product_react import ProductReactAdapter
from .product_egret import ProductEgretAdapter

ADAPTERS: dict[str, type[AdapterBase]] = {
    "generic-url": GenericUrlAdapter,
    "product-react": ProductReactAdapter,
    "product-egret": ProductEgretAdapter,
}


def get_adapter(name: str) -> AdapterBase:
    cls = ADAPTERS.get(name)
    if cls is None:
        raise ValueError(f"unknown adapter: {name}; available: {list(ADAPTERS)}")
    return cls()


__all__ = ["AdapterBase", "AdapterResult", "ADAPTERS", "get_adapter"]
