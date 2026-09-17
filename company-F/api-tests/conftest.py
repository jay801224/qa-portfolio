"""
conftest.py — pytest fixtures for API tests

提供 base_url、auth headers、session 等共用 fixtures。
"""

import os
import sys
from pathlib import Path
import pytest
import requests

# 確保可以 import 專案模組
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "react", "python"))


@pytest.fixture(scope="session")
def env():
    """測試環境（qa / uat），從環境變數或預設 qa"""
    return os.environ.get("TEST_ENV", "qa")


@pytest.fixture(scope="session")
def api_session():
    """共用 requests Session（含預設 headers）"""
    s = requests.Session()
    s.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json",
    })
    s.verify = False
    return s


@pytest.fixture(scope="session")
def login_endpoints():
    """登入 API 端點對照表"""
    return {
        "qa": "http://example.internal:2589/gi/operatorSimulation/getEntryUrl",
        "uat": "https://example.internal/operatorSimulation/getEntryUrl",
    }


@pytest.fixture(scope="session")
def jira_config():
    """Jira 連線設定（從 .env 讀取）"""
    try:
        from dotenv import load_dotenv
        load_dotenv(Path(__file__).parent.parent / ".env")
    except ImportError:
        pass

    url = os.environ.get("JIRA_URL", "")
    email = os.environ.get("JIRA_EMAIL", "")
    token = os.environ.get("JIRA_API_TOKEN", "")

    return {
        "url": url.rstrip("/"),
        "email": email,
        "token": token,
        "configured": bool(url and email and token),
    }
