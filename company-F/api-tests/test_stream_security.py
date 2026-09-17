"""
test_stream_security.py — STREAM API 安全測試

支援環境:
    STREAM_ENV=staging  → example.internal（預設）
    STREAM_ENV=prod     → example.internal
覆蓋: SQL Injection / XSS / Path Traversal / Header Injection / Security Headers / CORS

OWASP Top 10 對應:
  A01: Broken Access Control (path traversal)
  A03: Injection (SQL / XSS / header)
  A05: Security Misconfiguration (headers / CORS)
"""

import os
import pytest
import requests

STREAM_ENDPOINTS = {
    "staging": ("https://example.internal/api", "https://example.internal"),
    "prod": ("https://example.internal/api", "https://example.internal"),
}
_env = os.environ.get("STREAM_ENV", "staging")
BASE_URL, FRONTEND_URL = STREAM_ENDPOINTS.get(_env, STREAM_ENDPOINTS["staging"])
VIDEO_ID = "020a5328-4069-44bd-bc76-d8f85294123d"
TIMEOUT = 10


@pytest.fixture(scope="module")
def session():
    s = requests.Session()
    s.headers.update({"Accept": "application/json"})
    s.verify = True
    return s


# ═══════════════════════════════════════════════════════════════
#  A03: SQL Injection
# ═══════════════════════════════════════════════════════════════

SQL_PAYLOADS = [
    ("' OR 1=1 --", "classic OR injection"),
    ("'; DROP TABLE users; --", "DROP TABLE"),
    ("1' UNION SELECT null,null,null --", "UNION SELECT"),
    ("' AND 1=CONVERT(int,(SELECT @@version)) --", "error-based"),
    ("admin'--", "comment bypass"),
]


@pytest.mark.parametrize("payload,desc", SQL_PAYLOADS, ids=[p[1] for p in SQL_PAYLOADS])
def test_sql_injection_search(session, payload, desc):
    """搜尋 API 不應受 SQL injection 影響"""
    resp = session.get(f"{BASE_URL}/search", params={"q": payload}, timeout=TIMEOUT)
    # 不能回 500（代表 SQL 語法被執行）
    assert resp.status_code != 500, \
        f"[SQL INJECTION] /search 回 500，payload: {payload}"
    # 回傳不能包含資料庫錯誤訊息
    body = resp.text.lower()
    db_errors = ["syntax error", "mysql", "postgresql", "sqlite", "unclosed quotation",
                 "sql error", "orm", "sequelize", "prisma error", "query failed"]
    for err in db_errors:
        assert err not in body, \
            f"[SQL INJECTION] 回傳含資料庫錯誤 '{err}'，payload: {payload}"


@pytest.mark.parametrize("payload,desc", SQL_PAYLOADS[:3], ids=[p[1] for p in SQL_PAYLOADS[:3]])
def test_sql_injection_video_id(session, payload, desc):
    """影片 ID 參數不應受 SQL injection 影響"""
    resp = session.get(f"{BASE_URL}/videos/{payload}", timeout=TIMEOUT)
    assert resp.status_code != 500, \
        f"[SQL INJECTION] /videos/{{id}} 回 500，payload: {payload}"


def test_sql_injection_auth_login(session):
    """登入 API 不應受 SQL injection 影響"""
    resp = session.post(f"{BASE_URL}/auth/login",
                        json={"email": "' OR 1=1 --", "password": "' OR 1=1 --"},
                        timeout=TIMEOUT)
    assert resp.status_code != 500, \
        f"[SQL INJECTION] /auth/login 回 500"
    assert resp.status_code in (400, 401, 422), \
        f"預期 400/401/422，得到 {resp.status_code}"


# ═══════════════════════════════════════════════════════════════
#  A03: XSS (Reflected / Stored via API)
# ═══════════════════════════════════════════════════════════════

XSS_PAYLOADS = [
    ("<script>alert('xss')</script>", "basic script tag"),
    ("<img src=x onerror=alert(1)>", "img onerror"),
    ("javascript:alert(1)", "javascript protocol"),
    ("<svg onload=alert(1)>", "svg onload"),
    ("'\"><script>alert(1)</script>", "quote escape + script"),
    ("<iframe src='javascript:alert(1)'>", "iframe injection"),
    ("{{constructor.constructor('alert(1)')()}}", "template injection"),
]


@pytest.mark.parametrize("payload,desc", XSS_PAYLOADS, ids=[p[1] for p in XSS_PAYLOADS])
def test_xss_search_reflected(session, payload, desc):
    """搜尋結果不應反射未 escape 的 XSS payload"""
    resp = session.get(f"{BASE_URL}/search", params={"q": payload}, timeout=TIMEOUT)
    assert resp.status_code != 500, \
        f"[XSS] /search 回 500，payload: {payload}"
    if resp.status_code == 200:
        body = resp.text
        # 回傳的 JSON 中不應包含未 escape 的 HTML 標籤
        assert f"<script>" not in body, \
            f"[XSS REFLECTED] 回傳含未 escape 的 <script>，payload: {payload}"
        assert "onerror=" not in body, \
            f"[XSS REFLECTED] 回傳含 onerror=，payload: {payload}"
        assert "<iframe" not in body.lower(), \
            f"[XSS REFLECTED] 回傳含 <iframe>，payload: {payload}"


@pytest.mark.parametrize("payload,desc", XSS_PAYLOADS[:3], ids=[p[1] for p in XSS_PAYLOADS[:3]])
def test_xss_auth_register(session, payload, desc):
    """註冊 API 不應接受含 XSS 的 username/email"""
    resp = session.post(f"{BASE_URL}/auth/register",
                        json={"name": payload, "email": f"{payload}@test.com",
                              "password": "Test1234!"},
                        timeout=TIMEOUT)
    if resp.status_code == 200:
        body = resp.text
        assert "<script>" not in body, \
            f"[XSS STORED] 註冊回傳含未 escape 的 <script>"


# ═══════════════════════════════════════════════════════════════
#  A01: Path Traversal
# ═══════════════════════════════════════════════════════════════

PATH_TRAVERSAL_PAYLOADS = [
    ("../../../etc/passwd", "unix passwd"),
    ("..\\..\\..\\windows\\system32\\config\\sam", "windows sam"),
    ("....//....//....//etc/passwd", "double dot bypass"),
    ("%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd", "url encoded"),
    ("..%252f..%252f..%252fetc%252fpasswd", "double url encoded"),
]


@pytest.mark.parametrize("payload,desc", PATH_TRAVERSAL_PAYLOADS,
                         ids=[p[1] for p in PATH_TRAVERSAL_PAYLOADS])
def test_path_traversal_video_id(session, payload, desc):
    """影片 ID 不應允許 path traversal"""
    resp = session.get(f"{BASE_URL}/videos/{payload}", timeout=TIMEOUT)
    body = resp.text.lower()
    # 不能回傳系統檔案內容
    assert "root:" not in body, \
        f"[PATH TRAVERSAL] /etc/passwd 內容洩漏，payload: {payload}"
    assert "[boot loader]" not in body, \
        f"[PATH TRAVERSAL] Windows 系統檔洩漏，payload: {payload}"
    assert resp.status_code != 500, \
        f"[PATH TRAVERSAL] 回 500，payload: {payload}"


@pytest.mark.parametrize("payload,desc", PATH_TRAVERSAL_PAYLOADS[:2],
                         ids=[p[1] for p in PATH_TRAVERSAL_PAYLOADS[:2]])
def test_path_traversal_channels(session, payload, desc):
    """頻道 ID 不應允許 path traversal"""
    resp = session.get(f"{BASE_URL}/channels/{payload}", timeout=TIMEOUT)
    assert resp.status_code != 500, \
        f"[PATH TRAVERSAL] /channels 回 500，payload: {payload}"
    assert "root:" not in resp.text.lower()


# ═══════════════════════════════════════════════════════════════
#  A03: Header Injection (CRLF / Host)
# ═══════════════════════════════════════════════════════════════

def test_crlf_injection_search(session):
    """搜尋參數不應允許 CRLF header injection"""
    payload = "test\r\nX-Injected: true\r\n"
    resp = session.get(f"{BASE_URL}/search", params={"q": payload}, timeout=TIMEOUT)
    assert "x-injected" not in resp.headers, \
        "[CRLF INJECTION] 自訂 header 被注入到回應中"


def test_host_header_injection(session):
    """Host header 篡改不應導致異常"""
    resp = session.get(f"{BASE_URL}/videos",
                       headers={"Host": "evil.com"},
                       timeout=TIMEOUT)
    # 不能回 500，也不能回含 evil.com 的回應
    assert "evil.com" not in resp.text, \
        "[HOST INJECTION] 回傳中出現被篡改的 Host"


# ═══════════════════════════════════════════════════════════════
#  A05: Security Headers（安全性 HTTP 標頭）
# ═══════════════════════════════════════════════════════════════

REQUIRED_HEADERS = [
    ("x-content-type-options", "nosniff", "防止 MIME type sniffing"),
    ("x-frame-options", None, "防止 clickjacking（DENY 或 SAMEORIGIN）"),
    ("strict-transport-security", None, "強制 HTTPS（HSTS）"),
]

RECOMMENDED_HEADERS = [
    ("content-security-policy", None, "CSP 內容安全策略"),
    ("x-xss-protection", None, "瀏覽器 XSS 過濾器（舊版瀏覽器）"),
    ("referrer-policy", None, "控制 Referer 洩漏"),
    ("permissions-policy", None, "限制瀏覽器 API 權限"),
]


@pytest.mark.parametrize("header,expected,desc", REQUIRED_HEADERS,
                         ids=[h[0] for h in REQUIRED_HEADERS])
def test_required_security_header(session, header, expected, desc):
    """必要的安全 header 應存在"""
    resp = session.get(f"{BASE_URL}/videos", timeout=TIMEOUT)
    value = resp.headers.get(header)
    assert value is not None, \
        f"[MISSING HEADER] {header} 缺失 — {desc}"
    if expected:
        assert expected.lower() in value.lower(), \
            f"[WRONG HEADER] {header}={value}，預期含 '{expected}'"


@pytest.mark.parametrize("header,expected,desc", RECOMMENDED_HEADERS,
                         ids=[h[0] for h in RECOMMENDED_HEADERS])
def test_recommended_security_header(session, header, expected, desc):
    """建議的安全 header 應存在"""
    resp = session.get(f"{BASE_URL}/videos", timeout=TIMEOUT)
    value = resp.headers.get(header)
    assert value is not None, \
        f"[MISSING HEADER] {header} 缺失 — {desc}"


# ═══════════════════════════════════════════════════════════════
#  A05: CORS 配置驗證
# ═══════════════════════════════════════════════════════════════

def test_cors_no_wildcard(session):
    """CORS 不應允許任意 origin（Access-Control-Allow-Origin: *）"""
    resp = session.options(f"{BASE_URL}/videos",
                           headers={"Origin": "https://evil.com",
                                    "Access-Control-Request-Method": "GET"},
                           timeout=TIMEOUT)
    acao = resp.headers.get("access-control-allow-origin", "")
    assert acao != "*", \
        "[CORS] Access-Control-Allow-Origin 設為 *，允許任意跨域存取"


def test_cors_reject_unknown_origin(session):
    """CORS 不應接受未知的 origin"""
    resp = session.get(f"{BASE_URL}/videos",
                       headers={"Origin": "https://evil-site.com"},
                       timeout=TIMEOUT)
    acao = resp.headers.get("access-control-allow-origin", "")
    if acao:
        assert "evil-site.com" not in acao, \
            f"[CORS] 未知 origin 'evil-site.com' 被接受: {acao}"


def test_cors_allow_legitimate_origin(session):
    """CORS 應接受合法的前端 origin"""
    resp = session.get(f"{BASE_URL}/videos",
                       headers={"Origin": FRONTEND_URL},
                       timeout=TIMEOUT)
    acao = resp.headers.get("access-control-allow-origin", "")
    # 合法 origin 應被接受（或不設 CORS = 同源不需要）
    if acao:
        assert FRONTEND_URL in acao or acao == "*", \
            f"[CORS] 合法 origin 被拒絕: {acao}"


# ═══════════════════════════════════════════════════════════════
#  額外: 大量 / 異常輸入
# ═══════════════════════════════════════════════════════════════

def test_oversized_input_search(session):
    """超長搜尋字串不應導致 500"""
    payload = "A" * 10000
    resp = session.get(f"{BASE_URL}/search", params={"q": payload}, timeout=TIMEOUT)
    assert resp.status_code != 500, \
        f"[OVERSIZED INPUT] 10000 字元搜尋導致 500"


def test_null_byte_injection(session):
    """Null byte 不應導致異常"""
    resp = session.get(f"{BASE_URL}/videos/\x00{VIDEO_ID}", timeout=TIMEOUT)
    assert resp.status_code != 500, \
        "[NULL BYTE] null byte 導致 500"


def test_special_chars_search(session):
    """特殊字元搜尋不應導致 500"""
    special = "!@#$%^&*(){}[]|\\:\";<>?/~`"
    resp = session.get(f"{BASE_URL}/search", params={"q": special}, timeout=TIMEOUT)
    assert resp.status_code != 500, \
        f"[SPECIAL CHARS] 特殊字元搜尋導致 500"
