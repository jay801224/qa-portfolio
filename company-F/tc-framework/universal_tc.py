"""
universal_tc.py — 通用測試案例（絕對異常類）
適用任何網站，測試失敗 = BUG，不依賴特定需求規格。

TC_0035 ~ TC_0075（41 個通用 TC）
對應範本：universal_tc_templates.md (TC_001 ~ TC_116)

用法:
    python tests/universal_tc.py --url https://www.youtube.com
    python tests/universal_tc.py --url https://www.amazon.com --headed
    python tests/universal_tc.py --url https://www.github.com --xlsx results.xlsx
"""

import argparse
import os
import sys
import time
from datetime import datetime
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

# ---------------------------------------------------------------------------
# 全域設定
# ---------------------------------------------------------------------------
SCREENSHOTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

results = []
BASE_URL = ""
DOMAIN = ""


def log(msg):
    print(msg)


def ts():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def shot_path(tid, label="fail"):
    return os.path.join(SCREENSHOTS_DIR, f"testcase{tid}_{label}_{ts()}.png")


def ok(tid, cat, name, note=""):
    log(f"  [{tid}] PASS — {note}")
    results.append({"id": tid, "cat": cat, "name": name,
                     "status": "PASS", "note": note[:200], "path": ""})


def ng(tid, cat, name, err, page=None):
    note = str(err)[:200]
    path = ""
    if page:
        try:
            path = shot_path(tid)
            page.screenshot(path=path, timeout=8000, animations="disabled")
        except Exception:
            path = ""
    log(f"  [{tid}] FAIL — {note}")
    results.append({"id": tid, "cat": cat, "name": name,
                     "status": "FAIL", "note": note, "path": path})


def new_page(browser):
    ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = ctx.new_page()
    return ctx, page


# ===========================================================================
# 一、頁面載入 (TC_001 ~ TC_004)
# ===========================================================================

def tc0035_page_not_blank(browser):
    tid, cat, name = "TC_0035", "Page Load", "頁面載入不白屏"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        length = page.evaluate("() => document.body.innerHTML.length")
        assert length > 100, f"body innerHTML too short: {length}"
        ok(tid, cat, name, f"body.innerHTML.length={length}")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0036_page_title_not_empty(browser):
    tid, cat, name = "TC_0036", "Page Load", "頁面標題非空"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        title = page.title()
        assert title and len(title.strip()) > 0, f"Title is empty"
        ok(tid, cat, name, f"title='{title[:60]}'")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0037_page_load_time(browser):
    tid, cat, name = "TC_0037", "Performance", "頁面載入時間合理"
    ctx, page = new_page(browser)
    try:
        t0 = time.time()
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        elapsed = time.time() - t0
        assert elapsed < 30, f"Load too slow: {elapsed:.1f}s"
        ok(tid, cat, name, f"wall={elapsed:.2f}s")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0038_http_status_ok(browser):
    tid, cat, name = "TC_0038", "Page Load", "HTTP 狀態碼非 4xx/5xx"
    ctx, page = new_page(browser)
    try:
        resp = page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        status = resp.status if resp else 0
        assert status < 400, f"HTTP {status}"
        ok(tid, cat, name, f"HTTP {status}")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


# ===========================================================================
# 二、圖片完整性 (TC_010 ~ TC_013)
# ===========================================================================

def tc0039_images_not_broken(browser):
    tid, cat, name = "TC_0039", "Image UI", "圖片不 broken"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        page.wait_for_timeout(3000)
        info = page.evaluate("""() => {
            const imgs = [...document.querySelectorAll('img')];
            const visible = imgs.filter(i => i.offsetWidth > 0);
            const loaded = visible.filter(i => i.naturalWidth > 0);
            return {total: imgs.length, visible: visible.length, loaded: loaded.length};
        }""")
        if info["visible"] > 0:
            ratio = info["loaded"] / info["visible"]
            assert ratio >= 0.75, f"Only {info['loaded']}/{info['visible']} loaded ({ratio:.0%})"
        ok(tid, cat, name, f"total={info['total']} visible={info['visible']} loaded={info['loaded']}")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0040_images_have_alt(browser):
    tid, cat, name = "TC_0040", "Image UI", "圖片有 alt 屬性"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        info = page.evaluate("""() => {
            const imgs = [...document.querySelectorAll('img')];
            const with_alt = imgs.filter(i => i.hasAttribute('alt'));
            return {total: imgs.length, with_alt: with_alt.length};
        }""")
        if info["total"] > 0:
            ratio = info["with_alt"] / info["total"]
            assert ratio >= 0.5, f"Only {info['with_alt']}/{info['total']} have alt ({ratio:.0%})"
        ok(tid, cat, name, f"total={info['total']} with_alt={info['with_alt']}")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0041_images_src_not_empty(browser):
    tid, cat, name = "TC_0041", "Image UI", "圖片 src 非空"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        empty_src = page.evaluate("""() => {
            const imgs = [...document.querySelectorAll('img')];
            return imgs.filter(i => !i.src || i.src === 'about:blank').length;
        }""")
        assert empty_src == 0, f"{empty_src} images have empty src"
        ok(tid, cat, name, f"All img src non-empty")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0042_svg_icons_loaded(browser):
    tid, cat, name = "TC_0042", "Image UI", "SVG 圖示載入正常"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        svg_count = page.evaluate("() => document.querySelectorAll('svg').length")
        ok(tid, cat, name, f"svg_count={svg_count}")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


# ===========================================================================
# 三、連結完整性 (TC_020 ~ TC_022)
# ===========================================================================

def tc0043_links_href_not_empty(browser):
    tid, cat, name = "TC_0043", "Interaction", "連結 href 非空"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        info = page.evaluate("""() => {
            const links = [...document.querySelectorAll('a')];
            const visible = links.filter(a => a.offsetWidth > 0);
            const bad = visible.filter(a => {
                const h = a.getAttribute('href');
                return !h || h === '#' || h === 'javascript:void(0)';
            });
            return {total: visible.length, bad: bad.length};
        }""")
        ok(tid, cat, name, f"visible_links={info['total']} bad_href={info['bad']}")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0044_internal_links_not_404(browser):
    tid, cat, name = "TC_0044", "Interaction", "內部連結不 404"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        links = page.evaluate(f"""() => {{
            const origin = window.location.origin;
            return [...document.querySelectorAll('a[href]')]
                .map(a => a.href)
                .filter(h => h.startsWith(origin))
                .slice(0, 10);
        }}""")
        failed = []
        for link in links:
            try:
                resp = page.request.head(link, timeout=5000)
                if resp.status >= 400:
                    failed.append(f"{resp.status}:{link[:60]}")
            except Exception:
                pass
        assert len(failed) == 0, f"404 links: {failed}"
        ok(tid, cat, name, f"checked={len(links)} all OK")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0045_links_clickable(browser):
    tid, cat, name = "TC_0045", "Interaction", "連結可點擊"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        blocked = page.evaluate("""() => {
            const links = [...document.querySelectorAll('a')].filter(a => a.offsetWidth > 0);
            return links.filter(a => {
                const s = getComputedStyle(a);
                return s.pointerEvents === 'none' || s.visibility === 'hidden';
            }).length;
        }""")
        assert blocked == 0, f"{blocked} links blocked by CSS"
        ok(tid, cat, name, f"No CSS-blocked links")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


# ===========================================================================
# 四、按鈕互動 (TC_030 ~ TC_032)
# ===========================================================================

def tc0046_button_click_no_crash(browser):
    tid, cat, name = "TC_0046", "Interaction", "按鈕點擊不 crash"
    ctx, page = new_page(browser)
    page_errors = []
    try:
        page.on("pageerror", lambda e: page_errors.append(str(e)))
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        btn_count = page.evaluate("() => document.querySelectorAll('button').length")
        # 只點前 5 個按鈕避免副作用
        for i in range(min(btn_count, 5)):
            try:
                btn = page.locator("button").nth(i)
                if btn.is_visible():
                    btn.click(timeout=3000)
                    page.wait_for_timeout(500)
            except Exception:
                pass
        assert len(page_errors) == 0, f"JS errors after click: {page_errors[:3]}"
        ok(tid, cat, name, f"Clicked {min(btn_count, 5)} buttons, no crash")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0047_button_has_label(browser):
    tid, cat, name = "TC_0047", "Accessibility", "按鈕有可識別文字或 aria-label"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        info = page.evaluate("""() => {
            const btns = [...document.querySelectorAll('button')];
            const labeled = btns.filter(b =>
                (b.innerText && b.innerText.trim().length > 0) ||
                b.getAttribute('aria-label') ||
                b.getAttribute('title')
            );
            return {total: btns.length, labeled: labeled.length};
        }""")
        if info["total"] > 0:
            ratio = info["labeled"] / info["total"]
            note = f"total={info['total']} labeled={info['labeled']} ({ratio:.0%})"
        else:
            note = "No buttons found"
        ok(tid, cat, name, note)
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


# ===========================================================================
# 五、表單元素 (TC_040 ~ TC_043)
# ===========================================================================

def tc0048_input_fillable(browser):
    tid, cat, name = "TC_0048", "Interaction", "輸入框可輸入"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        inputs = page.locator("input[type='text'], input[type='search'], input:not([type])")
        count = inputs.count()
        filled = 0
        for i in range(min(count, 3)):
            try:
                inp = inputs.nth(i)
                if inp.is_visible():
                    inp.fill("test_input")
                    val = inp.input_value()
                    if val == "test_input":
                        filled += 1
                    inp.fill("")
            except Exception:
                pass
        ok(tid, cat, name, f"visible_inputs={count} fillable={filled}")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0049_password_field_masked(browser):
    tid, cat, name = "TC_0049", "Security", "密碼欄位 type=password"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        info = page.evaluate("""() => {
            const inputs = [...document.querySelectorAll('input')];
            const pwd_like = inputs.filter(i =>
                (i.name && i.name.toLowerCase().includes('pass')) ||
                (i.placeholder && i.placeholder.toLowerCase().includes('pass')) ||
                (example.internal && example.internal.toLowerCase().includes('pass'))
            );
            const masked = pwd_like.filter(i => i.type === 'password');
            return {pwd_like: pwd_like.length, masked: masked.length};
        }""")
        if info["pwd_like"] > 0:
            assert info["masked"] == info["pwd_like"], \
                f"{info['pwd_like'] - info['masked']} password fields not masked"
        ok(tid, cat, name, f"pwd_fields={info['pwd_like']} masked={info['masked']}")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0050_search_box_works(browser):
    tid, cat, name = "TC_0050", "Interaction", "搜尋框存在且可用"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        search = page.locator(
            "input[type='search'], input[role='searchbox'], "
            "input[name='q'], input[name='search'], input[aria-label*='earch']"
        ).first
        if search.count() > 0 and search.is_visible():
            search.fill("test")
            ok(tid, cat, name, "Search box found and fillable")
        else:
            ok(tid, cat, name, "No search box found (not required)")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


# ===========================================================================
# 六、JS 錯誤偵測 (TC_050 ~ TC_052)
# ===========================================================================

def tc0051_no_js_errors(browser):
    tid, cat, name = "TC_0051", "Error Handling", "無 Uncaught JS Error"
    ctx, page = new_page(browser)
    page_errors = []
    try:
        page.on("pageerror", lambda e: page_errors.append(str(e)))
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        page.wait_for_timeout(3000)
        assert len(page_errors) == 0, f"JS errors: {page_errors[:3]}"
        ok(tid, cat, name, f"No JS errors")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0052_no_console_errors(browser):
    """TC_0052: Console 是否存在 Error 級別訊息 [UNIVERSAL]
    監聽 console.error，分類: CORS / 404 / JS Runtime / 其他。
    與 TC_0053 差異: 0052 抓 console 印出的錯誤訊息，0053 抓 request 本身失敗。
    """
    tid, cat, name = "TC_0052", "Error Handling", "Console 是否存在 Error 級別訊息"
    ctx, page = new_page(browser)
    console_errors = []
    try:
        page.on("console", lambda msg: console_errors.append(msg.text)
                if msg.type == "error" else None)
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        page.wait_for_timeout(3000)
        noise = ["favicon", "manifest", "adsbygoogle", "third-party", "blocked"]
        real = [e for e in console_errors
                if not any(kw in e.lower() for kw in noise)]
        if len(real) > 0:
            # 分類統計
            cors = [e for e in real if "cors" in e.lower() or "access-control" in e.lower()]
            res404 = [e for e in real if "404" in e]
            net_err = [e for e in real if "net::err" in e.lower() and e not in cors]
            js_err = [e for e in real if e not in cors and e not in res404 and e not in net_err]
            parts = []
            if cors:
                parts.append(f"CORS blocked={len(cors)}")
            if res404:
                parts.append(f"404 資源缺失={len(res404)}")
            if net_err:
                parts.append(f"網路錯誤={len(net_err)}")
            if js_err:
                parts.append(f"JS/其他={len(js_err)}")
            summary = f"Console errors ({len(real)}): {' | '.join(parts)}"
            assert False, summary
        ok(tid, cat, name, f"total={len(console_errors)} real=0")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0053_no_failed_resources(browser):
    """TC_0053: 資源載入無 failed（HTTP request 層） [UNIVERSAL]
    監聽 requestfailed 事件，分類: API / CDN 圖片 / 其他。
    與 TC_0052 差異: 0053 抓 request 本身發不出去或被拒，0052 抓 console 印的錯誤文字。
    """
    tid, cat, name = "TC_0053", "Error Handling", "頁面資源載入是否存在失敗（HTTP request 層）"
    ctx, page = new_page(browser)
    failed_reqs = []
    try:
        def _on_fail(req):
            failed_reqs.append({
                "type": req.resource_type,
                "url": req.url,
                "failure": req.failure or "",
            })
        page.on("requestfailed", _on_fail)
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        page.wait_for_timeout(3000)
        # 排除廣告/追蹤器
        noise = ["ads", "analytics", "tracking", "doubleclick", "facebook", "google-analytics"]
        real = [r for r in failed_reqs
                if not any(n in r["url"].lower() for n in noise)]
        if len(real) > 0:
            # 依來源分類，取唯一 URL
            api_fails = []
            cdn_fails = []
            other_fails = []
            seen = set()
            for r in real:
                url = r["url"]
                short = url.split("?")[0]  # 去 query string
                if short in seen:
                    continue
                seen.add(short)
                if r["type"] in ("fetch", "xhr"):
                    api_fails.append(short)
                elif r["type"] == "image" or "cdn" in url.lower() or "static" in url.lower():
                    cdn_fails.append(short.split("/")[-1])  # 只取檔名
                else:
                    other_fails.append(short.split("/")[-1])
            parts = []
            if api_fails:
                parts.append(f"API 請求失敗={len(api_fails)} ({', '.join(a[:40] for a in api_fails[:2])})")
            if cdn_fails:
                unique_names = list(dict.fromkeys(cdn_fails))
                parts.append(f"CDN 圖片缺失={len(cdn_fails)} ({', '.join(unique_names[:3])})")
            if other_fails:
                parts.append(f"其他={len(other_fails)}")
            summary = f"Failed resources ({len(real)}筆, {len(seen)}種): {' | '.join(parts)}"
            assert False, summary
        ok(tid, cat, name, f"total_failed={len(failed_reqs)} real=0")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


# ===========================================================================
# 七、SEO 基礎 (TC_060 ~ TC_062)
# ===========================================================================

def tc0054_charset_meta(browser):
    tid, cat, name = "TC_0054", "SEO", "charset meta 存在"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        has_charset = page.evaluate("""() =>
            !!document.querySelector('meta[charset]') ||
            !!document.querySelector('meta[http-equiv="Content-Type"]')
        """)
        assert has_charset, "No charset meta found"
        ok(tid, cat, name, "charset meta exists")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0055_viewport_meta(browser):
    tid, cat, name = "TC_0055", "SEO", "viewport meta 存在"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        viewport = page.evaluate("""() => {
            const m = document.querySelector('meta[name="viewport"]');
            return m ? m.getAttribute('content') : null;
        }""")
        assert viewport and "width" in viewport, f"viewport meta: {viewport}"
        ok(tid, cat, name, f"viewport='{viewport[:60]}'")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0056_html_lang(browser):
    tid, cat, name = "TC_0056", "Accessibility", "頁面有 lang 屬性"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        lang = page.evaluate("() => document.documentElement.lang")
        assert lang and len(lang) >= 2, f"html lang='{lang}'"
        ok(tid, cat, name, f"lang='{lang}'")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


# ===========================================================================
# 八、無障礙基礎 (TC_070 ~ TC_072)
# ===========================================================================

def tc0057_tab_focus_moves(browser):
    tid, cat, name = "TC_0057", "Accessibility", "Tab 鍵 Focus 可移動"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        page.keyboard.press("Tab")
        page.wait_for_timeout(500)
        tag = page.evaluate("() => document.activeElement.tagName")
        assert tag != "BODY", f"Focus stuck on {tag}"
        ok(tid, cat, name, f"Focus moved to {tag}")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0058_aria_coverage(browser):
    tid, cat, name = "TC_0058", "Accessibility", "互動元素 ARIA 標記覆蓋率"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        info = page.evaluate("""() => {
            const interactive = [...document.querySelectorAll('button, a, input, select, textarea')];
            const with_aria = interactive.filter(el =>
                [...el.attributes].some(a => a.name.startsWith('aria-')) ||
                el.getAttribute('role')
            );
            return {total: interactive.length, with_aria: with_aria.length};
        }""")
        ratio = info["with_aria"] / info["total"] if info["total"] > 0 else 1
        ok(tid, cat, name, f"interactive={info['total']} aria={info['with_aria']} ({ratio:.0%})")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


# ===========================================================================
# 九、效能基礎 (TC_080 ~ TC_081)
# ===========================================================================

def tc0059_dom_node_count(browser):
    tid, cat, name = "TC_0059", "Performance", "DOM 節點數合理"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        count = page.evaluate("() => document.querySelectorAll('*').length")
        note = f"DOM nodes={count}"
        if count > 5000:
            note += " (WARNING: > 5000)"
        ok(tid, cat, name, note)
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0060_first_contentful_paint(browser):
    tid, cat, name = "TC_0060", "Performance", "首次繪製時間合理"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        page.wait_for_timeout(2000)
        fcp = page.evaluate("""() => {
            const entries = performance.getEntriesByType('paint');
            const fcp = entries.find(e => e.name === 'first-contentful-paint');
            return fcp ? fcp.startTime : -1;
        }""")
        if fcp > 0:
            assert fcp < 5000, f"FCP too slow: {fcp:.0f}ms"
            ok(tid, cat, name, f"FCP={fcp:.0f}ms")
        else:
            ok(tid, cat, name, "FCP not available (SPA)")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


# ===========================================================================
# 十、RWD 響應式 (TC_090 ~ TC_091)
# ===========================================================================

def tc0061_mobile_no_overflow(browser):
    tid, cat, name = "TC_0061", "RWD", "手機寬度無水平溢出"
    ctx = browser.new_context(viewport={"width": 375, "height": 667})
    page = ctx.new_page()
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        page.wait_for_timeout(2000)
        info = page.evaluate("""() => ({
            scrollWidth: document.documentElement.scrollWidth,
            clientWidth: document.documentElement.clientWidth
        })""")
        overflow = info["scrollWidth"] - info["clientWidth"]
        note = f"scroll={info['scrollWidth']} client={info['clientWidth']} overflow={overflow}px"
        if overflow > 10:
            note += " (WARNING: horizontal overflow)"
        ok(tid, cat, name, note)
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0062_desktop_renders(browser):
    tid, cat, name = "TC_0062", "RWD", "桌面寬度正常顯示"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        length = page.evaluate("() => document.body.innerHTML.length")
        assert length > 100, f"body too short: {length}"
        ok(tid, cat, name, f"body.innerHTML.length={length}")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


# ===========================================================================
# 十一、Cookie / Session 基礎 (TC_100 ~ TC_102)
# ===========================================================================

def tc0063_cookie_secure(browser):
    tid, cat, name = "TC_0063", "Security", "Cookie 有 Secure 屬性"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        is_https = BASE_URL.startswith("https")
        cookies = ctx.cookies()
        if is_https and cookies:
            insecure = [c["name"] for c in cookies if not c.get("secure", False)]
            note = f"total={len(cookies)} insecure={len(insecure)}"
            if insecure:
                note += f" names={insecure[:5]}"
        else:
            note = f"cookies={len(cookies)} https={is_https}"
        ok(tid, cat, name, note)
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0064_cookie_httponly(browser):
    tid, cat, name = "TC_0064", "Security", "Cookie 有 HttpOnly"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        cookies = ctx.cookies()
        session_like = [c for c in cookies
                        if any(k in c["name"].lower()
                               for k in ["session", "token", "sid", "auth"])]
        no_httponly = [c["name"] for c in session_like if not c.get("httpOnly", False)]
        note = f"session_cookies={len(session_like)} no_httponly={len(no_httponly)}"
        if no_httponly:
            note += f" names={no_httponly[:5]}"
        ok(tid, cat, name, note)
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0065_cookie_samesite(browser):
    tid, cat, name = "TC_0065", "Security", "Cookie 有 SameSite"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        cookies = ctx.cookies()
        no_samesite = [c["name"] for c in cookies
                       if c.get("sameSite", "None") == "None"]
        note = f"total={len(cookies)} samesite_none={len(no_samesite)}"
        ok(tid, cat, name, note)
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


# ===========================================================================
# 十二、資安測試 (TC_110 ~ TC_116)
# ===========================================================================

def tc0066_xss_url_param(browser):
    tid, cat, name = "TC_0066", "Security", "Reflected XSS — URL 參數注入"
    ctx, page = new_page(browser)
    dialog_fired = []
    try:
        page.on("dialog", lambda d: (dialog_fired.append(d.message), d.dismiss()))
        xss_url = BASE_URL.rstrip("/") + "?q=<script>alert('xss')</script>"
        page.goto(xss_url, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        assert len(dialog_fired) == 0, f"XSS dialog triggered: {dialog_fired}"
        ok(tid, cat, name, f"No XSS dialog on URL param injection")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0067_xss_input(browser):
    tid, cat, name = "TC_0067", "Security", "Stored XSS — 表單輸入注入"
    ctx, page = new_page(browser)
    dialog_fired = []
    try:
        page.on("dialog", lambda d: (dialog_fired.append(d.message), d.dismiss()))
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        payload = "<img src=x onerror=alert('xss')>"
        inputs = page.locator("input[type='text'], input[type='search'], input:not([type])")
        for i in range(min(inputs.count(), 3)):
            try:
                inp = inputs.nth(i)
                if inp.is_visible():
                    inp.fill(payload)
                    inp.press("Enter")
                    page.wait_for_timeout(1000)
            except Exception:
                pass
        assert len(dialog_fired) == 0, f"XSS dialog triggered: {dialog_fired}"
        ok(tid, cat, name, f"No XSS dialog on input injection")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0068_sql_injection(browser):
    tid, cat, name = "TC_0068", "Security", "SQL Injection 基礎偵測"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        payload = "' OR '1'='1"
        inputs = page.locator("input[type='text'], input[type='search'], input:not([type])")
        sql_errors = ["syntax error", "mysql", "ora-", "sql", "database error",
                      "unclosed quotation", "unterminated string"]
        found_sql_error = False
        for i in range(min(inputs.count(), 3)):
            try:
                inp = inputs.nth(i)
                if inp.is_visible():
                    inp.fill(payload)
                    inp.press("Enter")
                    page.wait_for_timeout(2000)
                    body_text = page.evaluate("() => document.body.innerText.toLowerCase()")
                    if any(err in body_text for err in sql_errors):
                        found_sql_error = True
                        break
            except Exception:
                pass
        assert not found_sql_error, "SQL error message exposed in response"
        ok(tid, cat, name, "No SQL error messages exposed")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0069_open_redirect(browser):
    tid, cat, name = "TC_0069", "Security", "Open Redirect"
    ctx, page = new_page(browser)
    try:
        parsed = urlparse(BASE_URL)
        test_url = f"{BASE_URL.rstrip('/')}?redirect=https://evil.com&next=https://evil.com&return=https://evil.com"
        page.goto(test_url, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        current = urlparse(page.url)
        assert current.hostname != "evil.com", f"Redirected to {page.url}"
        ok(tid, cat, name, f"No open redirect, stayed on {current.hostname}")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0070_security_headers(browser):
    tid, cat, name = "TC_0070", "Security", "HTTP Security Headers"
    ctx, page = new_page(browser)
    try:
        resp = page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        headers = resp.headers if resp else {}
        checks = {
            "x-content-type-options": headers.get("x-content-type-options", ""),
            "x-frame-options": headers.get("x-frame-options", ""),
            "strict-transport-security": headers.get("strict-transport-security", ""),
        }
        missing = [k for k, v in checks.items() if not v]
        present = [k for k, v in checks.items() if v]
        note = f"present={present} missing={missing}"
        ok(tid, cat, name, note)
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0071_csrf_token(browser):
    tid, cat, name = "TC_0071", "Security", "CSRF Token 存在"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        info = page.evaluate("""() => {
            const forms = [...document.querySelectorAll('form[method="post"], form[method="POST"]')];
            const with_csrf = forms.filter(f =>
                f.querySelector('input[name*="csrf"], input[name*="token"], input[name*="_token"]')
            );
            return {post_forms: forms.length, with_csrf: with_csrf.length};
        }""")
        note = f"POST forms={info['post_forms']} with_csrf={info['with_csrf']}"
        if info["post_forms"] > 0 and info["with_csrf"] == 0:
            note += " (WARNING: POST form without CSRF token)"
        ok(tid, cat, name, note)
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0072_mixed_content(browser):
    tid, cat, name = "TC_0072", "Security", "Mixed Content 偵測"
    ctx, page = new_page(browser)
    mixed = []
    try:
        if not BASE_URL.startswith("https"):
            ok(tid, cat, name, "HTTP site, skip mixed content check")
            return
        page.on("console", lambda msg: mixed.append(msg.text)
                if "mixed content" in msg.text.lower() else None)
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        page.wait_for_timeout(3000)
        http_resources = page.evaluate("""() => {
            const all = performance.getEntriesByType('resource');
            return all.filter(r => r.name.startsWith('http://')).map(r => r.name).slice(0, 5);
        }""")
        note = f"mixed_warnings={len(mixed)} http_resources={len(http_resources)}"
        if http_resources:
            note += f" urls={http_resources[:3]}"
        ok(tid, cat, name, note)
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0074_login_error_no_leak(browser):
    """TC_0074: 登入錯誤訊息不洩露帳號是否存在"""
    tid, cat, name = "TC_0074", "Security", "登入錯誤不洩露帳號資訊"
    ctx, page = new_page(browser)
    try:
        # 嘗試找 login 頁面
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        login_href = page.evaluate("""() => {
            const a = document.querySelector('a[href*="login"], a[href*="signin"], a[href*="sign-in"]');
            return a ? a.href : null;
        }""")
        login_url = login_href or (BASE_URL.rstrip("/") + "/login")
        page.goto(login_url, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_timeout(2000)

        # 檢查是否有登入表單
        pwd_field = page.locator("input[type='password']")
        if pwd_field.count() == 0:
            ok(tid, cat, name, "No login form found, skip")
            return

        # 找 email/username 欄位
        email_field = page.locator(
            "input[name='email'], input[type='email'], "
            "input[name='username'], input[name='user']"
        ).first
        if email_field.count() == 0:
            ok(tid, cat, name, "No email/username field found, skip")
            return

        # 送出錯誤帳密
        field_type = email_field.get_attribute("type") or "text"
        test_email = "nonexistent_user_test@fakeemail99.com" if field_type == "email" else "nonexistent_user_test"
        email_field.fill(test_email)
        pwd_field.first.fill("WrongPassword!@#123")
        # 在包含 password 欄位的 form 內找 submit 按鈕
        login_form = page.locator("form:has(input[type='password'])")
        if login_form.count() > 0:
            submit = login_form.first.locator(
                "button[type='submit'], input[type='submit'], button"
            ).first
            if submit.count() > 0 and submit.is_visible():
                submit.click(timeout=5000)
            else:
                pwd_field.first.press("Enter")
        else:
            pwd_field.first.press("Enter")
        page.wait_for_timeout(3000)

        body_text = page.locator("body").inner_text().lower()
        leak_phrases = [
            "email not found", "user not found", "account not found",
            "no account", "doesn't exist", "does not exist",
            "not registered", "no user", "email is not registered",
        ]
        leaked = [p for p in leak_phrases if p in body_text]
        assert len(leaked) == 0, f"Error message leaks account info: {leaked}"
        ok(tid, cat, name, f"No account leak in error msg")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0075_login_form_https(browser):
    """TC_0075: 登入表單 action 走 HTTPS"""
    tid, cat, name = "TC_0075", "Security", "登入表單透過 HTTPS 送出"
    ctx, page = new_page(browser)
    try:
        if not BASE_URL.startswith("https"):
            ok(tid, cat, name, "Site is HTTP, skip HTTPS form check")
            return

        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        login_href = page.evaluate("""() => {
            const a = document.querySelector('a[href*="login"], a[href*="signin"], a[href*="sign-in"]');
            return a ? a.href : null;
        }""")
        login_url = login_href or (BASE_URL.rstrip("/") + "/login")
        page.goto(login_url, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_timeout(2000)

        pwd_field = page.locator("input[type='password']")
        if pwd_field.count() == 0:
            ok(tid, cat, name, "No login form found, skip")
            return

        # 檢查 form action
        form_actions = page.evaluate("""() => {
            const forms = [...document.querySelectorAll('form')];
            const with_pwd = forms.filter(f => f.querySelector('input[type="password"]'));
            return with_pwd.map(f => ({
                action: f.action || window.location.href,
                method: f.method
            }));
        }""")
        http_forms = [f for f in form_actions if f["action"].startswith("http://")]
        assert len(http_forms) == 0, f"Login form submits over HTTP: {http_forms}"
        # 也確認登入頁本身是 HTTPS
        assert page.url.startswith("https"), f"Login page not HTTPS: {page.url}"
        ok(tid, cat, name, f"forms={len(form_actions)} all HTTPS, page={page.url[:50]}")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0073_cross_browser(playwright_instance):
    tid, cat, name = "TC_0073", "Cross-browser", "跨瀏覽器載入驗證"
    browser_map = {
        "chromium": playwright_instance.chromium,
        "firefox": playwright_instance.firefox,
        "webkit": playwright_instance.webkit,
    }
    passed, skipped, failed = [], [], []
    for bname, btype in browser_map.items():
        try:
            b = btype.launch(headless=True)
            ctx = b.new_context(viewport={"width": 1920, "height": 1080})
            pg = ctx.new_page()
            pg.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
            pg.wait_for_selector("body", timeout=8000)
            assert len(pg.title()) > 0
            passed.append(bname)
            ctx.close()
            b.close()
        except Exception as e:
            msg = str(e)
            if "Executable doesn't exist" in msg:
                skipped.append(bname)
            else:
                failed.append(f"{bname}:{msg[:60]}")
    if failed:
        ng(tid, cat, name, f"FAIL={failed}")
    else:
        ok(tid, cat, name, f"PASS={passed} SKIP={skipped}")


# ===========================================================================
# 十三、登入頁面標準測項 (TC_0076 ~ TC_0080)
# ===========================================================================

def tc0076_login_form_elements(browser):
    """TC_0076: 登入表單元素存在性驗證 [UNIVERSAL]"""
    tid, cat, name = "TC_0076", "Functional", "登入表單元素存在性驗證"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        login_href = page.evaluate("""() => {
            const a = document.querySelector('a[href*="login"], a[href*="signin"], a[href*="sign-in"]');
            return a ? a.href : null;
        }""")
        login_url = login_href or (BASE_URL.rstrip("/") + "/login")
        page.goto(login_url, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_timeout(2000)

        pwd_field = page.locator("input[type='password']")
        if pwd_field.count() == 0:
            ok(tid, cat, name, "No login page, skip")
            return

        email_field = page.locator(
            "input[name='email'], input[type='email'], "
            "input[name='username'], input[name='user'], "
            "input[name='account']"
        ).first
        has_email = email_field.count() > 0
        submit_btn = page.locator(
            "button[type='submit'], input[type='submit'], "
            "button:has-text('Login'), button:has-text('Sign in'), "
            "button:has-text('登入'), button:has-text('Log in')"
        ).first
        has_submit = submit_btn.count() > 0
        assert has_email, "No email/username input found"
        assert has_submit, "No submit button found"
        ok(tid, cat, name, f"pwd=True email={has_email} submit={has_submit}")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0077_empty_submit_validation(browser):
    """TC_0077: 空白帳密送出驗證提示 [UNIVERSAL]"""
    tid, cat, name = "TC_0077", "Functional", "空白帳密送出驗證提示"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        login_href = page.evaluate("""() => {
            const a = document.querySelector('a[href*="login"], a[href*="signin"], a[href*="sign-in"]');
            return a ? a.href : null;
        }""")
        login_url = login_href or (BASE_URL.rstrip("/") + "/login")
        page.goto(login_url, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_timeout(2000)

        pwd_field = page.locator("input[type='password']")
        if pwd_field.count() == 0:
            ok(tid, cat, name, "No login form, skip")
            return

        # 不填任何欄位，直接送出
        login_form = page.locator("form:has(input[type='password'])")
        if login_form.count() > 0:
            submit = login_form.first.locator(
                "button[type='submit'], input[type='submit'], button"
            ).first
            if submit.count() > 0 and submit.is_visible():
                submit.click(timeout=5000)
            else:
                pwd_field.first.press("Enter")
        else:
            pwd_field.first.press("Enter")
        page.wait_for_timeout(2000)

        body_text = page.locator("body").inner_text().lower()
        validation_hints = [
            "required", "please", "enter", "invalid", "error",
            "cannot be empty", "必填", "請輸入", "不能為空",
        ]
        found = [h for h in validation_hints if h in body_text]
        ok(tid, cat, name, f"validation_hints={found[:5]}")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0078_password_toggle(browser):
    """TC_0078: 密碼欄位顯示/隱藏切換 [UNIVERSAL]"""
    tid, cat, name = "TC_0078", "Interaction", "密碼欄位顯示/隱藏切換"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        login_href = page.evaluate("""() => {
            const a = document.querySelector('a[href*="login"], a[href*="signin"], a[href*="sign-in"]');
            return a ? a.href : null;
        }""")
        login_url = login_href or (BASE_URL.rstrip("/") + "/login")
        page.goto(login_url, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_timeout(2000)

        pwd_field = page.locator("input[type='password']").first
        if pwd_field.count() == 0:
            ok(tid, cat, name, "No password field, skip")
            return

        initial_type = pwd_field.get_attribute("type")
        assert initial_type == "password", f"Initial type={initial_type}"

        toggle = page.locator(
            "button[class*='toggle'], button[class*='show'], button[class*='eye'], "
            "[class*='toggle'][class*='password'], [class*='eye'], "
            "[aria-label*='show'], [aria-label*='password'], "
            "button[class*='visibility']"
        ).first
        if toggle.count() == 0 or not toggle.is_visible():
            ok(tid, cat, name, "No password toggle found, skip")
            return

        toggle.click(timeout=3000)
        page.wait_for_timeout(500)
        new_type = pwd_field.get_attribute("type")
        ok(tid, cat, name, f"initial=password after_toggle={new_type}")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0079_forgot_password_link(browser):
    """TC_0079: 忘記密碼連結存在且可導向 [UNIVERSAL]"""
    tid, cat, name = "TC_0079", "Navigation", "忘記密碼連結存在且可導向"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        login_href = page.evaluate("""() => {
            const a = document.querySelector('a[href*="login"], a[href*="signin"], a[href*="sign-in"]');
            return a ? a.href : null;
        }""")
        login_url = login_href or (BASE_URL.rstrip("/") + "/login")
        page.goto(login_url, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_timeout(2000)

        forgot_link = page.locator(
            'a[href*="forgot"], a[href*="reset"], '
            'a:has-text("forgot"), a:has-text("Forgot"), '
            'a:has-text("忘記"), a:has-text("密碼")'
        ).first
        if forgot_link.count() == 0 or not forgot_link.is_visible():
            ok(tid, cat, name, "No forgot password link, skip")
            return

        href = forgot_link.get_attribute("href")
        assert href and len(href) > 0, "Forgot password link has empty href"
        ok(tid, cat, name, f"forgot_link href={href[:60]}")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0080_register_link(browser):
    """TC_0080: 註冊連結存在且可導向 [UNIVERSAL]"""
    tid, cat, name = "TC_0080", "Navigation", "註冊連結存在且可導向"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        login_href = page.evaluate("""() => {
            const a = document.querySelector('a[href*="login"], a[href*="signin"], a[href*="sign-in"]');
            return a ? a.href : null;
        }""")
        login_url = login_href or (BASE_URL.rstrip("/") + "/login")
        page.goto(login_url, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_timeout(2000)

        register_link = page.locator(
            'a[href*="register"], a[href*="signup"], a[href*="sign-up"], '
            'a:has-text("Sign Up"), a:has-text("Register"), '
            'a:has-text("Create account"), a:has-text("註冊"), a:has-text("注册")'
        ).first
        if register_link.count() == 0 or not register_link.is_visible():
            ok(tid, cat, name, "No register link, skip")
            return

        href = register_link.get_attribute("href")
        assert href and len(href) > 0, "Register link has empty href"
        ok(tid, cat, name, f"register_link href={href[:60]}")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


# ===========================================================================
# 十四、未登入狀態標準測項 (TC_0081 ~ TC_0082)
# ===========================================================================

def tc0081_unauth_protected_redirect(browser):
    """TC_0081: 未登入存取受保護功能應提示登入 [UNIVERSAL]"""
    tid, cat, name = "TC_0081", "Functional", "未登入存取受保護功能應提示登入"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)

        protected_link = page.locator(
            'a[href*="upload"], a[href*="studio"], a[href*="playlist"], '
            'a[href*="subscription"], a[href*="settings"], '
            'a[href*="profile"], a[href*="dashboard"]'
        ).first
        if protected_link.count() == 0 or not protected_link.is_visible():
            ok(tid, cat, name, "No protected page links found, skip")
            return

        href = protected_link.get_attribute("href")
        protected_link.click(timeout=5000)
        page.wait_for_timeout(3000)

        current_url = page.url.lower()
        body_text = page.locator("body").inner_text().lower()
        redirected = "login" in current_url or "signin" in current_url
        has_prompt = any(kw in body_text for kw in [
            "sign in", "log in", "login", "登入", "please log in",
        ])
        ok(tid, cat, name, f"href={href[:40]} redirected={redirected} prompt={has_prompt}")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0082_unauth_action_blocked(browser):
    """TC_0082: 未登入不應執行受保護操作 [UNIVERSAL]"""
    tid, cat, name = "TC_0082", "Functional", "未登入不應執行受保護操作"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)

        action_btn = page.locator(
            'button:has-text("Subscribe"), button:has-text("Like"), '
            'button:has-text("Upload"), button:has-text("Comment"), '
            'button:has-text("訂閱"), button:has-text("留言")'
        ).first
        if action_btn.count() == 0 or not action_btn.is_visible():
            ok(tid, cat, name, "No auth-required action buttons found, skip")
            return

        action_btn.click(timeout=5000)
        page.wait_for_timeout(2000)

        current_url = page.url.lower()
        body_text = page.locator("body").inner_text().lower()
        redirected = "login" in current_url or "signin" in current_url
        has_modal = page.locator('[role="dialog"], .modal, [class*="modal"]').count() > 0
        has_prompt = any(kw in body_text for kw in [
            "sign in", "log in", "login", "登入",
        ])
        ok(tid, cat, name, f"redirected={redirected} modal={has_modal} prompt={has_prompt}")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


# ===========================================================================
# 十五、頁面導覽標準測項 (TC_0083 ~ TC_0084)
# ===========================================================================

def tc0083_nav_links_load(browser):
    """TC_0083: 導覽列連結導向後頁面正常載入 [UNIVERSAL]"""
    tid, cat, name = "TC_0083", "Navigation", "導覽列連結導向後頁面正常載入"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)

        parsed = urlparse(BASE_URL)
        base_domain = parsed.hostname
        links = page.evaluate("""(baseDomain) => {
            const selectors = 'nav a[href], header a[href], .navbar a[href], .nav-links a[href]';
            const anchors = [...document.querySelectorAll(selectors)];
            return anchors
                .map(a => a.href)
                .filter(h => {
                    try {
                        const u = new URL(h);
                        return u.hostname === baseDomain
                            && u.hash === ''
                            && !h.startsWith('javascript:');
                    } catch { return false; }
                })
                .filter((v, i, arr) => arr.indexOf(v) === i)
                .slice(0, 3);
        }""", base_domain)

        if len(links) == 0:
            ok(tid, cat, name, "No internal nav links found, skip")
            return

        checked = 0
        for href in links:
            resp = page.goto(href, timeout=30000, wait_until="domcontentloaded")
            status = resp.status if resp else 0
            length = page.evaluate("() => document.body.innerHTML.length")
            assert status < 400, f"{href} returned {status}"
            assert length > 100, f"{href} body too short: {length}"
            checked += 1
        ok(tid, cat, name, f"checked {checked} nav links, all OK")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0084_target_page_content(browser):
    """TC_0084: 目標頁面核心元素可見 [UNIVERSAL]"""
    tid, cat, name = "TC_0084", "Navigation", "目標頁面核心元素可見"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)

        parsed = urlparse(BASE_URL)
        base_domain = parsed.hostname
        first_link = page.evaluate("""(baseDomain) => {
            const selectors = 'nav a[href], header a[href], .navbar a[href], .nav-links a[href]';
            const anchors = [...document.querySelectorAll(selectors)];
            const internal = anchors
                .map(a => a.href)
                .filter(h => {
                    try {
                        const u = new URL(h);
                        return u.hostname === baseDomain
                            && u.hash === ''
                            && !h.startsWith('javascript:');
                    } catch { return false; }
                });
            return internal.length > 0 ? internal[0] : null;
        }""", base_domain)

        if not first_link:
            ok(tid, cat, name, "No internal nav link found, skip")
            return

        page.goto(first_link, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        length = page.evaluate("() => document.body.innerHTML.length")
        assert length > 100, f"Body too short: {length}"
        visible_count = page.evaluate("""() => {
            const els = document.querySelectorAll('h1, h2, h3, main, article, section, .content');
            return [...els].filter(e => e.offsetWidth > 0 && e.offsetHeight > 0).length;
        }""")
        ok(tid, cat, name, f"url={first_link[:50]} body={length} visible_elements={visible_count}")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


# ===========================================================================
# 十六、效能類 (TC_0085 ~ TC_0086)
# ===========================================================================

def tc0085_dom_nodes_warning(browser):
    """TC_0085: DOM 節點數量警告 [UNIVERSAL]"""
    tid, cat, name = "TC_0085", "Performance", "DOM 節點數量警告"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        page.wait_for_timeout(3000)
        count = page.evaluate("() => document.querySelectorAll('*').length")
        if count > 5000:
            raise AssertionError(f"DOM nodes={count} exceeds 5000 limit")
        note = f"DOM nodes={count}"
        if count > 3000:
            note += " (DOM nodes high)"
        ok(tid, cat, name, note)
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0086_page_total_size(browser):
    """TC_0086: 頁面總資源大小合理性 [UNIVERSAL]"""
    tid, cat, name = "TC_0086", "Performance", "頁面總資源大小合理性"
    ctx, page = new_page(browser)
    total_bytes = [0]
    try:
        def _on_response(response):
            try:
                body = response.body()
                total_bytes[0] += len(body)
            except Exception:
                pass
        page.on("response", _on_response)
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        page.wait_for_timeout(5000)
        size_mb = total_bytes[0] / (1024 * 1024)
        assert total_bytes[0] <= 10485760, f"Page too heavy: {size_mb:.2f}MB"
        ok(tid, cat, name, f"total_size={size_mb:.2f}MB")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


# ===========================================================================
# 十七、安全性類 (TC_0087 ~ TC_0089)
# ===========================================================================

def tc0087_xss_location_hash(browser):
    """TC_0087: DOM-based XSS 偵測（location.hash 注入） [UNIVERSAL]"""
    tid, cat, name = "TC_0087", "Security", "DOM-based XSS（location.hash 注入）"
    ctx, page = new_page(browser)
    dialog_fired = []
    try:
        page.on("dialog", lambda d: (dialog_fired.append(d.message), d.dismiss()))
        xss_url = BASE_URL.rstrip("/") + "#<img src=x onerror=alert('xss')>"
        page.goto(xss_url, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        assert len(dialog_fired) == 0, f"XSS dialog triggered via hash: {dialog_fired}"
        ok(tid, cat, name, "No XSS dialog from location.hash injection")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0088_clickjacking_protection(browser):
    """TC_0088: Clickjacking 防護 [UNIVERSAL]"""
    tid, cat, name = "TC_0088", "Security", "Clickjacking 防護"
    ctx, page = new_page(browser)
    try:
        resp = page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        headers = resp.headers if resp else {}
        x_frame = headers.get("x-frame-options", "")
        csp = headers.get("content-security-policy", "")
        has_xfo = x_frame.upper() in ("DENY", "SAMEORIGIN")
        has_csp_fa = "frame-ancestors" in csp
        assert has_xfo or has_csp_fa, "No clickjacking protection"
        ok(tid, cat, name, f"X-Frame-Options={x_frame or 'N/A'} CSP-frame-ancestors={has_csp_fa}")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


def tc0089_sensitive_info_in_url(browser):
    """TC_0089: 敏感資訊不在 URL 中傳遞 [UNIVERSAL]"""
    tid, cat, name = "TC_0089", "Security", "敏感資訊不在 URL 中傳遞"
    ctx, page = new_page(browser)
    try:
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        sensitive_params = ["password="<REDACTED>"token="<REDACTED>"secret="<REDACTED>"api_key="<REDACTED>"apikey="<REDACTED>"access_token="]
        leaky_links = page.evaluate("""(params) => {
            const anchors = [...document.querySelectorAll('a[href]')];
            const leaky = [];
            anchors.forEach(a => {
                const href = a.href.toLowerCase();
                params.forEach(p => {
                    if (href.includes(p)) {
                        leaky.push({href: a.href.substring(0, 80), param: p});
                    }
                });
            });
            return leaky.slice(0, 5);
        }""", sensitive_params)
        assert len(leaky_links) == 0, f"Sensitive info in URLs: {leaky_links}"
        ok(tid, cat, name, "No sensitive params found in links")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


# ===========================================================================
# 十八、可靠性類 (TC_0090)
# ===========================================================================

def tc0090_console_warnings_count(browser):
    """TC_0090: 頁面無 console.warn 過量 [UNIVERSAL]"""
    tid, cat, name = "TC_0090", "Reliability", "頁面無 console.warn 過量"
    ctx, page = new_page(browser)
    warnings = []
    try:
        page.on("console", lambda msg: warnings.append(msg.text)
                if msg.type == "warning" else None)
        page.goto(BASE_URL, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("body", timeout=8000)
        page.wait_for_timeout(5000)
        count = len(warnings)
        assert count <= 20, f"Excessive console warnings: {count}"
        ok(tid, cat, name, f"console warnings={count}")
    except Exception as e:
        ng(tid, cat, name, e, page)
    finally:
        ctx.close()


# ===========================================================================
# 執行入口
# ===========================================================================

ALL_TCS = [
    # 頁面載入
    tc0035_page_not_blank, tc0036_page_title_not_empty,
    tc0037_page_load_time, tc0038_http_status_ok,
    # 圖片
    tc0039_images_not_broken, tc0040_images_have_alt,
    tc0041_images_src_not_empty, tc0042_svg_icons_loaded,
    # 連結
    tc0043_links_href_not_empty, tc0044_internal_links_not_404,
    tc0045_links_clickable,
    # 按鈕
    tc0046_button_click_no_crash, tc0047_button_has_label,
    # 表單
    tc0048_input_fillable, tc0049_password_field_masked,
    tc0050_search_box_works,
    # JS 錯誤
    tc0051_no_js_errors, tc0052_no_console_errors, tc0053_no_failed_resources,
    # SEO
    tc0054_charset_meta, tc0055_viewport_meta, tc0056_html_lang,
    # 無障礙
    tc0057_tab_focus_moves, tc0058_aria_coverage,
    # 效能
    tc0059_dom_node_count, tc0060_first_contentful_paint,
    # RWD
    tc0061_mobile_no_overflow, tc0062_desktop_renders,
    # Cookie/Session
    tc0063_cookie_secure, tc0064_cookie_httponly, tc0065_cookie_samesite,
    # 資安
    tc0066_xss_url_param, tc0067_xss_input, tc0068_sql_injection,
    tc0069_open_redirect, tc0070_security_headers, tc0071_csrf_token,
    tc0072_mixed_content,
    # 登入表單安全
    tc0074_login_error_no_leak, tc0075_login_form_https,
    # 登入頁面標準測項
    tc0076_login_form_elements, tc0077_empty_submit_validation,
    tc0078_password_toggle, tc0079_forgot_password_link, tc0080_register_link,
    # 未登入狀態
    tc0081_unauth_protected_redirect, tc0082_unauth_action_blocked,
    # 頁面導覽
    tc0083_nav_links_load, tc0084_target_page_content,
    # 效能
    tc0085_dom_nodes_warning, tc0086_page_total_size,
    # 安全性
    tc0087_xss_location_hash, tc0088_clickjacking_protection,
    tc0089_sensitive_info_in_url,
    # 可靠性
    tc0090_console_warnings_count,
    # 跨瀏覽器（特殊：需 playwright instance）
    # tc0073 handled separately
]


def write_xlsx(xlsx_path):
    """將結果寫入 xlsx（只 append，不覆蓋既有資料）"""
    try:
        from openpyxl import Workbook, load_workbook
        from openpyxl.styles import PatternFill, Font

        green_fill = PatternFill("solid", fgColor="C6EFCE")
        green_font = Font(color="276221")
        red_fill = PatternFill("solid", fgColor="FFC7CE")
        red_font = Font(color="9C0006")

        headers = ["Test ID", "Category", "Test Name", "Status",
                    "Note", "Screenshot", "URL", "Execution Time"]

        if os.path.exists(xlsx_path):
            wb = load_workbook(xlsx_path)
            ws = wb.active
        else:
            wb = Workbook()
            ws = wb.active
            ws.title = "Results"
            for col, h in enumerate(headers, 1):
                ws.cell(row=1, column=col, value=h)
            ws.freeze_panes = "A2"

        start_row = ws.max_row + 1
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for i, r in enumerate(results):
            row = start_row + i
            ws.cell(row=row, column=1, value=r["id"])
            ws.cell(row=row, column=2, value=r["cat"])
            ws.cell(row=row, column=3, value=r["name"])
            ws.cell(row=row, column=4, value=r["status"])
            ws.cell(row=row, column=5, value=r["note"])
            ws.cell(row=row, column=6, value=r["path"])
            ws.cell(row=row, column=7, value=BASE_URL)
            ws.cell(row=row, column=8, value=now)

            fill = green_fill if r["status"] == "PASS" else red_fill
            font = green_font if r["status"] == "PASS" else red_font
            for col in range(1, 9):
                ws.cell(row=row, column=col).fill = fill
                ws.cell(row=row, column=col).font = font

        wb.save(xlsx_path)
        log(f"\n[xlsx] Saved {len(results)} results to {xlsx_path}")
    except ImportError:
        log("[xlsx] openpyxl not installed, skip xlsx output")


def main():
    global BASE_URL, DOMAIN

    parser = argparse.ArgumentParser(description="Universal TC Runner")
    parser.add_argument("--url", required=True, help="Target URL")
    parser.add_argument("--headed", action="store_true", help="Show browser")
    parser.add_argument("--xlsx", default="", help="Output xlsx path (append mode)")
    args = parser.parse_args()

    BASE_URL = args.url.rstrip("/")
    DOMAIN = urlparse(BASE_URL).hostname or "unknown"

    log(f"\n{'='*60}")
    log(f"Universal TC Runner — {DOMAIN}")
    log(f"URL: {BASE_URL}")
    log(f"{'='*60}")

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=not args.headed)

        for tc_func in ALL_TCS:
            tc_func(browser)

        # 跨瀏覽器（需 playwright instance）
        tc0073_cross_browser(pw)

        browser.close()

    # 統計
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = total - passed
    log(f"\n{'='*60}")
    log(f"Results: {passed}/{total} PASS | {failed} FAIL")
    log(f"{'='*60}")

    if args.xlsx:
        write_xlsx(args.xlsx)

    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
