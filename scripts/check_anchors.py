#!/usr/bin/env python3
"""Check that translated docs carry explicit English-aligned heading anchors.

For every language other than English (fr, de, es, pt, ...), each heading of
level 2 or more in docs/doc/<lang>/*.md must carry an explicit attr_list
anchor ({ #some-id }) so that cross-page links written against the English
slugs keep working in translations. The level-1 headings, index.md and the
generated print.md are ignored.

Usage:
    python scripts/check_anchors.py            # every language
    python scripts/check_anchors.py fr de       # specific languages
Exit code is 1 if any heading is missing an explicit anchor.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

DOC_DIR = Path(__file__).resolve().parent.parent / "docs" / "doc"

HEADING_RE = re.compile(r"^(#{1,6}) (.+?)(\s*\{[^}]*})?\s*$")


def iter_headings(text: str):
    fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        match = HEADING_RE.match(line)
        if match:
            yield match


def strip_frontmatter(text: str) -> str:
    return re.sub(r"\A---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.DOTALL)


def check_language(lang: str) -> list[str]:
    problems: list[str] = []
    lang_dir = DOC_DIR / lang
    if not lang_dir.is_dir():
        return problems
    for page in sorted(lang_dir.glob("*.md")):
        if page.name in ("print.md", "index.md"):
            continue
        text = strip_frontmatter(page.read_text(encoding="utf-8"))
        for match in iter_headings(text):
            level, title, attr = match.group(1), match.group(2), match.group(3)
            if len(level) == 1:
                continue
            if attr is None or "#" not in attr:
                problems.append(
                    f"{page.relative_to(page.parents[2])}:"
                    f"{'#' * len(level)} {title.strip()}")
    return problems


def main(argv: list[str]) -> int:
    langs = argv[1:]
    if not langs:
        langs = sorted(
            d.name for d in DOC_DIR.iterdir()
            if d.is_dir() and d.name != "en")
    failed = False
    for lang in langs:
        problems = check_language(lang)
        if problems:
            failed = True
            print(f"error: {lang} — headings without an explicit anchor:")
            for problem in problems:
                print(f"  {problem}")
        else:
            print(f"ok: {lang}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
