"""Three arms: a table that compares a person, a model and both names all three.

Vaccaro 2024 pooled 106 experiments and found that a person with a model did worse, on average, than the better of the
two alone. A claim of gain is therefore only a claim when it sets the combination against each part alone.

What it decides: in each Markdown table of the files in scope (outside fenced code), if any cell names a part alone
(human alone or model alone), the table names all three arms. A table that names only the combination is not flagged:
the word is common and a lone combination is more often a term than a claim. The arms and the words that name them are in `[three_arms]` of the config: human alone ("human alone",
"person alone"), model alone ("model alone", "ai alone") and the combination ("combination", "person and model",
"human and model", "both"). Words are matched whole and without case.

What it cannot decide: whether a table is a claim of gain (a glossary that explains "combination" is flagged and is a
false match, so every finding is a warning), whether the numbers in the arms are measured, or whether the task is a
decision or a creation task. Prose is not read, only tables.
Time O(size of the files).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _shapes import tables  # noqa: E402
from framework.check_api import Finding, files_in_scope, matches_any, prose_only  # noqa: E402

NAME = "three-arms"
EXACT = False

ARMS = {
    "human alone": ["human alone", "person alone"],
    "model alone": ["model alone", "ai alone"],
    "combination": ["combination", "person and model", "human and model", "both"],
}


TRIGGER = ["human alone", "model alone"]   # the arms whose mention makes a table a comparison


def arms_named(text: str, arms: dict[str, list[str]]) -> set[str]:
    """The arms a text names, matching each word whole and without case."""
    return {arm for arm, words in arms.items()
            if any(re.search(rf"\b{re.escape(word)}\b", text, re.IGNORECASE) for word in words)}


def check(root: Path, config: dict) -> list[Finding]:
    if "three_arms" not in config:
        return []
    settings = config["three_arms"]
    arms = settings.get("arms", ARMS)
    exempt = settings.get("exempt", [])
    findings = []
    for path in files_in_scope(root, config, {".md", ".qmd"}):
        if matches_any(path, exempt):
            continue
        text = prose_only((root / path).read_text(encoding="utf-8", errors="replace"))
        for line, rows in tables(text):
            named = arms_named("\n".join(rows), arms)
            if named & set(settings.get("trigger", TRIGGER)) and named != set(arms):
                missing = ", ".join(sorted(set(arms) - named))
                findings.append(Finding(NAME, path, line, f"a table names {', '.join(sorted(named))} but not {missing}: "
                                                          "set the combination against each part alone", "warning"))
    return findings
