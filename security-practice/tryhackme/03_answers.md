# 報告三：五題答案

**Room**: Gallery (gallery666) ｜ **Progress**: 100% ｜ **Points**: 150

---

## Task 1: Deploy and get a Shell

### Q1: How many ports are open?
**答案**: `3`

**解法**: nmap TCP connect scan（`-Pn -sT -sV`）

| Port | Service | Version |
|------|---------|---------|
| 22/tcp | SSH | OpenSSH 8.2p1 Ubuntu |
| 80/tcp | HTTP | Apache 2.4.41 — 預設頁面 |
| 8080/tcp | HTTP | Apache 2.4.41 — CMS 應用程式 |

**備註**: 初次填 "2" 錯誤（排除 SSH），檢查 nmap 輸出後自行修正為 "3"。

---

### Q2: What's the name of the CMS?
**答案**: `Simple Image Gallery`

**解法**: curl 探索 port 8080，HTML title 和頁尾顯示 CMS 名稱及版本 v1.0（by oretnom23）。

---

### Q3: What's the hash password of the admin user?
**答案**: `<hash>`

**解法**: Boolean-based Blind SQL Injection

1. 確認登入端點存在 SQLi（經典的 OR 真值繞過）
2. 應用程式在 JSON 回應的 last_qry 欄位洩漏完整 SQL 查詢
3. 確認密碼 hash 長度 = 32（MD5 格式）
4. 使用 SUBSTRING 函數逐字元提取，hex 字元集（0-9a-f）每位最多 16 次嘗試
5. 32 字元共約 512 次 HTTP 請求，耗時約 2 分鐘

---

### Q4: What's the user flag?
**答案**: `THM{<redacted>}`

**解法**:

1. SQLi 繞過登入進入 CMS 管理後台
2. 利用使用者頭像上傳功能上傳 PHP webshell（CMS 無檔案類型驗證）
3. 取得 www-data 身份的遠端指令執行（RCE）
4. 發現 /var/backups/mike_home_backup/.bash_history 含密碼洩漏
5. 以 mike 身份讀取 /home/mike/user.txt

---

## Task 2: Escalate to the root user

### Q5: What's the root flag?
**答案**: `THM{<redacted>}`

**解法**: sudo nano 提權（GTFOBins）

1. mike 可以 NOPASSWD 執行 sudo /bin/bash /opt/rootkit.sh
2. rootkit.sh 的 read 選項以 root 權限開啟 nano
3. GTFOBins nano 提權：Ctrl+R, Ctrl+X, 執行 shell 命令取得 root shell
4. 讀取 /root/root.txt

---

## 攻擊鏈

```
nmap 掃描 → 8080/HTTP (Simple Image Gallery CMS v1.0)
  → SQL Injection 登入繞過 → Blind SQLi 提取 admin hash
    → 管理後台 → 頭像上傳 webshell → RCE (www-data)
      → /var/backups/ 備份檔案 → mike 密碼
        → su mike → user.txt
          → sudo rootkit.sh → nano as root → GTFOBins
            → root.txt
```

## 截圖清單

| 檔案 | 說明 |
|------|------|
| thm_access_page.png | VPN Access 頁面 |
| thm_gallery_room.png | Gallery 房間頁面 |
| thm_gallery_joined.png | 加入房間後 |
| thm_machine_starting.png | 靶機啟動中 |
| thm_machine_ip.png | 靶機 IP 顯示 |
| thm_gallery_login.png | CMS 前端 |
| thm_gallery_admin_login.png | 管理後台登入頁 |
| thm_gallery_admin_panel.png | 管理後台（SQLi 繞過後） |
| thm_q1_correct.png | Q1 正確 |
| thm_q2_answer.png | Q2 正確 |
| thm_all_answers.png | Task 1 四題全對 (80%) |
| thm_task2.png | Task 2 頁面 |
| thm_room_completed.png | Room 100% 完成 |
