/**
 * ws_load.js — WebSocket 負載測試模板
 *
 * 測試流程:
 *   1. 建立 WebSocket 連線
 *   2. 發送 init / join room 訊息
 *   3. 接收遊戲事件
 *   4. 模擬下注操作
 *
 * 執行:
 *   k6 run --vus 5 --duration 60s shared/k6/ws_load.js
 *   k6 run -e WS_URL=wss://example.com/ws shared/k6/ws_load.js
 */

import ws from 'k6/ws';
import { check, sleep } from 'k6';
import { Rate, Counter, Trend } from 'k6/metrics';

// ── 自訂指標 ────────────────────────────────────────────────
const wsConnectDuration = new Trend('ws_connect_duration', true);
const wsErrors = new Rate('ws_errors');
const wsMessages = new Counter('ws_messages_received');

// ── 設定 ────────────────────────────────────────────────────
const WS_URL = __ENV.WS_URL || 'wss://example.com/ws';
const ROOM_ID = __ENV.ROOM_ID || 'N006';

// ── 閾值 ────────────────────────────────────────────────────
export const options = {
    vus: 5,
    duration: '60s',

    thresholds: {
        ws_connect_duration: ['p(95)<500'],
        ws_errors: ['rate<0.05'],
        ws_messages_received: ['count>0'],
    },
};

// ── 主測試邏輯 ────────────────────────────────────────────────
export default function () {
    const startTime = Date.now();

    const res = ws.connect(WS_URL, {}, function (socket) {
        const connectTime = Date.now() - startTime;
        wsConnectDuration.add(connectTime);

        socket.on('open', function () {
            // 發送加入房間訊息
            // 格式依實際 WebSocket 協議調整
            socket.send(JSON.stringify({
                action: 'join',
                room: ROOM_ID,
            }));
        });

        socket.on('message', function (data) {
            wsMessages.add(1);

            try {
                const msg = JSON.parse(data);

                // 收到遊戲狀態更新 → 模擬下注
                if (msg.type === 'gameState' || msg.action === 'countdown') {
                    // 模擬下注
                    socket.send(JSON.stringify({
                        action: 'bet',
                        room: ROOM_ID,
                        betType: 'banker',
                        amount: 100,
                    }));
                }
            } catch (e) {
                // 非 JSON 訊息，忽略
            }
        });

        socket.on('error', function (e) {
            wsErrors.add(true);
        });

        socket.on('close', function () {
            // 連線關閉
        });

        // 維持連線一段時間後關閉
        socket.setTimeout(function () {
            socket.close();
        }, 10000 + Math.random() * 5000);
    });

    const connected = check(res, {
        'WebSocket connected': (r) => r && r.status === 101,
    });

    if (!connected) {
        wsErrors.add(true);
    }

    sleep(Math.random() * 3 + 2);
}
