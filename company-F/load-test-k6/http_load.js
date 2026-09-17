/**
 * http_load.js — HTTP API 負載測試模板
 *
 * 測試流程:
 *   1. 登入 API → 取得 game URL（含 tss token）
 *   2. 查詢餘額
 *   3. 檢查回應時間與錯誤率
 *
 * 執行:
 *   k6 run --vus 10 --duration 30s shared/k6/http_load.js
 *   k6 run -e BASE_URL=http://example.internal:2589 shared/k6/http_load.js
 */

import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// ── 自訂指標 ────────────────────────────────────────────────
const loginDuration = new Trend('login_duration', true);
const loginErrors = new Rate('login_errors');

// ── 設定 ────────────────────────────────────────────────────
const BASE_URL = __ENV.TARGET_URL || 'https://httpbin.org';
const LOGIN_ENDPOINT = `${BASE_URL}/gi/operatorSimulation/getEntryUrl`;
const USERNAME = __ENV.USERNAME || '<ACCOUNT>';

// ── 閾值（通過標準）────────────────────────────────────────
export const options = {
    // 預設: 10 VU, 30 秒（可用 CLI 覆蓋）
    vus: 10,
    duration: '30s',

    thresholds: {
        http_req_duration: ['p(95)<500', 'p(99)<1000'],
        http_req_failed: ['rate<0.01'],
        login_duration: ['p(95)<3000'],
        login_errors: ['rate<0.05'],
    },

    // Ramp-up 階段（進階模式，取消註解使用）
    // stages: [
    //     { duration: '10s', target: 5 },   // 暖機
    //     { duration: '30s', target: 20 },  // 爬坡
    //     { duration: '10s', target: 0 },   // 冷卻
    // ],
};

// ── 登入 ────────────────────────────────────────────────────
function login() {
    const payload = JSON.stringify({
        cagent: '<ACCOUNT>',
        loginname: USERNAME,
        password: '<REDACTED>',
        currency: 'CNY',
        language: '1',
        platformType: 'pc',
        gameCode: 'bac',
    });

    const params = {
        headers: { 'Content-Type': 'application/json' },
    };

    const res = http.post(LOGIN_ENDPOINT, payload, params);

    const success = check(res, {
        'login status 200': (r) => r.status === 200,
        'login has game URL': (r) => {
            try {
                const body = JSON.parse(r.body);
                const url = body.url || (body.data && body.data.url) || '';
                return url.includes('tss=');
            } catch (e) {
                return false;
            }
        },
    });

    loginDuration.add(res.timings.duration);
    loginErrors.add(!success);

    if (success) {
        try {
            const body = JSON.parse(res.body);
            return body.url || (body.data && body.data.url) || '';
        } catch (e) {
            return '';
        }
    }
    return '';
}

// ── 主測試邏輯 ────────────────────────────────────────────────
export default function () {
    // Step 1: 登入
    const gameUrl = login();

    if (gameUrl) {
        // Step 2: 訪問 game URL（模擬載入遊戲頁面）
        const pageRes = http.get(gameUrl, { timeout: '10s' });
        check(pageRes, {
            'game page status 200': (r) => r.status === 200,
        });
    }

    // 模擬使用者思考時間
    sleep(Math.random() * 2 + 1);
}
