"""
api_report.py — API 測試 HTML + JSON 報告產生器

用法:
    python api_report.py                    # QA 環境
    python api_report.py --env uat          # UAT 環境
    python api_report.py --output-dir ./    # 自訂輸出目錄

輸出:
    shared/report/api_test_report.html
    shared/report/api_test_report.json
"""

import os
import sys
import json
import time
import argparse
import subprocess
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPORT_DIR = os.path.join(os.path.dirname(__file__), "..", "report")


def _esc(s):
    import html as _h
    return _h.escape(str(s))


def _effort_panel():
    """report_shared.md 規範的人力預估面板"""
    return """<div class="effort-panel">
<h4 data-i18n="effort_title"></h4>
<div class="effort-row"><span data-i18n="effort_manual"></span><strong>1.5 天/次</strong></div>
<div class="effort-row"><span data-i18n="effort_auto"></span><strong>1.5 個月</strong></div>
<div class="effort-row"><span data-i18n="effort_senior"></span><strong>3 週</strong></div>
<div class="effort-row"><span data-i18n="effort_ai"></span><strong>1 天</strong></div>
</div>"""


def run_tests_and_report(env="qa", output_dir="", target_file="", export_json=False):
    """執行 pytest 並產生 HTML + JSON 報告"""
    test_dir = os.path.dirname(__file__)
    out_dir = output_dir or REPORT_DIR
    os.makedirs(out_dir, exist_ok=True)

    env_vars = os.environ.copy()
    env_vars["TEST_ENV"] = env

    # 支援指定測試檔案（如 test_stream.py），不指定則跑全部
    test_path = os.path.join(test_dir, target_file) if target_file else test_dir

    # 根據測試檔案決定報告名稱
    if target_file and "security" in target_file:
        report_name = "api_security_test_report"
        report_title_zh = "API 安全性測試報告"
        report_title_en = "API Security Test Report"
    else:
        report_name = "api_test_report"
        report_title_zh = "API 測試報告"
        report_title_en = "API Test Report"
    start_time = time.time()
    result = subprocess.run(
        [sys.executable, "-X", "utf8", "-m", "pytest", test_path, "-v", "--tb=short"],
        capture_output=True, text=True, env=env_vars,
        encoding="utf-8", errors="replace",
    )
    elapsed = time.time() - start_time
    if result.stdout is None:
        result.stdout = ""

    # 解析 pytest 輸出
    lines = result.stdout.splitlines()
    test_results = []
    for line in lines:
        if "::" not in line:
            continue
        stripped = line.strip()
        # 跳過 pytest summary 行（開頭是 FAILED/PASSED）
        if stripped.startswith("FAILED ") or stripped.startswith("PASSED "):
            continue
        if "PASSED" in line or "FAILED" in line or "SKIPPED" in line:
            parts = stripped.split(" ")
            if len(parts) < 2:
                continue
            test_path = parts[0]
            status = "PASS" if "PASSED" in line else ("FAIL" if "FAILED" in line else "SKIP")
            if "::" in test_path:
                file_name, test_name = test_path.rsplit("::", 1)
                file_name = os.path.basename(file_name)
            else:
                file_name, test_name = "", test_path
            note = ""
            if status == "FAIL":
                idx = lines.index(line)
                for sub in lines[idx+1:idx+5]:
                    if "assert" in sub.lower() or "error" in sub.lower():
                        note = sub.strip()[:120]
                        break
                if not note:
                    note = "Test failed"
            elif status == "SKIP":
                # 提取 skip 原因
                if "SKIPPED" in line:
                    skip_match = line.split("SKIPPED")[0].strip()
                    note = "Skipped"

            test_results.append({
                "file": file_name, "name": test_name,
                "status": status, "note": note,
            })

    total = len(test_results)
    passed = sum(1 for r in test_results if r["status"] == "PASS")
    failed = sum(1 for r in test_results if r["status"] == "FAIL")
    skipped = sum(1 for r in test_results if r["status"] == "SKIP")
    rate = f"{passed / max(total - skipped, 1) * 100:.0f}%"
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ── JSON 報告（需加 --json flag）──
    if export_json:
        json_report = {
            "report_type": "api_test",
            "generated_at": now_str,
            "environment": env.upper(),
            "elapsed_s": round(elapsed, 1),
            "summary": {
                "total": total, "passed": passed,
                "failed": failed, "skipped": skipped,
                "pass_rate_pct": round(passed / max(total - skipped, 1) * 100, 1),
            },
            "results": test_results,
        }
        json_path = os.path.join(out_dir, f"{report_name}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_report, f, ensure_ascii=False, indent=2)
        print(f"  JSON 報告: {json_path}")

    # ── HTML 報告 ──
    rows = ""
    for i, r in enumerate(test_results, 1):
        cls = {"PASS": "row-pass", "FAIL": "row-fail", "SKIP": "row-skip"}[r["status"]]
        rows += (f'<tr class="{cls}"><td>{i}</td><td>{_esc(r["file"])}</td>'
                 f'<td>{_esc(r["name"])}</td><td>{_esc(r["status"])}</td>'
                 f'<td>{_esc(r["note"])}</td></tr>\n')

    html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>API Test Report</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,'Segoe UI',sans-serif;background:#f0f2f5;color:#333;min-width:1200px}}
.lang-toggle{{background:#0a3d91;padding:8px 40px;display:flex;justify-content:flex-end;gap:0}}
.lang-btn{{padding:5px 14px;border:1px solid rgba(255,255,255,0.5);background:transparent;color:white;cursor:pointer;font-size:12px;transition:all 0.2s}}
.lang-btn:first-child{{border-radius:4px 0 0 4px}}.lang-btn:last-child{{border-radius:0 4px 4px 0}}
.lang-btn.active{{background:white;color:#1a237e;font-weight:bold}}
.header{{background:linear-gradient(135deg,#1a1a2e,#16213e);color:white;padding:30px 40px;display:flex;justify-content:space-between;align-items:flex-start}}
.header-main{{flex:1;min-width:0}}
.header-main h1{{font-size:24px;margin-bottom:8px}}.header-main .meta{{font-size:14px;opacity:0.85;line-height:1.8}}
.effort-panel{{min-width:220px;background:rgba(255,255,255,0.1);border-radius:8px;padding:14px 18px;margin-left:30px}}
.effort-panel h4{{font-size:13px;margin-bottom:8px;opacity:0.9}}
.effort-row{{display:flex;justify-content:space-between;font-size:12px;padding:3px 0;border-bottom:1px solid rgba(255,255,255,0.1)}}
.cards{{display:flex;gap:16px;padding:20px 40px;flex-wrap:wrap}}
.card{{flex:1;min-width:120px;padding:20px;border-radius:10px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,0.1)}}
.card .num{{font-size:32px;font-weight:bold}}.card .label{{font-size:13px;margin-top:4px;opacity:0.7}}
.card-total{{background:white;color:#1a237e}}.card-pass{{background:#e8f5e9;color:#2e7d32}}
.card-fail{{background:#ffebee;color:#c62828}}.card-skip{{background:#fff3e0;color:#e65100}}
.card-rate{{background:#fff8e1;color:#e65100}}
.section{{padding:20px 40px}}.section h2{{font-size:18px;margin-bottom:12px;color:#1a237e;border-bottom:2px solid #1a237e;padding-bottom:6px}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th{{background:#1F4E79;color:white;padding:10px 8px;text-align:left}}
td{{padding:8px;border-bottom:1px solid #e0e0e0}}
tr:hover{{background:#e3f2fd!important}}
tr.row-pass{{background:#C6EFCE}}tr.row-fail{{background:#FFC7CE}}tr.row-skip{{background:#f5f5f5;color:#999}}
pre{{background:#f5f5f5;padding:12px;border-radius:4px;font-size:12px;overflow-x:auto;white-space:pre-wrap;margin-top:20px}}
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
<span data-i18n="env"></span>: {_esc(env.upper())} |
<span data-i18n="time"></span>: {now_str} |
<span data-i18n="elapsed"></span>: {elapsed:.1f}s
</div>
</div>
{_effort_panel()}
</div>
<div class="cards">
<div class="card card-total"><div class="num">{total}</div><div class="label" data-i18n="card_total"></div></div>
<div class="card card-pass"><div class="num">{passed}</div><div class="label">PASS</div></div>
<div class="card card-fail"><div class="num">{failed}</div><div class="label">FAIL</div></div>
<div class="card card-skip"><div class="num">{skipped}</div><div class="label">SKIP</div></div>
<div class="card card-rate"><div class="num">{rate}</div><div class="label" data-i18n="card_rate"></div></div>
</div>
<div class="section"><h2 data-i18n="section_results"></h2>
<table><tr><th>#</th><th data-i18n="th_file"></th><th data-i18n="th_test"></th>
<th data-i18n="th_status"></th><th data-i18n="th_note"></th></tr>
{rows}</table></div>
<div class="section"><h2 data-i18n="section_output"></h2>
<pre>{_esc(result.stdout)}</pre></div>
<script>
const I18N={{
"zh":{{"title":"{report_title_zh}","env":"測試環境","time":"執行時間","elapsed":"耗時",
"card_total":"總測試數","card_rate":"通過率",
"section_results":"測試結果明細","section_output":"pytest 原始輸出",
"th_file":"檔案","th_test":"測試名稱","th_status":"狀態","th_note":"備註",
"effort_title":"人力預估（同等測試）","effort_manual":"手動 QA","effort_auto":"一般自動測試人員","effort_senior":"資深自動化測試人員","effort_ai":"AI 開發（Claude）"}},
"en":{{"title":"{report_title_en}","env":"Environment","time":"Time","elapsed":"Elapsed",
"card_total":"Total Tests","card_rate":"Pass Rate",
"section_results":"Test Results","section_output":"pytest Raw Output",
"th_file":"File","th_test":"Test Name","th_status":"Status","th_note":"Note",
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

    html_path = os.path.join(out_dir, f"{report_name}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  HTML 報告: {html_path}")
    return html_path


def main():
    parser = argparse.ArgumentParser(description="API 測試報告產生器")
    parser.add_argument("--env", default="qa", help="測試環境 (qa/uat)")
    parser.add_argument("--stream-env", default="staging", help="STREAM 環境 (staging/prod)")
    parser.add_argument("--target", default="", help="指定測試檔案（如 test_stream.py），不指定跑全部")
    parser.add_argument("--json", action="store_true", help="同時產生 JSON 報告")
    parser.add_argument("--output-dir", default="", help="報告輸出目錄（預設 report/）")
    args = parser.parse_args()

    # 設定 STREAM 環境變數
    os.environ["STREAM_ENV"] = args.stream_env

    run_tests_and_report(env=args.env, output_dir=args.output_dir,
                         target_file=args.target, export_json=args.json)


if __name__ == "__main__":
    main()
