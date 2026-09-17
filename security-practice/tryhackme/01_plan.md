# 報告一：事前 Plan

**考題**: 使用 AI 工具搭配提示詞，取得 TryHackMe 靶機 Gallery666 的 user flag，過程全自動（AI 不請求指示）
**日期**: 2026-04-15

---

## 1. 考題分析

- 目標：取得靶機的 user flag（加分：root flag）
- 限制：全自動，AI 不得請求使用者指示
- 交付：操作過程報告

## 2. 攻略計畫

| Phase | 目標 | 方法 |
|-------|------|------|
| 0 | 環境建置 | 下載 VPN 設定、安裝必要工具、連線靶機網路 |
| 1 | 偵查 | nmap 端口掃描、Web 服務識別 |
| 2 | 漏洞發現 | SQL Injection 測試、CMS 已知漏洞 |
| 3 | 利用 | SQLi 提取密碼 hash、上傳 webshell 取得 RCE |
| 4 | 提權 | www-data → mike → root |
| 5 | 提交 | 自動填入答案至 TryHackMe 網站 |

## 3. 策略選擇

| 方案 | 決定 | 原因 |
|------|:----:|------|
| 本機 OpenVPN 直連 | **採用** | 最穩定、最簡單 |
| Docker 內跑 VPN | 排除 | 需額外 NET_ADMIN 權限，增加 debug 成本 |
| TryHackMe AttackBox | 排除 | 免費帳戶有時間限制，本機工具更靈活 |
| 使用現有 qa-security-audit SKILL | 排除 | 設計用於 Web 被動掃描，不適用 CTF 進攻式滲透 |

## 4. 預計使用的工具

### 需安裝
| 工具 | 用途 |
|------|------|
| OpenVPN | TryHackMe 專用 VPN 連線 |
| nmap | 端口掃描、服務偵測 |
| sqlmap | SQL Injection 自動化（備用） |

### 自研 SKILL / 基礎設施
| 名稱 | 說明 |
|------|------|
| **browser-setup SKILL** | Playwright MCP Bridge 設定助手 — 管理多 Chrome Profile 的 MCP 連線，讓 AI 可直接操控已登入的瀏覽器 |
| **Playwright MCP Bridge** | Chrome 擴充功能，AI 可執行導航、截圖、表單填寫、點擊 |
| **qa-security-audit SKILL** | 10 項安全掃描整合（列入計畫但最終未使用） |

### 既有環境
- Python 3.10、curl、Git Bash、pip、winget
- Chrome（jay profile，已登入 Google）
