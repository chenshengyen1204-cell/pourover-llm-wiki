#!/usr/bin/env python3
"""Executable Draft Gate — 在渲染 HTML 前檢查頁數、出處、Wiki 存在性、單頁字數上限與 S2 術語衝突防護。"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRAFTS_DIR = ROOT / "topic-pourover-science" / "drafts"

slides = sorted(DRAFTS_DIR.glob("slide-*.md"))
errors = []

if not (8 <= len(slides) <= 15):
    errors.append(f"Slide count {len(slides)} outside 8-15 range")

wiki_ref_pat = re.compile(r"`(wiki/[^`]+\.md)`")
for s in slides:
    text = s.read_text(encoding="utf-8")
    # 1. Must have Wiki source line
    if "Wiki 出處" not in text:
        errors.append(f"{s.name}: missing 'Wiki 出處'")
    # 2. Referenced wiki file must exist
    refs = wiki_ref_pat.findall(text)
    if not refs:
        errors.append(f"{s.name}: no explicit wiki/*.md path cited")
    for r in refs:
        if not (ROOT / r).exists():
            errors.append(f"{s.name}: cited wiki file does not exist -> {r}")
    # 3. Anti-overflow density check (body chars <= 320 per slide)
    body_chars = len(re.sub(r"\s+", "", text))
    if body_chars > 320:
        errors.append(f"{s.name}: too dense ({body_chars} chars > 320 limit; risk of HTML overflow)")
    # 4. Guard against S2's conflation error ("濾沖 TDS 為 18%–22%")
    if re.search(r"濾沖\s*TDS\s*(為|是|約)\s*18", text):
        errors.append(f"{s.name}: conflated filter TDS with 18-22% Extraction Yield!")

print("=== DRAFT VERIFICATION REPORT ===")
print(f"Slides checked : {len(slides)}")
print(f"Errors         : {len(errors)}")
for e in errors:
    print(f"  [ERROR] {e}")

sys.exit(1 if errors else 0)
