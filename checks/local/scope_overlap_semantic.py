"""Scope overlap, by meaning: two members must not claim the same thing in their "in" rows, even in other words.

The textual check (scope_overlap.py) finds a shared run of words. This one reads the same rows, from the same
checkouts beside this repository, and finds two rows that say the same thing in different words.

What it decides exactly:
- every "What" cell of every member's "in" rows is embedded whole, with the model the standard's meaning tier uses
  (all-MiniLM-L6-v2, through fastembed; vectors are normalised, so a dot product is a cosine);
- two rows of different members whose cosine similarity is at least `threshold` (checks/config.toml, table
  `scope_overlap`, key `semantic_threshold`) give one warning, quoting both rows and their score; the closest pairs
  come first;
- the threshold is PROVISIONAL: it sits between the best score of the known non-overlaps in the tests (0.65) and the
  worst score of the planted paraphrases (0.76), so it separates those fixtures, not the family's future rows;
- members whose README cannot be read are named by the textual check, not repeated here; with fewer than two members
  readable there is nothing to compare, and the check is silent. It sits in the meaning tier: without fastembed it is
  skipped and run.py says so, and a skip is not a pass.

What it cannot decide:
- whether two similar rows are one claim. A high score is a question for the maintainer, as the family's closest pair
  shows: two rows about what the model is handed, one on each side of a line the members may rightly draw;
- a pair below the threshold: a low score is not a proof that nothing overlaps;
- anything but English; a row that is a list of unrelated claims scores low against each of them;
- the "Why" cells, "later" rows and "out" rows, which the textual check leaves out too.

Every finding is a warning, never an error, until the family has judged how often it is right.
Time O(rows) embeddings, O(rows^2) for the similarity matrix.
"""
from __future__ import annotations

import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import scope_overlap as textual  # noqa: E402
from framework.check_api import Finding  # noqa: E402
from meaning import embeddings  # noqa: E402

NAME = "scope-overlap-semantic"
EXACT = False
TIER = "meaning"
available = embeddings.available

DEFAULT_THRESHOLD = 0.70   # PROVISIONAL: see the docstring


def quote(cell: str) -> str:
    """The row as one line, links and markup read as their text."""
    return " ".join(textual.LINK.sub(r"\1", cell).replace("`", "").replace("*", "").split())


def rows_of_family(root: Path, settings: dict) -> list[tuple[str, int, str]]:
    """(member, line in its README, What) for every readable 'in' row of every member checked out beside root."""
    front = (root / settings.get("front_page", "README.md")).read_text(encoding="utf-8", errors="replace")
    found = []
    for name, _ in textual.members_of(front):
        readme = root.parent / name / "README.md"
        if not readme.is_file():
            continue
        rows, _ = textual.in_rows(readme.read_text(encoding="utf-8", errors="replace"))
        found += [(name, line, cell) for line, cell in rows or []]
    return found


def scored_pairs(rows: list[tuple[str, int, str]]) -> list[tuple[float, tuple, tuple]]:
    """Every pair of rows of two different members with its cosine, the closest first."""
    if len({name for name, _, _ in rows}) < 2:
        return []
    vectors = embeddings.embed([quote(cell) for _, _, cell in rows])
    similarity = vectors @ vectors.T
    pairs = [(float(similarity[i, j]), rows[i], rows[j])
             for i, j in combinations(range(len(rows)), 2) if rows[i][0] != rows[j][0]]
    return sorted(pairs, key=lambda pair: -pair[0])


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("scope_overlap", {})
    if not settings:
        return []
    threshold = float(settings.get("semantic_threshold", DEFAULT_THRESHOLD))
    front_name = settings.get("front_page", "README.md")
    return [Finding(NAME, front_name, 0,
                    f"{a[0]} (line {a[1]}) and {b[0]} (line {b[1]}) have 'in' rows of cosine {score:.2f}, "
                    f"at least {threshold:.2f}: \"{quote(a[2])}\" and \"{quote(b[2])}\": "
                    f"one of them owns the claim, the other links it, or the rows differ and say how", "warning")
            for score, a, b in scored_pairs(rows_of_family(root, settings)) if score >= threshold]
