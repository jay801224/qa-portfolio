"""
k6_report.py — k6 負載測試 HTML + JSON 報告產生器

用法:
    # 先跑 k6 匯出 JSON，再產報告
    k6 run --summary-export result.json script.js
    python k6_report.py --json result.json

    # 或一步到位：跑 k6 + 自動產報告
    python k6_report.py --run shared/k6/http_load.js --vus 2 --duration 10s -e BASE_URL=https://example.com

輸出:
    shared/report/k6_load_test_report.html
    shared/report/k6_load_test_report.json
"""

import os
import sys
import json
import argparse
import subprocess
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPORT_DIR = os.path.join(os.path.dirname(__file__), "..", "report")


def _esc(s):
    import html as _h
    return _h.escape(str(s))


def _score_color(value, good, warn):
    if value <= good:
        return "#2e7d32"
    if value <= warn:
        return "#e65100"
    return "#c62828"


def _effort_panel():
    """report_shared.md 規範的人力預估面板"""
    return """<div class="effort-panel">
<h4 data-i18n="effort_title"></h4>
<div class="effort-row"><span data-i18n="effort_manual"></span><strong>1.5 天/次</strong></div>
<div class="effort-row"><span data-i18n="effort_auto"></span><strong>1.5 個月</strong></div>
<div class="effort-row"><span data-i18n="effort_senior"></span><strong>3 週</strong></div>
<div class="effort-row"><span data-i18n="effort_ai"></span><strong>1 天</strong></div>
</div>"""


def generate_report(data, output_dir, target_url="", export_json=False):
    """從 k6 JSON summary 產生 HTML 報告（加 --json 產 JSON）"""
    os.makedirs(output_dir, exist_ok=True)
    metrics = data.get("metrics", {})
    checks_raw = data.get("root_group", {}).get("checks", {})

    duration = metrics.get("http_req_duration", {})
    reqs = metrics.get("http_reqs", {})
    failed = metrics.get("http_req_failed", {})
    checks_meta = metrics.get("checks", {})
    vus = metrics.get("vus", {})
    data_recv = metrics.get("data_received", {})

    p95 = duration.get("p(95)", 0)
    avg_ms = duration.get("avg", 0)
    total_reqs = reqs.get("count", 0)
    error_rate = failed.get("value", 0) * 100
    check_pass = int(checks_meta.get("passes", 0))
    check_fail = int(checks_meta.get("fails", 0))
    check_total = check_pass + check_fail
    pass_rate = (check_pass / max(check_total, 1)) * 100
    vu_count = vus.get("max", 0)
    total_data_kb = data_recv.get("count", 0) / 1024
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ── JSON 報告（需加 --json flag）──
    if export_json:
        json_report = {
            "report_type": "k6_load_test",
            "generated_at": now_str,
            "target_url": target_url,
            "summary": {
                "vus": vu_count, "total_requests": total_reqs,
                "p95_ms": round(p95, 1), "avg_ms": round(avg_ms, 1),
                "error_rate_pct": round(error_rate, 2),
                "checks_pass": check_pass, "checks_fail": check_fail,
                "pass_rate_pct": round(pass_rate, 1),
            },
            "checks": [],
            "latency": {},
        }
        for name, info in checks_raw.items():
            json_report["checks"].append({
                "name": name, "passes": info.get("passes", 0),
                "fails": info.get("fails", 0),
            })
        for key in ("http_req_duration", "http_req_waiting", "http_req_connecting",
                    "http_req_tls_handshaking", "http_req_blocked"):
            m = metrics.get(key, {})
            if m:
                json_report["latency"][key] = {
                    k: round(v, 2) for k, v in m.items()
                    if k in ("avg", "min", "med", "max", "p(90)", "p(95)")
                }
        json_path = os.path.join(output_dir, "k6_load_test_report.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_report, f, ensure_ascii=False, indent=2)
        print(f"  JSON 報告: {json_path}")

    # ── HTML 報告 ──
    check_rows = ""
    for i, (name, info) in enumerate(checks_raw.items(), 1):
        p, fl = info.get("passes", 0), info.get("fails", 0)
        cls = "row-pass" if fl == 0 else "row-fail"
        r = f"{p/max(p+fl,1)*100:.0f}%"
        check_rows += (f'<tr class="{cls}"><td>{i}</td><td>{_esc(name)}</td>'
                       f'<td>{p}</td><td>{fl}</td><td>{r}</td>'
                       f'<td>{"PASS" if fl==0 else "FAIL"}</td></tr>\n')

    latency_keys = [
        ("http_req_duration", "HTTP Request Duration"),
        ("http_req_waiting", "Waiting (TTFB)"),
        ("http_req_connecting", "Connecting"),
        ("http_req_tls_handshaking", "TLS Handshake"),
        ("http_req_sending", "Sending"),
        ("http_req_receiving", "Receiving"),
        ("http_req_blocked", "Blocked"),
    ]
    latency_rows = ""
    for key, label in latency_keys:
        m = metrics.get(key, {})
        if not m:
            continue
        latency_rows += (f'<tr><td>{label}</td>'
                         f'<td>{m.get("avg",0):.1f}</td><td>{m.get("min",0):.1f}</td>'
                         f'<td>{m.get("med",0):.1f}</td><td>{m.get("max",0):.1f}</td>'
                         f'<td>{m.get("p(90)",0):.1f}</td><td>{m.get("p(95)",0):.1f}</td></tr>\n')

    p95_c = _score_color(p95, 500, 1000)
    err_c = _score_color(error_rate, 1, 5)
    rate_c = _score_color(100 - pass_rate, 1, 5)

    html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>k6 Load Test Report</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,'Segoe UI',sans-serif;background:#f0f2f5;color:#333;min-width:1200px}}
.lang-toggle{{background:#0a3d91;padding:8px 40px;display:flex;justify-content:flex-end;gap:0}}
.lang-btn{{padding:5px 14px;border:1px solid rgba(255,255,255,0.5);background:transparent;color:white;cursor:pointer;font-size:12px;transition:all 0.2s}}
.lang-btn:first-child{{border-radius:4px 0 0 4px}}.lang-btn:last-child{{border-radius:0 4px 4px 0}}
.lang-btn.active{{background:white;color:#1a237e;font-weight:bold}}
.header{{background:linear-gradient(135deg,#1a1a2e,#16213e);color:white;padding:30px 40px;display:flex;justify-content:space-between;align-items:flex-start}}
.header-main{{flex:1;min-width:0}}
.header-main h1{{font-size:24px;margin-bottom:8px}}.header-main .meta{{font-size:14px;opacity:0.85;line-height:1.8;word-break:break-all}}
.effort-panel{{min-width:220px;background:rgba(255,255,255,0.1);border-radius:8px;padding:14px 18px;margin-left:30px}}
.effort-panel h4{{font-size:13px;margin-bottom:8px;opacity:0.9}}
.effort-row{{display:flex;justify-content:space-between;font-size:12px;padding:3px 0;border-bottom:1px solid rgba(255,255,255,0.1)}}
.cards{{display:flex;gap:16px;padding:20px 40px;flex-wrap:wrap}}
.card{{flex:1;min-width:120px;padding:20px;border-radius:10px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,0.1);background:white}}
.card .num{{font-size:28px;font-weight:bold}}.card .label{{font-size:13px;margin-top:4px;opacity:0.7}}
.section{{padding:20px 40px}}.section h2{{font-size:18px;margin-bottom:12px;color:#1a237e;border-bottom:2px solid #1a237e;padding-bottom:6px}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th{{background:#1F4E79;color:white;padding:10px 8px;text-align:left}}
td{{padding:8px;border-bottom:1px solid #e0e0e0}}
tr:hover{{background:#e3f2fd!important}}
tr.row-pass{{background:#C6EFCE}}tr.row-fail{{background:#FFC7CE}}
</style>
</head>
<body>
<div class="lang-toggle">
<button class="lang-btn active" onclick="switchLang('zh')">中文</button>
<button class="lang-btn" onclick="switchLang('en')">EN</button>
</div>
<div class="header">
<div class="header-main">
<h1 data-i18n="title"></h1>
<div class="meta">
<span data-i18n="target"></span>: {_esc(target_url or 'N/A')} |
<span data-i18n="time"></span>: {now_str} |
VUs: {vu_count} |
<span data-i18n="total_reqs"></span>: {total_reqs}
</div>
</div>
{_effort_panel()}
</div>
<div class="cards">
<div class="card"><div class="num" style="color:{p95_c}">{p95:.0f}ms</div><div class="label" data-i18n="card_p95"></div></div>
<div class="card"><div class="num" style="color:#333">{avg_ms:.0f}ms</div><div class="label" data-i18n="card_avg"></div></div>
<div class="card"><div class="num" style="color:{err_c}">{error_rate:.1f}%</div><div class="label" data-i18n="card_error"></div></div>
<div class="card"><div class="num" style="color:{rate_c}">{pass_rate:.0f}%</div><div class="label" data-i18n="card_checks"></div></div>
<div class="card"><div class="num" style="color:#333">{total_data_kb:.0f}KB</div><div class="label" data-i18n="card_data"></div></div>
</div>
<div class="section"><h2 data-i18n="section_checks"></h2>
<table><tr><th>#</th><th data-i18n="th_check"></th><th data-i18n="th_pass"></th>
<th data-i18n="th_fail"></th><th data-i18n="th_rate"></th><th data-i18n="th_status"></th></tr>
{check_rows}</table></div>
<div class="section"><h2 data-i18n="section_latency"></h2>
<table><tr><th data-i18n="th_metric"></th><th>Avg(ms)</th><th>Min</th><th>Med</th><th>Max</th><th>P90</th><th>P95</th></tr>
{latency_rows}</table></div>
<script>
const I18N={{
"zh":{{"title":"k6 負載測試報告","target":"測試目標","time":"執行時間","total_reqs":"總請求數",
"card_p95":"P95 延遲","card_avg":"平均延遲","card_error":"錯誤率","card_checks":"Checks 通過率","card_data":"接收資料",
"section_checks":"Checks 明細","section_latency":"延遲分佈",
"th_check":"檢查項","th_pass":"通過","th_fail":"失敗","th_rate":"通過率","th_status":"狀態","th_metric":"指標",
"effort_title":"人力預估（同等測試）","effort_manual":"手動 QA","effort_auto":"一般自動測試人員","effort_senior":"資深自動化測試人員","effort_ai":"AI 開發（Claude）"}},
"en":{{"title":"k6 Load Test Report","target":"Target","time":"Time","total_reqs":"Total Requests",
"card_p95":"P95 Latency","card_avg":"Avg Latency","card_error":"Error Rate","card_checks":"Checks Pass Rate","card_data":"Data Received",
"section_checks":"Checks Detail","section_latency":"Latency Distribution",
"th_check":"Check","th_pass":"Pass","th_fail":"Fail","th_rate":"Rate","th_status":"Status","th_metric":"Metric",
"effort_title":"Effort Estimate","effort_manual":"Manual QA","effort_auto":"Automation Tester","effort_senior":"Senior Automation","effort_ai":"AI Dev (Claude)"}}
}};
let currentLang=localStorage.getItem('report_lang')||'zh';
function switchLang(lang){{
currentLang=lang;localStorage.setItem('report_lang',lang);
const t=I18N[lang];
document.querySelectorAll('[data-i18n]').forEach(el=>{{const k=el.getAttribute('data-i18n');if(t[k]!==undefined)el.textContent=t[k];}});
document.querySelectorAll('.lang-btn').forEach(btn=>{{btn.classList.toggle('active',btn.textContent.trim()===(lang==='zh'?'中文':'EN'));}});
}}
switchLang(currentLang);
</script>
</body></html>"""

    html_path = os.path.join(output_dir, "k6_load_test_report.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  HTML 報告: {html_path}")
    return html_path


def main():
    parser = argparse.ArgumentParser(description="k6 負載測試報告產生器")
    parser.add_argument("--json", help="k6 JSON summary 檔案路徑")
    parser.add_argument("--run", help="直接執行 k6 腳本並產報告")
    parser.add_argument("--vus", type=int, default=2, help="VU 數量（預設 2）")
    parser.add_argument("--duration", default="10s", help="測試時間（預設 10s）")
    parser.add_argument("-e", action="append", default=[], help="環境變數（可多個）")
    parser.add_argument("--export-json", action="store_true", help="同時產生 JSON 報告")
    parser.add_argument("--output-dir", default="", help="報告輸出目錄（預設 report/）")
    parser.add_argument("--k6-path", default="k6", help="k6 執行檔路徑")
    args = parser.parse_args()

    target_url = ""
    for env in args.e:
        if env.startswith("BASE_URL="):
            target_url = env.split("=", 1)[1]

    if args.run:
        json_path = "k6_result.json"
        cmd = [args.k6_path, "run",
               "--vus", str(args.vus), "--duration", args.duration,
               "--summary-export", json_path, "--no-usage-report"]
        for env in args.e:
            cmd.extend(["-e", env])
        cmd.append(args.run)
        print(f"  執行 k6: {' '.join(cmd)}")
        subprocess.run(cmd, capture_output=False)
        if not os.path.isfile(json_path):
            print("  k6 未產生 JSON，中止")
            return
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    elif args.json:
        with open(args.json, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        parser.print_help()
        return

    out_dir = args.output_dir or REPORT_DIR
    generate_report(data, out_dir, target_url=target_url, export_json=args.export_json)


if __name__ == "__main__":
    main()
