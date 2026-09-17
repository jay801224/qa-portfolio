"""
test_login.py — 登入 API 測試

驗證:
    - API 端點可達
    - 回傳含 tss= 的 game URL
    - 回應時間 < 5 秒
"""

import time
import pytest


LOGIN_PARAMS = {
    "cagent": "<ACCOUNT>",
    "loginname": "<ACCOUNT>",
    "password": "1234",
    "currency": "CNY",
    "language": "1",
    "platformType": "pc",
    "gameCode": "bac",
}


def test_login_api_reachable(api_session, login_endpoints, env):
    """登入 API 端點應可連線"""
    url = login_endpoints.get(env)
    if not url:
        pytest.skip(f"未設定 {env} 環境的登入端點")

    resp = api_session.post(url, json=LOGIN_PARAMS, timeout=10)
    assert resp.status_code == 200, f"HTTP {resp.status_code}: {resp.text[:200]}"


def test_login_returns_game_url(api_session, login_endpoints, env):
    """登入應回傳含 tss= 的 game URL"""
    url = login_endpoints.get(env)
    if not url:
        pytest.skip(f"未設定 {env} 環境的登入端點")

    resp = api_session.post(url, json=LOGIN_PARAMS, timeout=10)
    assert resp.status_code == 200

    data = resp.json()
    game_url = data.get("url", "") or data.get("data", {}).get("url", "")

    assert game_url, f"回應中缺少 game URL: {list(data.keys())}"
    assert "tss=" in game_url, f"game URL 缺少 tss= token: {game_url[:100]}"


def test_login_response_time(api_session, login_endpoints, env):
    """登入 API 回應時間應 < 5 秒"""
    url = login_endpoints.get(env)
    if not url:
        pytest.skip(f"未設定 {env} 環境的登入端點")

    start = time.time()
    resp = api_session.post(url, json=LOGIN_PARAMS, timeout=10)
    elapsed = time.time() - start

    assert resp.status_code == 200
    assert elapsed < 5.0, f"回應時間 {elapsed:.2f}s 超過 5 秒閾值"


def test_login_invalid_credentials(api_session, login_endpoints, env):
    """無效帳密不應回傳有效 game URL"""
    url = login_endpoints.get(env)
    if not url:
        pytest.skip(f"未設定 {env} 環境的登入端點")

    bad_params = {**LOGIN_PARAMS, "loginname": "nonexistent_user_12345"}
    resp = api_session.post(url, json=bad_params, timeout=10)

    # 可能回 200 帶錯誤訊息，或回 4xx
    if resp.status_code == 200:
        data = resp.json()
        game_url = data.get("url", "") or data.get("data", {}).get("url", "")
        assert not game_url or "tss=" not in game_url, \
            "無效帳密不應回傳含 tss= 的 URL"
