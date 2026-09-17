"""
screenshot_diff.py — 修復前後截圖對比（gstack 特色：before/after 驗證）

用途:
  TC 修復流程中，自動比對修復前後的截圖，產出 diff 圖 + 差異百分比。

用法:
  from shared.ai.screenshot_diff import compare_screenshots

  result = compare_screenshots("before.png", "after.png", "diff.png")
  print(f"差異: {result['diff_percent']:.1f}%")
  print(f"Diff 圖: {result['diff_path']}")

CLI:
  python screenshot_diff.py before.png after.png
  python screenshot_diff.py before.png after.png --output diff.png
"""

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# 差異閾值
SIGNIFICANT_THRESHOLD = 5.0  # >5% = 顯著變化


def compare_screenshots(before_path, after_path, diff_path=None):
    """比對兩張截圖，產出差異分析。

    Args:
        before_path: 修復前截圖路徑
        after_path: 修復後截圖路徑
        diff_path: diff 圖輸出路徑（可選，預設 auto）

    Returns:
        dict: {
            "diff_percent": float,     # 差異百分比 0-100
            "diff_path": str | None,   # diff 圖路徑
            "before_size": (w, h),
            "after_size": (w, h),
            "significant": bool,       # 是否顯著變化（>5%）
            "summary": str,            # 人類可讀摘要
        }
    """
    before_path = Path(before_path)
    after_path = Path(after_path)

    if not before_path.exists():
        return _error(f"before 不存在: {before_path}")
    if not after_path.exists():
        return _error(f"after 不存在: {after_path}")

    try:
        from PIL import Image, ImageChops
    except ImportError:
        return _fallback_compare(before_path, after_path)

    img_before = Image.open(before_path).convert("RGB")
    img_after = Image.open(after_path).convert("RGB")

    # 尺寸不同時，resize after 到 before 的尺寸
    if img_before.size != img_after.size:
        img_after = img_after.resize(img_before.size, Image.LANCZOS)

    # 逐像素差異
    diff_img = ImageChops.difference(img_before, img_after)

    # 計算差異百分比
    pixels = list(diff_img.getdata())
    total = len(pixels)
    diff_count = sum(1 for r, g, b in pixels if r + g + b > 30)  # 閾值 30
    diff_percent = (diff_count / total * 100) if total > 0 else 0

    # 產出 diff 圖（差異部分紅色高亮）
    if diff_path is None:
        diff_path = before_path.parent / f"{before_path.stem}_diff.png"
    else:
        diff_path = Path(diff_path)

    # 紅色高亮 diff
    highlight = img_before.copy()
    highlight_pixels = highlight.load()
    diff_pixels = diff_img.load()
    w, h = highlight.size
    for x in range(w):
        for y in range(h):
            r, g, b = diff_pixels[x, y]
            if r + g + b > 30:
                highlight_pixels[x, y] = (255, 0, 0)  # 差異處標紅

    highlight.save(str(diff_path))

    significant = diff_percent > SIGNIFICANT_THRESHOLD
    if diff_percent == 0:
        summary = "完全相同"
    elif significant:
        summary = f"顯著變化（{diff_percent:.1f}%）"
    else:
        summary = f"微小差異（{diff_percent:.1f}%）"

    return {
        "diff_percent": round(diff_percent, 2),
        "diff_path": str(diff_path),
        "before_size": img_before.size,
        "after_size": img_after.size,
        "significant": significant,
        "summary": summary,
    }


def _fallback_compare(before_path, after_path):
    """Pillow 不可用時的 fallback：只比檔案大小。"""
    b_size = before_path.stat().st_size
    a_size = after_path.stat().st_size
    size_diff = abs(b_size - a_size) / max(b_size, a_size) * 100

    return {
        "diff_percent": round(size_diff, 2),
        "diff_path": None,
        "before_size": (0, 0),
        "after_size": (0, 0),
        "significant": size_diff > SIGNIFICANT_THRESHOLD,
        "summary": f"檔案大小差異 {size_diff:.1f}%（Pillow 未安裝，無法做像素對比）",
    }


def _error(msg):
    return {
        "diff_percent": -1,
        "diff_path": None,
        "before_size": (0, 0),
        "after_size": (0, 0),
        "significant": False,
        "summary": f"錯誤: {msg}",
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="截圖對比工具")
    parser.add_argument("before", help="修復前截圖")
    parser.add_argument("after", help="修復後截圖")
    parser.add_argument("--output", "-o", default=None, help="diff 圖輸出路徑")
    args = parser.parse_args()

    result = compare_screenshots(args.before, args.after, args.output)
    print(f"結果: {result['summary']}")
    print(f"差異: {result['diff_percent']}%")
    if result["diff_path"]:
        print(f"Diff 圖: {result['diff_path']}")
