"""Shared by the local checks: which documents declare which shape, and the tables of a document.

A document follows a shape of this repository when it carries a line `**Shape:**` linking the shape's file, as the
decision records do. A check finds its documents that way. A Shape line inside fenced code, as in a shape's skeleton,
declares nothing. This module has no NAME, so the runner loads it and skips it; a check puts its folder on sys.path
to import it.
"""
from __future__ import annotations

import re
from pathlib import Path

from framework.check_api import prose_only

SHAPE_LINE = re.compile(r"\*\*Shape:\*\*\s*\[[^\]]*\]\(([^)\s]+)\)")


def declared(root: Path, paths: list[str], shape_file: str) -> list[str]:
    """The markdown paths whose Shape line links shapes/<shape_file>."""
    found = []
    for path in paths:
        if not path.endswith((".md", ".qmd")):
            continue
        text = prose_only((root / path).read_text(encoding="utf-8", errors="replace"))
        if any(link.split("#")[0].endswith(f"shapes/{shape_file}") or link.split("#")[0] == shape_file
               for link in SHAPE_LINE.findall(text)):
            found.append(path)
    return found


def cells(line: str) -> list[str]:
    """The cells of a table row, trimmed."""
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def tables(text: str) -> list[tuple[int, list[str]]]:
    """Every table of the text as (line of its first row, its rows as raw lines), blocks of consecutive '|' lines."""
    found, block, start = [], [], 0
    for number, line in enumerate(text.splitlines() + [""], 1):
        if line.lstrip().startswith("|"):
            if not block:
                start = number
            block.append(line)
        elif block:
            found.append((start, block))
            block = []
    return found
