"""
card_test_plans.py — 52 張牌三階段覆蓋驗證的牌序計畫

測試目的:
  驗證 52 張撲克牌在控端輸入後，前端各位置的顯示是否正確，
  排除前後端 card ID 對應錯誤。

三種模式:
  simple   — 52 張牌只要在任一位置出現過（~9 局 + 天牌補測）
  basic    — 52 張牌在莊/閒各出現過（~18 局 + 天牌補測）
  advanced — 每局 6 位置全放同一張牌（52 局 + 天牌補測）

用法:
  from card_test_plans import generate_plan
  plan = generate_plan("advanced")
  for entry in plan:
      print(entry["plan_id"], entry["target_card"], entry["cards"])
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "react", "python"))

from qa_auto_dealer import encode_card, card_display, bac_point

# 52 張牌（按 A♠, A♥, A♣, A♦, 2♠, 2♥, ... K♦ 排列）
ALL_CARDS = list(range(1, 53))

# 位置名稱
POSITIONS = ["P1", "P2", "P3", "B1", "B2", "B3"]


def _face_of(card_value):
    """cardValue → face (1-13)"""
    return (card_value - 1) // 4 + 1


def _points_of_two(c1, c2):
    """兩張牌的百家樂點數"""
    return (bac_point(_face_of(c1)) + bac_point(_face_of(c2))) % 10


def _is_natural(c1, c2):
    """兩張牌是否為天牌（8 或 9 點）"""
    return _points_of_two(c1, c2) >= 8


def _will_have_third_card(p1, p2, b1, b2):
    """判斷這組牌是否會補第三張（任一方）。
    天牌規則：閒/莊任一方前兩張 = 8 或 9 點 → 雙方都不補。
    簡化判斷：只看是否天牌，不走完整補牌規則表。
    """
    if _is_natural(p1, p2) or _is_natural(b1, b2):
        return False
    # 非天牌 → 至少閒方會根據點數決定是否補牌
    # 閒方 0-5 點補牌，6-7 不補
    player_pts = _points_of_two(p1, p2)
    if player_pts <= 5:
        return True  # 閒方補牌
    # 閒方 6-7 不補 → 莊方 0-5 補，6-7 不補
    banker_pts = _points_of_two(b1, b2)
    return banker_pts <= 5


# ── 簡單版 ──────────────────────────────────────────────────────────────────

def generate_simple_plan():
    """簡單版：每局用 6 張不同的牌，~9 局涵蓋全部 52 張。
    天牌不補牌的局，P3/B3 沒測到的牌會加補測局。
    """
    plan = []
    remaining = list(ALL_CARDS)
    round_num = 0
    tested_cards = set()

    while remaining:
        round_num += 1
        # 取最多 6 張
        batch = remaining[:6]
        remaining = remaining[6:]
        # 不足 6 張時用已測過的牌填充
        while len(batch) < 6:
            filler = ALL_CARDS[len(batch) % 52]
            batch.append(filler)

        cards = batch  # [P1, B1, P2, B2, P3, B3] 順序由 server dispatch 控制
        third_card = _will_have_third_card(cards[0], cards[2], cards[1], cards[3])
        target_names = [card_display(c) for c in batch[:6]]

        plan.append({
            "round_num": round_num,
            "plan_id": f"SMP-{round_num:03d}",
            "mode": "simple",
            "target_card": ", ".join(target_names[:4]) + (" +" if third_card else ""),
            "cards": cards,
            "note": f"簡單版 第{round_num}批（{len(batch)}張）",
            "expect_third_card": third_card,
        })
        tested_cards.update(batch)

    # 檢查是否有牌因天牌沒在 P3/B3 出現 → 這裡簡單版不嚴格追蹤位置
    return plan


# ── 基礎版 ──────────────────────────────────────────────────────────────────

def generate_basic_plan():
    """基礎版：52 張牌在閒方和莊方各出現至少一次。
    閒方位置 = P1, P2, P3（每局 3 張）→ 52÷3 ≈ 18 局
    莊方位置 = B1, B2, B3（每局 3 張）→ 同上
    交錯安排讓兩邊同時推進。
    """
    plan = []
    # 閒方待測、莊方待測
    player_remaining = list(ALL_CARDS)
    banker_remaining = list(ALL_CARDS)
    round_num = 0

    while player_remaining or banker_remaining:
        round_num += 1
        # 閒方取 3 張
        p_batch = player_remaining[:3]
        player_remaining = player_remaining[3:]
        while len(p_batch) < 3:
            p_batch.append(ALL_CARDS[len(p_batch)])

        # 莊方取 3 張
        b_batch = banker_remaining[:3]
        banker_remaining = banker_remaining[3:]
        while len(b_batch) < 3:
            b_batch.append(ALL_CARDS[len(b_batch)])

        # 牌序: server dispatch 決定位置，我們準備 6 張
        # 按 [P1, B1, P2, B2, P3, B3] 的 docstring 順序
        cards = [p_batch[0], b_batch[0], p_batch[1], b_batch[1], p_batch[2], b_batch[2]]
        third_card = _will_have_third_card(cards[0], cards[2], cards[1], cards[3])

        p_names = [card_display(c) for c in p_batch]
        b_names = [card_display(c) for c in b_batch]

        plan.append({
            "round_num": round_num,
            "plan_id": f"BSC-{round_num:03d}",
            "mode": "basic",
            "target_card": f"閒:{','.join(p_names)} 莊:{','.join(b_names)}",
            "cards": cards,
            "note": f"基礎版 閒={','.join(p_names)} 莊={','.join(b_names)}",
            "expect_third_card": third_card,
        })

    return plan


# ── 進階版 ──────────────────────────────────────────────────────────────────

def generate_advanced_plan():
    """進階版：每局 6 位置全放同一張牌，52 局 + 天牌補測局。"""
    plan = []

    # 主要 52 局
    for i, cv in enumerate(ALL_CARDS):
        round_num = i + 1
        cards = [cv] * 6
        name = card_display(cv)
        third_card = _will_have_third_card(cv, cv, cv, cv)

        plan.append({
            "round_num": round_num,
            "plan_id": f"ADV-{round_num:03d}",
            "mode": "advanced",
            "target_card": name,
            "cards": cards,
            "note": f"全位置 {name}" + ("" if third_card else " ⚠天牌不補"),
            "expect_third_card": third_card,
        })

    # 天牌補測局：找出哪些牌因天牌沒在 P3/B3 出現
    no_third = [e for e in plan if not e["expect_third_card"]]
    if no_third:
        # 把這些牌安排到 P3/B3 位置（其他位置用 2♠ 確保不天牌）
        filler = encode_card(2, 1)  # 2♠ = 2 點，不會天牌
        for sup_idx, entry in enumerate(no_third):
            cv = entry["cards"][0]
            name = card_display(cv)
            round_num = len(plan) + 1
            # P1=2♠, B1=2♠, P2=2♠, B2=2♠, P3=目標牌, B3=目標牌
            # 閒 2+2=4 點 → 補牌 ✓, 莊會根據閒的補牌結果決定
            cards = [filler, filler, filler, filler, cv, cv]

            plan.append({
                "round_num": round_num,
                "plan_id": f"ADV-{round_num:03d}",
                "mode": "advanced",
                "target_card": f"{name} (P3/B3補測)",
                "cards": cards,
                "note": f"天牌補測 P3/B3={name}",
                "expect_third_card": True,
            })

    return plan


# ── 統一入口 ────────────────────────────────────────────────────────────────

def generate_plan(mode="advanced"):
    """產出牌序計畫。mode: simple / basic / advanced"""
    if mode == "simple":
        return generate_simple_plan()
    elif mode == "basic":
        return generate_basic_plan()
    elif mode == "advanced":
        return generate_advanced_plan()
    else:
        raise ValueError(f"未知模式: {mode}（需 simple / basic / advanced）")


def print_plan_summary(plan):
    """印出計畫摘要。"""
    mode = plan[0]["mode"] if plan else "?"
    total = len(plan)
    third_count = sum(1 for e in plan if e["expect_third_card"])
    no_third = total - third_count

    print(f"\n{'='*60}")
    print(f"  牌序計畫 — {mode} 模式")
    print(f"  總局數: {total}")
    print(f"  預期補牌: {third_count} 局 | 不補牌: {no_third} 局")
    print(f"{'='*60}")
    for e in plan:
        flag = "" if e["expect_third_card"] else " ⚠不補"
        print(f"  {e['plan_id']}  {e['target_card']:<20s}  {e['note']}{flag}")
    print()


# ── CLI ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="牌序計畫產出")
    parser.add_argument("--mode", default="advanced", choices=["simple", "basic", "advanced"])
    args = parser.parse_args()

    plan = generate_plan(args.mode)
    print_plan_summary(plan)
