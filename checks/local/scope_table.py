"""Scope table: a document that follows the scope-table shape holds a table the overlap check can read, and every row
says why.

A document is in scope when its `**Shape:**` line links shapes/scope-table.md. A run with no error guarantees, for each:
- a heading `Scope` is followed by a table whose header is `| | What | Why |` (the form scope-overlap reads);
- the first cell of every row is `in`, `later` or `out`, and the rows come in that order, in rows first;
- there is at least one `in` row, and no What or Why cell is empty.
It warns, as a heuristic, on an `out` row with no link in its What or Why and none of the words "others", "nobody" or
"no one": an out row names the member that holds the thing, or says who does it, or that nobody does.
What it cannot decide: whether the rows are true, whether two rows overlap in meaning, or whether a Why is a reason.
Time O(size of the documents).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _shapes import cells, declared, tables  # noqa: E402
from framework.check_api import Finding, files_in_scope, prose_only  # noqa: E402

NAME = "scope-table"
EXACT = True

KINDS = ["in", "later", "out"]
HEADING = re.compile(r"^#{1,6}\s+(.*?)\s*$")
LINK = re.compile(r"\[[^\]]*\]\([^)]+\)|\b(?:others|nobody|no one)\b", re.IGNORECASE)


def check(root: Path, config: dict) -> list[Finding]:
    if "scope_table" not in config:
        return []
    findings = []
    for path in declared(root, files_in_scope(root, config, {".md", ".qmd"}), "scope-table.md"):
        text = prose_only((root / path).read_text(encoding="utf-8", errors="replace"))
        lines = text.splitlines()
        heading = next((n for n, line in enumerate(lines, 1)
                        if (m := HEADING.match(line)) and m.group(1).strip().lower() == "scope"), 0)
        if not heading:
            findings.append(Finding(NAME, path, 1, "no 'Scope' heading"))
            continue
        block = next(((start, rows) for start, rows in tables(text) if start > heading), None)
        if block is None:
            findings.append(Finding(NAME, path, heading, "no table under 'Scope'"))
            continue
        start, rows = block
        header = [cell.lower() for cell in cells(rows[0])]
        if header != ["", "what", "why"]:
            findings.append(Finding(NAME, path, start, f"the header is {header}, not '| | What | Why |'"))
            continue
        rank, kinds = 0, []
        for number, row in enumerate(rows[2:], start + 2):
            parts = cells(row)
            if len(parts) != 3:
                findings.append(Finding(NAME, path, number, f"{len(parts)} cells, not 3"))
                continue
            kind, what, why = parts[0].lower(), parts[1], parts[2]
            kinds.append(kind)
            if kind not in KINDS:
                findings.append(Finding(NAME, path, number, f"the first cell is '{kind}', not in, later or out"))
                continue
            if KINDS.index(kind) < rank:
                findings.append(Finding(NAME, path, number, f"a '{kind}' row after a later kind: order is in, later, out"))
            rank = max(rank, KINDS.index(kind))
            if not what or not why:
                findings.append(Finding(NAME, path, number, f"the {'What' if not what else 'Why'} cell of this '{kind}' row is empty"))
            if kind == "out" and what and why and not LINK.search(what + " " + why):
                findings.append(Finding(NAME, path, number, "an out row names no member that holds it: link it, or say who does or that nobody does", "warning"))
        if "in" not in kinds:
            findings.append(Finding(NAME, path, start, "the table has no 'in' row"))
    return findings
