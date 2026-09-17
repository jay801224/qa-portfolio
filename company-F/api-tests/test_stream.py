"""
test_stream.py — STREAM API 測試

支援環境:
    STREAM_ENV=staging  → example.internal（預設）
    STREAM_ENV=prod     → example.internal
不需登入即可測的公開 API。
"""

import os
import time
import pytest
import requests

STREAM_ENDPOINTS = {
    "staging": "https://example.internal/api",
    "prod": "https://example.internal/api",
}
BASE_URL = STREAM_ENDPOINTS.get(os.environ.get("STREAM_ENV", "staging"), STREAM_ENDPOINTS["staging"])
VIDEO_ID = "020a5328-4069-44bd-bc76-d8f85294123d"
TIMEOUT = 10


@pytest.fixture(scope="module")
def session():
    s = requests.Session()
    s.headers.update({"Accept": "application/json"})
    s.verify = True
    return s


# ── Videos API ──────────────────────────────────────────────

def test_videos_list(session):
    """GET /api/videos 應回傳影片清單"""
    resp = session.get(f"{BASE_URL}/videos", timeout=TIMEOUT)
    assert resp.status_code == 200, f"HTTP {resp.status_code}"
    data = resp.json()
    videos = data.get("data", {}).get("videos", data.get("data", []))
    assert isinstance(videos, list), f"預期 list，得到 {type(videos)}"
    assert len(videos) > 0, "影片清單為空"


def test_video_detail(session):
    """GET /api/videos/{id} 應回傳影片詳細資訊"""
    resp = session.get(f"{BASE_URL}/videos/{VIDEO_ID}", timeout=TIMEOUT)
    assert resp.status_code == 200, f"HTTP {resp.status_code}"
    data = resp.json()
    video = data.get("data", {}).get("video", data.get("data", {}))
    assert video, "影片資料為空"


def test_video_not_found(session):
    """GET /api/videos/{invalid_id} 應回 404"""
    resp = session.get(f"{BASE_URL}/videos/nonexistent-id-12345", timeout=TIMEOUT)
    assert resp.status_code in (404, 400), f"預期 404/400，得到 {resp.status_code}"


# ── Trending API ────────────────────────────────────────────

def test_trending(session):
    """GET /api/trending 應回傳熱門影片"""
    resp = session.get(f"{BASE_URL}/trending", timeout=TIMEOUT)
    assert resp.status_code == 200, f"HTTP {resp.status_code}"
    data = resp.json()
    assert data, "trending 回應為空"


# ── Search API ──────────────────────────────────────────────

def test_search(session):
    """GET /api/search?q=test 應回傳搜尋結果"""
    resp = session.get(f"{BASE_URL}/search", params={"q": "test"}, timeout=TIMEOUT)
    assert resp.status_code == 200, f"HTTP {resp.status_code}"
    data = resp.json()
    assert data, "search 回應為空"


def test_search_suggestions(session):
    """GET /api/search/suggestions 應回傳搜尋建議"""
    resp = session.get(f"{BASE_URL}/search/suggestions",
                       params={"q": "a"}, timeout=TIMEOUT)
    # 可能回 200 或 404（視功能是否啟用）
    assert resp.status_code in (200, 404), f"HTTP {resp.status_code}"


# ── Broadcasts API ──────────────────────────────────────────

def test_broadcasts_list(session):
    """GET /api/broadcasts 應回傳直播清單"""
    resp = session.get(f"{BASE_URL}/broadcasts", timeout=TIMEOUT)
    assert resp.status_code == 200, f"HTTP {resp.status_code}"


# ── Auth API（不登入，只驗結構）──────────────────────────────

def test_login_endpoint_exists(session):
    """POST /api/auth/login 無帳密應回 400/401（不是 404）"""
    resp = session.post(f"{BASE_URL}/auth/login",
                        json={"email": "", "password": ""},
                        timeout=TIMEOUT)
    assert resp.status_code in (400, 401, 422), \
        f"預期 400/401/422，得到 {resp.status_code}"


def test_register_endpoint_exists(session):
    """POST /api/auth/register 空資料應回 400/422（不是 404）"""
    resp = session.post(f"{BASE_URL}/auth/register",
                        json={"email": "", "password": "", "name": ""},
                        timeout=TIMEOUT)
    assert resp.status_code in (400, 401, 422), \
        f"預期 400/422，得到 {resp.status_code}"


# ── Response Time ───────────────────────────────────────────

def test_videos_response_time(session):
    """GET /api/videos 回應時間應 < 3 秒"""
    start = time.time()
    resp = session.get(f"{BASE_URL}/videos", timeout=TIMEOUT)
    elapsed = time.time() - start
    assert resp.status_code == 200
    assert elapsed < 3.0, f"回應時間 {elapsed:.2f}s 超過 3 秒"


def test_trending_response_time(session):
    """GET /api/trending 回應時間應 < 3 秒"""
    start = time.time()
    resp = session.get(f"{BASE_URL}/trending", timeout=TIMEOUT)
    elapsed = time.time() - start
    assert resp.status_code == 200
    assert elapsed < 3.0, f"回應時間 {elapsed:.2f}s 超過 3 秒"
