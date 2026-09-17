"""
test_jira.py — Jira API 連線測試

驗證:
    - Jira 伺服器可達
    - 認證有效
    - 查詢 API 正常運作
"""

import time
import pytest
import requests
from requests.auth import HTTPBasicAuth


def _auth(jira_config):
    """建立 HTTP Basic Auth"""
    return HTTPBasicAuth(jira_config["email"], jira_config["token"])


def test_jira_server_reachable(jira_config):
    """Jira 伺服器應可連線"""
    if not jira_config["configured"]:
        pytest.skip("Jira 未設定（JIRA_URL / JIRA_EMAIL / JIRA_API_TOKEN）")

    resp = requests.get(
        f"{jira_config['url']}/rest/api/2/serverInfo",
        auth=_auth(jira_config),
        timeout=10,
    )
    assert resp.status_code == 200, f"HTTP {resp.status_code}"
    data = resp.json()
    assert "serverTitle" in data or "baseUrl" in data, \
        f"非預期的 serverInfo 回應: {list(data.keys())}"


def test_jira_auth_valid(jira_config):
    """Jira 認證應有效"""
    if not jira_config["configured"]:
        pytest.skip("Jira 未設定")

    resp = requests.get(
        f"{jira_config['url']}/rest/api/2/myself",
        auth=_auth(jira_config),
        timeout=10,
    )
    assert resp.status_code == 200, \
        f"認證失敗: HTTP {resp.status_code} — 請檢查 JIRA_EMAIL 和 JIRA_API_TOKEN"
    data = resp.json()
    assert "emailAddress" in data or "displayName" in data


def test_jira_search_query(jira_config):
    """Jira JQL 搜尋應正常運作"""
    if not jira_config["configured"]:
        pytest.skip("Jira 未設定")

    resp = requests.get(
        f"{jira_config['url']}/rest/api/2/search",
        params={"jql": "project is not EMPTY", "maxResults": 1},
        auth=_auth(jira_config),
        timeout=15,
    )
    assert resp.status_code == 200, f"JQL 搜尋失敗: HTTP {resp.status_code}"
    data = resp.json()
    assert "total" in data, f"非預期的搜尋回應: {list(data.keys())}"


def test_jira_response_time(jira_config):
    """Jira API 回應時間應 < 5 秒"""
    if not jira_config["configured"]:
        pytest.skip("Jira 未設定")

    start = time.time()
    resp = requests.get(
        f"{jira_config['url']}/rest/api/2/serverInfo",
        auth=_auth(jira_config),
        timeout=10,
    )
    elapsed = time.time() - start

    assert resp.status_code == 200
    assert elapsed < 5.0, f"回應時間 {elapsed:.2f}s 超過 5 秒閾值"
