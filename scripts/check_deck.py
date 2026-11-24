#!/usr/bin/env python3
"""Executable Deck Gate — 驗證渲染後的 HTML 簡報頁數、每頁出處、Wiki 頁面存在性、外部連結完整性與單頁文字密度。"""
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
DECK_PATH = ROOT / "topic-pourover-science" / "deck.html"

if not DECK_PATH.exists():
    print("[ERROR] deck.html not found")
    sys.exit(1)

soup = BeautifulSoup(DECK_PATH.read_text(encoding="utf-8"), "html.parser")
slides = soup.select("section.slide")
errors = []

if not (8 <= len(slides) <= 15):
    errors.append(f"Slide count {len(slides)} outside 8-15 range")

wiki_pat = re.compile(r"wiki/[a-zA-Z0-9_./-]+\.md")
for idx, slide in enumerate(slides, 1):
    footer = slide.select_one(".slide-source")
    if not footer:
        errors.append(f"Slide {idx}: missing .slide-source attribution footer")
    else:
        ftext = footer.get_text(" ", strip=True)
        refs = wiki_pat.findall(ftext)
        if not refs:
            errors.append(f"Slide {idx}: footer missing wiki/*.md path")
        for r in refs:
            if not (ROOT / r).exists():
                errors.append(f"Slide {idx}: cited wiki path does not exist -> {r}")
        links = footer.select("a[href^='https://']")
        if not links:
            errors.append(f"Slide {idx}: footer missing clickable https:// source link")

    # Anti-overflow text density check on rendered slide text
    visible_text = re.sub(r"\s+", "", slide.get_text())
    if len(visible_text) > 520:
        errors.append(f"Slide {idx}: rendered text too dense ({len(visible_text)} chars > 520)")

print("=== HTML DECK VERIFICATION REPORT ===")
print(f"Slides rendered : {len(slides)}")
print(f"Errors          : {len(errors)}")
for e in errors:
    print(f"  [ERROR] {e}")

sys.exit(1 if errors else 0)
