"""
screenshot_validator.py — Screenshot deduplication validator (zero token cost)

Detects duplicate screenshots across different pages/labels.
Uses PIL pixel-level diff (via screenshot_diff.py) — no AI/API calls needed.

Problem solved:
  When AI context is nearly full, it marks screenshots as PASS just because
  they were captured, without verifying content differs between pages.
  This validator catches identical screenshots that should be different.

Usage:
  from shared.ai.screenshot_validator import validate_screenshot_set

  report = validate_screenshot_set("screenshots/")
  if report["status"] == "FAIL":
      print(f"Duplicates found: {len(report['duplicates'])}")

CLI:
  python screenshot_validator.py --dir screenshots/
  python screenshot_validator.py --dir screenshots/ --threshold 15 --skip-step 3
"""

import json
import re
import sys
from itertools import combinations
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# --- Thresholds ---
IDENTITY_THRESHOLD = 1.0       # diff% below this = "effectively identical"
PAIR_COUNT_THRESHOLD = 15      # unique labels <= this: compare all pairs
SKIP_STEP_MEDIUM = 3           # 16-30 labels: sample every 3rd distant pair
SKIP_STEP_LARGE = 5            # >30 labels: sample every 5th distant pair
MAX_COMPARISONS = 30           # hard cap on comparison count


def validate_screenshot_set(screenshot_dir, threshold=None, skip_step=None):
    """Validate that screenshots with different labels are actually different.

    Args:
        screenshot_dir: Directory containing screenshot files
        threshold: Override PAIR_COUNT_THRESHOLD (optional)
        skip_step: Override skip step for sampling (optional)

    Returns:
        dict with status, duplicates, and comparison stats
    """
    screenshot_dir = Path(screenshot_dir)
    if not screenshot_dir.exists():
        return _report("WARN", 0, 0, 0, [],
                        "Screenshot directory does not exist")

    # Collect and group screenshots by label
    screenshots = _collect_screenshots(screenshot_dir)
    if len(screenshots) <= 1:
        return _report("PASS", len(screenshots), len(screenshots), 0, [],
                        "Single or no screenshots — nothing to compare")

    # Group by label
    labels = sorted(set(s["label"] for s in screenshots))
    if len(labels) <= 1:
        return _report("PASS", len(screenshots), 1, 0, [],
                        "All screenshots share the same label")

    # Pick one representative per label (latest timestamp)
    representatives = _pick_representatives(screenshots, labels)

    # Build comparison pairs based on count
    effective_threshold = threshold or PAIR_COUNT_THRESHOLD
    pairs = _build_pairs(representatives, labels, effective_threshold,
                         skip_step)

    # Run comparisons
    duplicates = []
    comparisons_made = 0

    for label_a, label_b in pairs:
        path_a = representatives[label_a]
        path_b = representatives[label_b]
        diff_pct = _quick_diff(path_a, path_b)
        comparisons_made += 1

        if diff_pct is not None and diff_pct < IDENTITY_THRESHOLD:
            duplicates.append({
                "screenshot_a": Path(path_a).name,
                "screenshot_b": Path(path_b).name,
                "label_a": label_a,
                "label_b": label_b,
                "diff_percent": round(diff_pct, 2),
                "verdict": "DUPLICATE_SUSPECT",
            })

    status = "FAIL" if duplicates else "PASS"
    summary = (f"{len(duplicates)} duplicate pairs found among {len(labels)} "
               f"unique pages" if duplicates else
               f"All {len(labels)} pages are visually distinct")

    return _report(status, len(screenshots), len(labels),
                   comparisons_made, duplicates, summary)


def _collect_screenshots(directory):
    """Scan directory for screenshot files and parse metadata from filenames."""
    screenshots = []
    patterns = [
        # testcase{id}_{label}_{timestamp}.png
        re.compile(
            r"testcase(\d+)_(.+?)_(\d{8,14})\.png", re.IGNORECASE),
        # {label}_{timestamp}.png
        re.compile(
            r"(.+?)_(\d{8,14})\.png", re.IGNORECASE),
        # {flow}_{timestamp}.png (ADB style)
        re.compile(
            r"(.+?)_(\d+)\.png", re.IGNORECASE),
    ]

    for f in sorted(directory.glob("*.png")):
        if f.stat().st_size < 1024:  # skip < 1KB (likely broken)
            continue

        parsed = False
        for pat in patterns:
            m = pat.match(f.name)
            if m:
                groups = m.groups()
                if len(groups) == 3:
                    label = groups[1]
                    timestamp = groups[2]
                elif len(groups) == 2:
                    label = groups[0]
                    timestamp = groups[1]
                else:
                    continue
                screenshots.append({
                    "path": str(f),
                    "label": label.lower().strip(),
                    "timestamp": timestamp,
                })
                parsed = True
                break

        if not parsed:
            # Use filename stem as label
            screenshots.append({
                "path": str(f),
                "label": f.stem.lower().strip(),
                "timestamp": "0",
            })

    return screenshots


def _pick_representatives(screenshots, labels):
    """Pick one screenshot per label (latest timestamp)."""
    reps = {}
    for label in labels:
        candidates = [s for s in screenshots if s["label"] == label]
        best = max(candidates, key=lambda s: s["timestamp"])
        reps[label] = best["path"]
    return reps


def _build_pairs(representatives, labels, threshold, skip_step_override):
    """Build comparison pairs with sampling strategy."""
    n = len(labels)
    if n <= threshold:
        # Compare all unique pairs
        return list(combinations(labels, 2))

    # Over threshold: adjacent + sampled distant pairs
    pairs = []

    # 1. Always compare consecutive neighbors (catches navigation failures)
    for i in range(n):
        j = (i + 1) % n
        pairs.append((labels[i], labels[j]))

    # 2. Sample distant pairs
    step = skip_step_override or (SKIP_STEP_MEDIUM if n <= 30
                                   else SKIP_STEP_LARGE)
    all_combos = list(combinations(labels, 2))
    # Remove already-added adjacent pairs
    adjacent_set = set(pairs)
    distant = [p for p in all_combos if p not in adjacent_set]
    sampled = distant[::step]

    pairs.extend(sampled)

    # Cap total comparisons
    if len(pairs) > MAX_COMPARISONS:
        pairs = pairs[:MAX_COMPARISONS]

    return pairs


def _quick_diff(path_a, path_b):
    """Get diff percentage between two screenshots. Returns None on error."""
    try:
        from shared.ai.screenshot_diff import compare_screenshots
        result = compare_screenshots(path_a, path_b)
        if result["diff_percent"] >= 0:
            return result["diff_percent"]
    except ImportError:
        # Fallback: direct PIL comparison
        try:
            from PIL import Image, ImageChops
            img_a = Image.open(path_a).convert("RGB")
            img_b = Image.open(path_b).convert("RGB")
            if img_a.size != img_b.size:
                img_b = img_b.resize(img_a.size, Image.LANCZOS)
            diff = ImageChops.difference(img_a, img_b)
            pixels = list(diff.getdata())
            total = len(pixels)
            diff_count = sum(1 for r, g, b in pixels if r + g + b > 30)
            return (diff_count / total * 100) if total > 0 else 0
        except Exception:
            pass
    except Exception:
        pass
    return None


def _report(status, total, unique_labels, comparisons, duplicates, summary):
    """Build structured validation report."""
    return {
        "status": status,
        "total_screenshots": total,
        "unique_labels": unique_labels,
        "comparisons_made": comparisons,
        "duplicates": duplicates,
        "summary": summary,
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Screenshot deduplication validator")
    parser.add_argument("--dir", "-d", required=True,
                        help="Screenshot directory to validate")
    parser.add_argument("--threshold", "-t", type=int, default=None,
                        help=f"Pair count threshold (default: {PAIR_COUNT_THRESHOLD})")
    parser.add_argument("--skip-step", "-s", type=int, default=None,
                        help="Skip step for sampling when over threshold")
    parser.add_argument("--pretty", action="store_true",
                        help="Pretty-print JSON output")
    args = parser.parse_args()

    report = validate_screenshot_set(args.dir, args.threshold, args.skip_step)
    indent = 2 if args.pretty else None
    print(json.dumps(report, ensure_ascii=False, indent=indent))
    sys.exit(0 if report["status"] != "FAIL" else 1)
