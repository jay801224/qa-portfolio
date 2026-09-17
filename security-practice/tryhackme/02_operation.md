# 報告二：完整操作流程

**日期**: 2026-04-15 ｜ **靶機 IP**: 10.0.0.1 ｜ **全程耗時**: 約 60 分鐘

---

## 1. 安裝套件

### 事前安裝（Plan 階段確認需要）
無。所有套件都在操作過程中按需安裝。

### 途中安裝
| 工具 | 安裝指令 | 安裝時機 | 用途 |
|------|----------|----------|------|
| OpenVPN 2.7.1 | `winget install OpenVPNTechnologies.OpenVPN` | Phase 0 — VPN 連線前 | 連接 TryHackMe 內網 |
| nmap 7.80 | `winget install Insecure.Nmap` | Phase 1 — 靶機啟動後 | 端口掃描 |
| sqlmap 1.10.3 | `pip install sqlmap` | Phase 2 — 發現 SQLi 後 | SQL Injection 自動化（最終未使用） |
| paramiko 4.0.0 | `pip install paramiko` | Phase 4 — 需要 SSH 時 | Python SSH 連線 |

## 2. 實際使用的工具

| 工具 | 用途 | 使用階段 |
|------|------|----------|
| **Playwright MCP Bridge** | TryHackMe 全程操作：VPN 下載、加入房間、啟動靶機、提交答案 | 全程 |
| **nmap** | 端口掃描（`-Pn -sT -sV`） | Phase 1 |
| **curl** | SQLi 手動測試、webshell 操控 | Phase 2-4 |
| **Python requests** | 檔案上傳（webshell） | Phase 3 |
| **paramiko** | SSH 登入靶機（mike 帳號） | Phase 4 |

## 3. 自研 SKILL — browser-setup + Playwright MCP Bridge

本次攻略的核心差異化工具。一般 CTF 需要手動操作 TryHackMe 網站，但透過自研的 browser-setup SKILL：

- AI 直接操控已登入的 Chrome 瀏覽器（jay profile）
- 自動導航至 VPN 下載頁、點擊下載
- 自動加入房間、啟動靶機、用 JavaScript 抓取目標 IP
- 自動在瀏覽器中用 SQLi payload 登入 CMS 管理後台
- 自動填寫並提交全部 5 題答案
- 全程截圖存證

**效果：整個流程從「AI 做滲透 + 人操作網站」變成「AI 全自動完成」。**

## 4. 操作流程

### Phase 0：環境建置
1. Playwright 導航至 `tryhackme.com/access`（jay profile 已登入）
2. 自動點擊 "Download Regular Configuration File" 下載 `.ovpn`
3. 偵測到 OpenVPN 未安裝 → `winget install` 自動安裝
4. 設定檔放置至 OpenVPN config 目錄，啟動 OpenVPN GUI
5. 使用者手動點擊連線（**唯一需要手動的步驟**）
6. `ping 10.0.0.1` 驗證連通（延遲 143-152ms）

### Phase 1：偵查
1. `nmap -Pn -sT -sV` → 發現 3 個 open port：22(SSH)、80(Apache)、8080(Apache)
2. curl 探索 port 80 → Apache 預設頁面
3. curl 探索 port 8080 → **Simple Image Gallery System** (by oretnom23) v1.0
4. 自動跳轉至 `/gallery/login.php`

### Phase 2：漏洞發現
1. 對 `/gallery/classes/Login.php?f=login` 測試 `admin' or 1=1-- -` → **SQLi 登入繞過成功**
2. 應用程式在 `last_qry` 欄位完整回顯 SQL 查詢：`SELECT * from users where username = '...' and password = md5('...')`
3. UNION SELECT 暴力測試 → 確認 users 表有 10 個欄位
4. Boolean Blind SQLi 確認密碼 hash 長度 = 32（MD5）
5. 逐字元提取 hash：對 `0-9a-f` 逐位測試，32 位共約 512 次 HTTP 請求，耗時約 2 分鐘
6. 取得 admin hash：`<hash>`

### Phase 3：利用
1. Playwright 在瀏覽器中以 `admin' OR 1=1-- -` 登入管理後台
2. Python requests 透過使用者頭像上傳功能上傳 PHP webshell（無檔案類型驗證）
3. webshell 位置：`/gallery/uploads/1776256260_shell.php`
4. 驗證 RCE：`whoami` → www-data

### Phase 4：提權
**www-data → mike：**
1. `/home/mike/user.txt` 權限 `-rwx------`，www-data 無法讀取
2. 發現 `initialize.php` 含 MySQL 憑證（`gallery_user` / `<practice-box-password>`）
3. 發現 `/var/backups/mike_home_backup/` — mike 家目錄備份
4. `.bash_history` 中 mike 意外洩漏密碼：`sudo -l<practice-box-password>`（密碼 = `<practice-box-password>`）
5. `accounts.txt` 也含有 mike 的多個帳密
6. webshell 執行 `echo <practice-box-password> | su -c 'cat /home/mike/user.txt' mike` → **取得 user flag**

**mike → root：**
1. `sudo -l` → mike 可 NOPASSWD 執行 `/bin/bash /opt/rootkit.sh`
2. rootkit.sh 選 `read` → 以 root 權限開啟 nano
3. 解法為 GTFOBins nano 提權：Ctrl+R → Ctrl+X → `reset; sh 1>&0 2>&0` → root shell
4. 在 root shell 中 `cat /root/root.txt` → **取得 root flag**

### Phase 5：提交答案
- Playwright MCP 自動填入 5 題答案，逐一點擊 Check
- Room progress 100%，獲得 150 points

## 5. 遇到的問題與解決方式

| # | 問題 | 解決方式 |
|---|------|----------|
| 1 | jay Chrome profile MCP 連線逾時 | 確認擴充功能已啟用後重試成功 |
| 2 | 先嘗試 fatty Chrome profile，未登入 TryHackMe | 切回 jay profile（已登入 Google） |
| 3 | VPN 設定檔下載為 `.tmp` 暫存格式 | 驗證檔案內容完整（130 行，正確結尾），重命名為 `.ovpn` |
| 4 | OpenVPN 未安裝 | `winget install` 自動安裝 |
| 5 | nmap 因缺少 Npcap 無法使用 SYN scan | 改用 TCP connect scan（`-sT`），結果相同 |
| 6 | **Q1 填 "2" 錯誤** | 重新檢查 nmap 原始輸出，確認 22/80/8080 三個都是 open，改填 "3" 正確。**AI 自行發現並修正** |
| 7 | sqlmap 啟動慢 | 改用手動 Boolean Blind SQLi，hex 字元集效率更高 |
| 8 | curl `-F @path` 在 Git Bash 路徑衝突 | 改用 Python requests 完成檔案上傳 |
| 9 | webshell session 過期 | 改用 SSH（paramiko）直連靶機，更穩定 |
| 10 | nano PTY 互動不穩定（root 提權） | Windows 環境下 paramiko + nano 互動兼容性問題，嘗試多種 PTY 方法 |
| 11 | PwnKit exploit 需 gcc，靶機未安裝 | 嘗試下載預編譯 binary，但靶機無外網；本機下載被防毒刪除 |

## 6. 重要註記

### Q1 填錯原因
nmap 掃出 22/80/8080 共 3 個 open port。AI 初次誤判為 2（排除 SSH），提交後自行檢查 nmap 輸出修正為 3。**未請求使用者協助。**

### 全自動執行
整個攻略過程中 AI **未主動請求使用者協助**。使用者的操作僅限於：
- 連線 VPN（OpenVPN GUI 需手動點擊）
- 中間的閒聊訊息（對攻略流程無影響）
