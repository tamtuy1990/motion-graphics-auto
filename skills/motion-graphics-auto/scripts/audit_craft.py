#!/usr/bin/env python3
"""Chấm "tay nghề dựng" của một beat-plan — bù chỗ `slideshow_risk.py` không thấy.

VÌ SAO CẦN: `slideshow_risk.py` chỉ đo event dài/ngắn và khoảng trống. Nó KHÔNG
thấy được năm lỗi đã ship thật trong job faceless:

  1. Lặp một công thức  — 47% event cùng một dạng, toạ độ lặp y hệt
  2. Không có B-roll    — chỉ một tuyến nền phẳng
  3. Rải accent         — nhiều màu nhấn cùng frame
  4. Nhịp đều tăm tắp   — độ lệch chuẩn độ dài cảnh gần 0
  5. Không có state     — mỗi graphic hiện ra rồi biến mất, không gì tồn tại

Năm lỗi đó qua được mọi validator. Script này đo chúng.

Chạy:
  python audit_craft.py --board _hf/beat-plan.json
  python audit_craft.py --board _hf/beat-plan.json --report _hf/craft-report.json
  python audit_craft.py --board plan.json --max-score 0.5    # exit 1 nếu vượt
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

# Dạng hình "có chuyển động thật" — dùng để đo đa dạng cơ chế.
MOTION_FAMILIES = {
    "counter-v1": "count", "counter-signed-v1": "count", "counter-confetti": "count",
    "bar-chart-v1": "bars", "bar-race-v1": "bars", "scale-bars": "bars",
    "debt-stack-v1": "stack", "ratio-discs-v1": "discs",
    "timeline-v1": "time", "trend-v1": "line", "timeline-v2": "time",
    "escalation-v1": "line", "step-chart": "bars",
    "flow-v1": "flow", "price-compare-v1": "stamp", "price-stamp": "stamp",
    "pictogram-v1": "people", "pictogram": "people", "icons-wiggle-v1": "people",
    "chapter-v1": "intertitle", "neon-callout-v1": "callout",
    "state-board": "state", "ranking-v1": "state",
    "location-card": "footage",
    "quote-card": "quote", "quote-light": "quote",
    "compare-cards": "compare", "split-stage": "compare",
    "before-after-slider-scrub": "compare",
    "banner-v1": "text", "callout-v1": "text", "infographic-v1": "text",
    "steps-v1": "text", "headline-banner": "text",
}

# Dạng "chỉ hiện chữ ra" — nếu chiếm quá nhiều thì đang đi theo công thức.
TEXT_ONLY = {"banner-v1", "callout-v1", "infographic-v1", "steps-v1", "headline-banner"}


def load(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8-sig"))


def analyse(board: dict, fps: float = 30.0) -> dict:
    ev = board.get("events", [])
    if not ev:
        return {"score": 1.0, "level": "critical",
                "reasons": ["không có event nào"], "samples": {}}

    ordered = sorted(ev, key=lambda e: e.get("startFrame", 0))
    n = len(ordered)
    reasons: list[str] = []

    # --- 1. lặp một công thức ------------------------------------------------
    counts = Counter(e.get("template", "") for e in ordered)
    top_t, top_n = counts.most_common(1)[0]
    top_share = top_n / n

    # Nhóm chức năng: đổi template nhưng giữ chức năng = vẫn lặp.
    fam = Counter(MOTION_FAMILIES.get(e.get("template", ""), "other") for e in ordered)
    top_f, top_fn = fam.most_common(1)[0]
    fam_share = top_fn / n

    if top_share > 0.30:
        reasons.append(
            "%d/%d event dùng cùng `%s` (%.0f%%) — lặp template máy móc"
            % (top_n, n, top_t, top_share * 100)
        )
    if fam_share > 0.45:
        reasons.append(
            "%d/%d event cùng NHÓM chức năng `%s` (%.0f%%) — đổi tên nhưng không "
            "đổi cách kể" % (top_fn, n, top_f, fam_share * 100)
        )

    text_share = sum(1 for e in ordered if e.get("template") in TEXT_ONLY) / n
    if text_share > 0.5:
        reasons.append(
            "%.0f%% event chỉ là 'chữ đặt lên màn hình' — hình không mang nghĩa"
            % (text_share * 100)
        )

    # --- 2. toạ độ lặp ------------------------------------------------------
    # MIỄN TRỪ: `location-card` CỐ Ý luôn nằm cùng một góc — đó là card định danh
    # của chế độ "footage tự nói", đặt cùng chỗ để thành ngôn ngữ nhất quán
    # (đúng như ảnh tham chiếu: card nguồn luôn ở góc trên trái). Lặp toạ độ của
    # nó KHÔNG phải lỗi. Chỉ tính toạ độ lặp của các dạng còn lại.
    FIXED_POS = {"location-card"}
    pos = Counter()
    for e in ordered:
        if e.get("template") in FIXED_POS:
            continue
        b = e.get("box") or {}
        if b:
            pos[(round(b.get("x", 0), 2), round(b.get("y", 0), 2))] += 1
    worst_pos, worst_n = (pos.most_common(1)[0] if pos else ((0, 0), 0))
    if worst_n >= 3:
        reasons.append(
            "toạ độ (x=%.2f y=%.2f) dùng %d lần — mọi graphic nằm cùng một chỗ"
            % (worst_pos[0], worst_pos[1], worst_n)
        )

    # --- 3. đa dạng chức năng -----------------------------------------------
    distinct_fam = len(fam)
    if distinct_fam < 4:
        reasons.append(
            "chỉ %d nhóm chức năng khác nhau — cần ít nhất 4 cách kể" % distinct_fam
        )

    # --- 4. nhịp: độ lệch chuẩn độ dài cảnh ---------------------------------
    durs = [(e.get("endFrame", 0) - e.get("startFrame", 0)) / fps for e in ordered]
    durs = [d for d in durs if d > 0]
    cv = 0.0
    if len(durs) >= 3:
        mean = statistics.mean(durs)
        sd = statistics.pstdev(durs)
        cv = sd / mean if mean else 0.0
        if cv < 0.28:
            reasons.append(
                "độ dài cảnh rất đều (CV=%.2f, trung bình %.1fs) — nhịp là hằng số, "
                "không đổi theo nội dung" % (cv, mean)
            )

    # --- 5. state xuyên cảnh ------------------------------------------------
    state_n = sum(1 for e in ordered if MOTION_FAMILIES.get(e.get("template")) == "state")
    reused = {}
    for e in ordered:
        reused.setdefault(e.get("template"), 0)
        reused[e.get("template")] += 1
    if state_n == 0:
        reasons.append(
            "không có cơ chế STATE nào — mỗi graphic hiện ra rồi biến mất; "
            "không có gì tồn tại và tiến hoá qua nhiều cảnh"
        )

    # --- 6. footage sạch ----------------------------------------------------
    footage_n = sum(1 for e in ordered
                    if MOTION_FAMILIES.get(e.get("template")) == "footage")
    # Cộng cả khoảng trống giữa các event: đó cũng là lúc footage tự nói.
    span = sum(durs)
    total = 0.0
    canvas = board.get("canvas") or {}
    if board.get("scope"):
        total = sum((e.get("endFrame", 0) - e.get("startFrame", 0)) / fps for e in ordered)
    covered = span
    dur_total = (canvas.get("durationFrames") or 0) / fps
    if dur_total:
        clean_share = max(0.0, (dur_total - covered) / dur_total)
        if clean_share < 0.20 and footage_n == 0:
            reasons.append(
                "chỉ %.0f%% thời lượng là footage sạch (không graphic) — cần ≥25%% "
                "để video có nhịp thở; bản ship hỏng có 0%%"
                % (clean_share * 100)
            )

    # --- 7. accent: đếm event khai nhiều hơn một accent ---------------------
    multi_accent = 0
    for e in ordered:
        p = e.get("props") or {}
        acc = 0
        for k in ("items", "bars", "entries", "groups"):
            for it in (p.get(k) or []):
                if isinstance(it, dict) and it.get("accent"):
                    acc += 1
        if acc > 1:
            multi_accent += 1
    if multi_accent:
        reasons.append(
            "%d event có nhiều hơn MỘT accent cùng lúc — luật là một màu nhấn mỗi frame"
            % multi_accent
        )

    # --- 8. không có bằng chứng đã nhìn frame ------------------------------
    has_why = sum(1 for e in ordered if e.get("_why") or e.get("why"))
    if has_why == 0:
        reasons.append(
            "không event nào có `why` — thiếu lý do cho hình; đây là dấu hiệu "
            "chọn hình theo thói quen thay vì theo nghĩa câu thoại"
        )

    # --- 9. mức sáng tạo ---------------------------------------------------
    # `editorial-craft.md` cho một BẢNG TRA cơ chế (mức A). Dùng bảng cho cả
    # video thì vẫn nhàm, dù đã "đa dạng". `inventing-visuals.md` nói mục tiêu:
    # 70% A / 25% B / 5% C — tức 1-2 đoạn được nghĩ riêng.
    # Không đo được "chất" của một ý tưởng bằng code. Nhưng ĐO ĐƯỢC dấu hiệu:
    # event nào không tra được từ bảng (dạng mới), và event nào kế thừa state
    # từ event trước (đối tượng đổi trạng thái thay vì dựng lại).
    KNOWN = set(MOTION_FAMILIES.keys())
    invented = [e for e in ordered if e.get("template") not in KNOWN]

    # State kế thừa: cùng một đối tượng/chủ đề xuất hiện ở >=2 event, và event
    # sau mang `continues` trỏ về event trước.
    inherits = [e for e in ordered if e.get("continues")]
    reuses = {}
    for e in ordered:
        key = (e.get("props") or {}).get("subject") or (e.get("props") or {}).get("title")
        if key:
            reuses[key] = reuses.get(key, 0) + 1
    repeated_subjects = {k: v for k, v in reuses.items() if v >= 2}

    n_events = len(ordered)
    if n_events >= 8:
        if not invented and not inherits:
            reasons.append(
                "không có event nào ở mức B/C — mọi hình đều tra được từ bảng cơ "
                "chế; mục tiêu là 1-2 đoạn được nghĩ riêng (xem inventing-visuals.md)"
            )
        # Đối tượng lặp mà không kế thừa state = dựng lại từ đầu mỗi lần.
        if repeated_subjects and not inherits:
            worst = max(repeated_subjects.items(), key=lambda kv: kv[1])
            reasons.append(
                "chủ đề '%s' xuất hiện %d lần nhưng không event nào kế thừa trạng "
                "thái trước — đối tượng nên ĐỔI TRẠNG THÁI, không dựng lại"
                % (worst[0], worst[1])
            )

    # --- 10. lớp biến đổi (bản quyền / reused content) ---------------------
    # Với faceless, mỗi hình phải qua >= 2 lớp biến đổi — không phải chuyện thẩm
    # mỹ mà là điều kiện để video không bị đánh reused content. Xem
    # faceless-transform.md. `transforms` là mảng tên lớp:
    # reframe | motion | grade | overlay | recompose | reuse
    VALID_TF = {"reframe", "motion", "grade", "overlay", "recompose", "reuse"}
    thin = []
    combos = Counter()
    for e in ordered:
        tf = [t for t in (e.get("transforms") or []) if t in VALID_TF]
        if len(tf) < 2:
            thin.append(e.get("id", "?"))
        if tf:
            combos[tuple(sorted(tf))] += 1
    if thin:
        reasons.append(
            "%d/%d hình có < 2 lớp biến đổi (%s) — mỗi hình phải qua ít nhất 2 lớp "
            "để tránh bị đánh reused content; 'để footage tự nói' KHÔNG có nghĩa là "
            "ảnh gốc nguyên bản"
            % (len(thin), n, ", ".join(thin[:5]))
        )
    combo_share = 0.0
    if combos:
        _, cn = combos.most_common(1)[0]
        combo_share = cn / n
        if combo_share > 0.40 and n >= 5:
            reasons.append(
                "tổ hợp lớp biến đổi lặp %.0f%% — mọi hình đi qua cùng một công thức "
                "xử lý, dễ bị nhận ra là sản xuất hàng loạt" % (combo_share * 100)
            )
    if not combos:
        reasons.append(
            "không event nào khai `transforms` — chưa xét yêu cầu biến đổi tài sản; "
            "xem faceless-transform.md"
        )

    # --- điểm ---------------------------------------------------------------
    score = 0.0
    if top_share > 0.30:
        score += min(0.22, 0.22 * (top_share - 0.30) / 0.30)
    if fam_share > 0.45:
        score += min(0.18, 0.18 * (fam_share - 0.45) / 0.30)
    if text_share > 0.5:
        score += min(0.16, 0.16 * (text_share - 0.5) / 0.3)
    if worst_n >= 3:
        score += min(0.10, 0.03 * (worst_n - 2))
    if distinct_fam < 4:
        score += 0.12 * (4 - distinct_fam) / 4
    if cv and cv < 0.28:
        score += min(0.12, 0.12 * (0.28 - cv) / 0.28)
    if state_n == 0:
        score += 0.10
    if footage_n == 0:
        score += 0.08
    if multi_accent:
        score += min(0.08, 0.04 * multi_accent)
    if has_why == 0:
        score += 0.06
    if n_events >= 8:
        if not invented and not inherits:
            score += 0.10
        if repeated_subjects and not inherits:
            score += 0.06
    # Biến đổi tài sản: hình mỏng hoặc dùng một công thức xử lý.
    if thin:
        score += min(0.14, 0.14 * len(thin) / max(1, n))
    if combo_share > 0.40 and n >= 5:
        score += min(0.08, 0.08 * (combo_share - 0.40) / 0.35)
    if not combos:
        score += 0.08
    score = max(0.0, min(1.0, score))
    level = ("good" if score < 0.20 else
             "medium" if score < 0.45 else
             "poor" if score < 0.7 else "critical")

    return {
        "score": round(score, 3),
        "level": level,
        "reasons": reasons,
        "samples": {
            "events": n,
            "top_template": "%s x%d (%.0f%%)" % (top_t, top_n, top_share * 100),
            "top_family": "%s x%d (%.0f%%)" % (top_f, top_fn, fam_share * 100),
            "distinct_families": distinct_fam,
            "families": dict(fam.most_common()),
            "duration_cv": round(cv, 3),
            "state_events": state_n,
            "footage_clean_events": footage_n,
            "events_with_why": has_why,
            "multi_accent_events": multi_accent,
            "invented_events": len(invented),
            "events_inheriting_state": len(inherits),
            "repeated_subjects": repeated_subjects,
            "thin_transform_events": len(thin),
            "top_transform_combo_share": round(combo_share, 2),
            "events_declaring_transforms": sum(1 for e in ordered if e.get("transforms")),
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--board", required=True, type=Path)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--report", type=Path, help="ghi JSON (UTF-8) ra file này")
    ap.add_argument("--max-score", type=float, default=0.45,
                    help="ngưỡng fail (mặc định 0.45 = medium)")
    ap.add_argument("--fps", type=float, default=30.0)
    a = ap.parse_args()

    board = load(a.board)
    r = analyse(board, a.fps)

    if a.report:
        a.report.parent.mkdir(parents=True, exist_ok=True)
        a.report.write_text(
            json.dumps({"board": str(a.board), **r}, ensure_ascii=False, indent=1),
            encoding="utf-8")
        print("đã ghi %s" % a.report)

    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
    elif not a.report:
        print("tay nghề dựng : %.2f  (%s)" % (r["score"], r["level"]))
        print()
        for k, v in r["samples"].items():
            print("  %-22s %s" % (k, v))
        if r["reasons"]:
            print()
            print("VẤN ĐỀ:")
            for x in r["reasons"]:
                print("  -", x)
        else:
            print()
            print("Không thấy dấu hiệu đi theo công thức.")

    if r["score"] > a.max_score:
        print()
        print("FAIL: %.2f > %.2f. Sửa: đa dạng cơ chế, đổi bố cục, thêm nhịp "
              "nhiều mức, thêm state, để footage tự nói, một accent mỗi frame."
              % (r["score"], a.max_score))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
