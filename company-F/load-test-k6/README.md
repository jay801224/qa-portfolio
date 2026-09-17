# k6 負載測試

## 安裝

```bash
# Windows (winget)
winget install grafana.k6

# macOS
brew install k6

# Docker
docker run --rm -i grafana/k6 run - <script.js
```

官方文件: https://k6.io/docs/get-started/installation/

## 使用方式

```bash
# HTTP API 壓測（10 VU，30 秒）
k6 run --vus 10 --duration 30s shared/k6/http_load.js

# WebSocket 壓測（5 VU，60 秒）
k6 run --vus 5 --duration 60s shared/k6/ws_load.js

# 自訂環境變數
k6 run -e BASE_URL=https://example.com -e USERNAME=<ACCOUNT> shared/k6/http_load.js

# 匯出 JSON 結果
k6 run --out json=results.json shared/k6/http_load.js
```

## 檔案說明

| 檔案 | 說明 |
|------|------|
| `http_load.js` | HTTP API 負載測試（登入 + 查餘額） |
| `ws_load.js` | WebSocket 負載測試（遊戲連線壓測） |
| `config/thresholds.json` | 通過標準配置 |

## 通過標準

| 指標 | 閾值 |
|------|------|
| P95 延遲 | < 500ms |
| 錯誤率 | < 1% |
| P99 延遲 | < 1000ms |
