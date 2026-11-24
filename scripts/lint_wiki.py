#!/usr/bin/env python3
"""Executable Wiki Lint Script — 檢查孤島頁面、斷鏈、出處標記、字元上限與衝突註記。"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = ROOT / "wiki"
AGENTS_FILE = ROOT / "AGENTS.md"
INDEX_FILE = WIKI_DIR / "index.md"

errors = []
warnings = []

# 1. Check AGENTS.md character limit (Antigravity <= 12,000 chars)
agents_len = len(AGENTS_FILE.read_text(encoding="utf-8"))
if agents_len > 12000:
    errors.append(f"AGENTS.md exceeds 12,000 chars ({agents_len})")

# 2. Check all wiki pages are linked in index.md (no orphan pages)
index_text = INDEX_FILE.read_text(encoding="utf-8")
all_md = sorted(p for p in WIKI_DIR.rglob("*.md") if p.name != "index.md")
for p in all_md:
    rel = p.relative_to(WIKI_DIR).as_posix()
    if rel not in index_text:
        errors.append(f"Orphan page not linked in wiki/index.md: {rel}")

# 3. Check broken relative markdown links across all wiki pages
link_pat = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
for p in [INDEX_FILE] + all_md:
    text = p.read_text(encoding="utf-8")
    for target in link_pat.findall(text):
        if target.startswith(("http://", "https://", "#")):
            continue
        resolved = (p.parent / target).resolve()
        if not resolved.exists():
            errors.append(f"Broken link in {p.relative_to(ROOT)}: {target}")

# 4. Check source citation coverage ([S1]-[S6]) in concepts/ and syntheses/
src_pat = re.compile(r"\[S[1-6]\]")
for folder in ["concepts", "syntheses"]:
    for p in sorted((WIKI_DIR / folder).glob("*.md")):
        text = p.read_text(encoding="utf-8")
        if not src_pat.search(text):
            errors.append(f"Missing source tag [S1-S6] in {p.relative_to(ROOT)}")

# 5. Check conflict annotations exist
conflict_count = sum(
    1 for p in all_md if "跨來源衝突註記" in p.read_text(encoding="utf-8") or "跨來源差異註記" in p.read_text(encoding="utf-8")
)
if conflict_count < 2:
    warnings.append(f"Expected >=2 conflict/discrepancy annotations, found {conflict_count}")

# 6. Check raw/ has >= 5 sources
raw_count = len(list((ROOT / "raw").glob("*.md")))
if raw_count < 5:
    errors.append(f"raw/ requires >=5 sources, found {raw_count}")

print(f"=== WIKI LINT REPORT ===")
print(f"AGENTS.md length : {agents_len} / 12000 chars")
print(f"Raw sources      : {raw_count} files")
print(f"Wiki pages       : {len(all_md) + 1} files")
print(f"Conflict notes   : {conflict_count} annotated")
print(f"Errors           : {len(errors)}")
for e in errors:
    print(f"  [ERROR] {e}")
for w in warnings:
    print(f"  [WARN]  {w}")

sys.exit(1 if errors else 0)
