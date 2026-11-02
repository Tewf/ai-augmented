"""Scope overlap: two members of the family must not claim the same thing in their "in" rows.

The members are the repositories linked in the first column of the front page's member table. Each one's README
has a `## Scope` section with a table `| | What | Why |`; its rows whose first cell is `in` are what the member
claims. The check reads those README files from checkouts beside this repository (a folder named like the member)
and warns when two members share a noun phrase of `min_words` words or more (default 3) in the "What" cells.

What it decides exactly:
- the "What" cell is cut into runs of words, at punctuation (comma, colon, semicolon, full stop, brackets, bar, dash)
  and at function words (articles, prepositions, conjunctions, pronouns, auxiliaries, a short list in this file),
  except "of", which may join two words ("tree of topics"); possessives are dropped;
- each run of `min_words` or more words is a noun phrase candidate; words are lowercased and a final plural "s" is
  dropped;
- two members share a phrase when the same `min_words` consecutive words occur in a candidate of each; the
  overlapping phrases of one pair are merged into the longest run, and one warning names the pair, the phrase and the
  row of each member (heuristic);
- a member whose README is missing, whose scope table has another shape, or that has no "in" row is reported by name,
  so a table that cannot be read is never taken for a table with no overlap;
- with fewer than two member checkouts present there is nothing to compare: the check is silent. CI clones every
  member and runs it alone, so silence on a developer's machine is not a pass.

What it cannot decide:
- meaning: two rows may say the same thing in different words (no shared phrase), or share a phrase and say
  different things ("tree of topics" in a row that includes it and in one that excludes it; only "in" rows are read,
  but "in" does not say how much);
- the "Why" cells, "later" rows and "out" rows, which are not claims on the member's own scope;
- grammar: a run of words between two function words is not always a noun phrase;
- anything but English.

Every finding is a warning, never an error, until the family has judged how often it is right.
Time O(total words * min_words) for the phrases, O(members^2 * phrases) for the pairs.
"""
from __future__ import annotations

import re
from itertools import combinations
from pathlib import Path

from framework.check_api import Finding

NAME = "scope-overlap"
EXACT = False

MEMBER_LINK = re.compile(r"\[([^\]]+)\]\(https://github\.com/[^/\s)]+/([^/\s)]+)\)")
HEADING = re.compile(r"^#{1,6}\s+(.*?)\s*$")
LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
BREAK = re.compile(r"[,;:.()\[\]|!?\"—–]|\s-\s")
WORD = re.compile(r"[^\W_]+(?:'[^\W_]+)?")
FUNCTION_WORDS = frozenset("""
a an the this that these those it its their his her our your my
and or but nor so yet if then else than as while when where which who whom whose what why how
of in on at by for with without from to into onto over under between among about against through during
is are was were be been being am do does did done has have had having can could may might must shall should will would
not no each every any all some one two more most less least much many other such own same only also both either
there here we you they he she them us me i
""".split())


def words_of(text: str) -> list[str]:
    """Lowercase words with a final plural 's' dropped, so 'checker' and 'checkers' meet."""
    found = []
    for word in WORD.findall(text.lower()):
        if len(word) > 4 and word.endswith("ies"):
            word = word[:-3] + "y"
        elif len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
            word = word[:-1]
        found.append(word)
    return found


def candidates(cell: str, min_words: int) -> list[list[str]]:
    """The runs of `min_words` or more words between punctuation and function words; 'of' may join two words."""
    clean = LINK.sub(r"\1", cell).replace("`", "").replace("*", "")
    clean = re.sub(r"['\u2019]s\b|(?<=s)['\u2019]", "", clean)   # possessives: "checker's" is "checker"
    runs = []

    def flush(run: list[str]) -> None:
        while run and run[-1] == "of":
            run.pop()
        runs.append(run)

    for segment in BREAK.split(clean):
        run: list[str] = []
        for raw in WORD.findall(segment.lower()):
            if raw == "of" and run:
                run.append("of")
            elif raw in FUNCTION_WORDS:
                flush(run)
                run = []
            else:
                run += words_of(raw)
        flush(run)
    return [run for run in runs if len(run) >= min_words]


def members_of(front: str) -> list[tuple[str, int]]:
    """The repository names linked in the first column of the front page's member table, with their line."""
    found, inside = [], False
    for number, line in enumerate(front.splitlines(), 1):
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if line.lstrip().startswith("|") and cells and cells[0].lower() == "member":
            inside = True
            continue
        if inside and not line.lstrip().startswith("|"):
            break
        match = MEMBER_LINK.search(cells[0]) if inside and cells else None
        if match:
            found.append((match.group(2), number))
    return found


def in_rows(readme: str) -> tuple[list[tuple[int, str]] | None, str]:
    """The (line, What) of every 'in' row of the Scope table, or None and the reason it cannot be read."""
    lines = readme.splitlines()
    start = next((i for i, line in enumerate(lines)
                  if (m := HEADING.match(line)) and m.group(1).strip().lower() == "scope"), None)
    if start is None:
        return None, "no '## Scope' heading"
    rows, header = [], None
    for number, line in enumerate(lines[start + 1:], start + 2):
        if HEADING.match(line):
            break
        if not line.lstrip().startswith("|"):
            if header is not None:
                break
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if header is None:
            header = [cell.lower() for cell in cells]
            if len(header) < 2 or header[1] != "what" or header[0] != "":
                return None, f"the scope table's header is {header}, not '| | What | Why |'"
            continue
        if set("".join(cells)) <= set("-: "):
            continue
        if len(cells) >= 2 and cells[0].lower() == "in":
            rows.append((number, cells[1]))
    if header is None:
        return None, "no table under '## Scope'"
    if not rows:
        return None, "the scope table has no 'in' row"
    return rows, ""


def phrases_of(rows: list[tuple[int, str]], min_words: int) -> dict[tuple[str, ...], list[tuple[int, list[str]]]]:
    """Every run of `min_words` consecutive words, to the rows (line, candidate) that hold it."""
    table: dict[tuple[str, ...], list[tuple[int, list[str]]]] = {}
    for line, cell in rows:
        for run in candidates(cell, min_words):
            for i in range(len(run) - min_words + 1):
                table.setdefault(tuple(run[i:i + min_words]), []).append((line, run))
    return table


def longest(shared: set[tuple[str, ...]], table: dict, min_words: int) -> list[tuple[str, ...]]:
    """Merge the shared `min_words`-grams that overlap inside one candidate into the longest runs."""
    merged = set()
    for gram in shared:
        for _, run in table[gram]:
            covered = [False] * len(run)
            for i in range(len(run) - min_words + 1):
                if tuple(run[i:i + min_words]) in shared:
                    covered[i:i + min_words] = [True] * min_words
            start = None
            for i, flag in enumerate(covered + [False]):
                if flag and start is None:
                    start = i
                if not flag and start is not None:
                    merged.add(tuple(run[start:i]))
                    start = None
    return sorted(merged)


def check(root: Path, config: dict) -> list[Finding]:
    settings = config.get("scope_overlap", {})
    if not settings:
        return []
    front_name = settings.get("front_page", "README.md")
    min_words = int(settings.get("min_words", 3))
    beside = root.parent
    front = (root / front_name).read_text(encoding="utf-8", errors="replace")
    findings, tables, present = [], {}, []
    for name, line in members_of(front):
        readme = beside / name / "README.md"
        if (beside / name).is_dir() and readme.is_file():
            present.append((name, line, readme))
    if len(present) < 2:
        return []
    for name, line in members_of(front):
        folder = beside / name
        if not (folder / "README.md").is_file():
            findings.append(Finding(NAME, front_name, line, f"{name}: no checkout beside this repository, so its scope was not compared", "warning"))
    for name, line, readme in present:
        rows, reason = in_rows(readme.read_text(encoding="utf-8", errors="replace"))
        if rows is None:
            findings.append(Finding(NAME, front_name, line, f"{name}: scope table not read ({reason}), so it was not compared", "warning"))
            continue
        tables[name] = (line, rows, phrases_of(rows, min_words))
    for first, second in combinations(tables, 2):
        _, rows_a, table_a = tables[first]
        _, rows_b, table_b = tables[second]
        shared = set(table_a) & set(table_b)
        if not shared:
            continue
        for phrase in longest(shared, table_a, min_words):
            gram = phrase[:min_words]
            line_a = table_a[gram][0][0] if gram in table_a else rows_a[0][0]
            line_b = table_b[gram][0][0] if gram in table_b else rows_b[0][0]
            findings.append(Finding(
                NAME, front_name, tables[first][0],
                f"{first} (row at line {line_a}) and {second} (row at line {line_b}) both claim "
                f"'{' '.join(phrase)}' in their 'in' rows: one of them owns it, the other links it", "warning"))
    return findings
