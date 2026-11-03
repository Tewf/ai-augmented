"""Tests of checks/local/scope_overlap_semantic.py: the threshold separates the known non-overlaps from planted ones.

Run: READER_ERGONOMICS_CHECKS=checks/out/standard/checks python3 -m unittest discover -s checks
Needs fastembed (the standard's meaning tier); without it the tests are skipped. The model is loaded once.
"""
import importlib.util
import os
import shutil
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
REPOSITORY = HERE.parents[1]
CANDIDATES = [os.environ.get("READER_ERGONOMICS_CHECKS", ""),
              REPOSITORY.parent / "standard" / "checks", REPOSITORY.parent / "reader-ergonomics" / "checks"]
sys.path.insert(0, str(next(Path(c) for c in CANDIDATES if c and (Path(c) / "framework").is_dir())))
SPEC = importlib.util.spec_from_file_location("scope_overlap_semantic", REPOSITORY / "checks" / "local" / "scope_overlap_semantic.py")
semantic = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(semantic)

THRESHOLD = tomllib.loads((REPOSITORY / "checks" / "config.toml").read_text())["scope_overlap"]["semantic_threshold"]
CONFIG = {"scope_overlap": {"front_page": "README.md", "semantic_threshold": THRESHOLD}}
FRONT = """# Hub

| Member | Problem | Status |
|---|---|---|
| [alpha](https://github.com/Tewf/alpha) | the first | scope only |
| [beta](https://github.com/Tewf/beta) | the second | scope only |

After the table.
"""

# Pairs the family does not count as one claim, scored 0.65 and below when the threshold was set.
NON_OVERLAPS = [
    ("any reasoning or creation, written as a tree or graph of topics",
     "expressiveness: what a tree, or a graph, of topics can and cannot encode, stated formally"),
    ("Lean as the oracle for logic and proofs, the first and for now only checker of meaning",
     "environments, hooks and CI as the oracle of what a program can decide"),
    ("a lesson that teaches recursion", "perfume recommendation from a user's tastes"),
]
# Planted overlaps: the same claim in other words, scored 0.76 and above.
OVERLAPS = [
    ("the checks of the machine, run before any model reads the output",
     "the programs that verify the output first, so a model reads only what already passed"),
    ("the memory a model keeps across sessions", "what the model remembers from one session to the next"),
]


def readme(*rows: str) -> str:
    body = "\n".join(f"| in | {row} | why |" for row in rows)
    return f"# Member\n\n## Scope\n\n| | What | Why |\n|---|---|---|\n{body}\n\n## Next\n\nText.\n"


@unittest.skipUnless(semantic.available(), "fastembed is not installed")
class Semantic(unittest.TestCase):
    def setUp(self) -> None:
        self.folder = Path(tempfile.mkdtemp())
        self.root = self.folder / "hub"
        self.write("hub/README.md", FRONT)

    def tearDown(self) -> None:
        shutil.rmtree(self.folder)

    def write(self, path: str, text: str) -> None:
        (self.folder / path).parent.mkdir(parents=True, exist_ok=True)
        (self.folder / path).write_text(text, encoding="utf-8")

    def pair(self, first: str, second: str) -> list:
        self.write("alpha/README.md", readme(first))
        self.write("beta/README.md", readme(second))
        return semantic.check(self.root, CONFIG)

    def test_the_known_non_overlaps_stay_below_the_threshold(self):
        for first, second in NON_OVERLAPS:
            self.assertEqual(self.pair(first, second), [], first)

    def test_the_planted_overlaps_reach_it(self):
        for first, second in OVERLAPS:
            self.assertEqual(len(self.pair(first, second)), 1, first)

    def test_the_warning_quotes_both_rows_and_is_a_warning(self):
        found = self.pair(*OVERLAPS[1])
        self.assertEqual(found[0].kind, "warning")
        self.assertFalse(semantic.EXACT)
        for text in ("alpha", "beta", OVERLAPS[1][0], OVERLAPS[1][1], "cosine 0."):
            self.assertIn(text, found[0].message)

    def test_two_rows_of_one_member_are_not_compared(self):
        self.write("alpha/README.md", readme(*OVERLAPS[1]))
        self.write("beta/README.md", readme("a lesson that teaches recursion"))
        self.assertEqual(semantic.check(self.root, CONFIG), [])

    def test_out_and_later_rows_are_not_read(self):
        text = readme(OVERLAPS[1][0]).replace("| in | " + OVERLAPS[1][0], "| out | " + OVERLAPS[1][0])
        self.write("alpha/README.md", text + "\n")
        self.write("beta/README.md", readme(OVERLAPS[1][1], "another unrelated row"))
        self.assertEqual(semantic.check(self.root, CONFIG), [])

    def test_the_threshold_is_read_from_the_config(self):
        self.write("alpha/README.md", readme(*[OVERLAPS[1][0]]))
        self.write("beta/README.md", readme(OVERLAPS[1][1]))
        strict = {"scope_overlap": {"semantic_threshold": 0.99}}
        self.assertEqual(semantic.check(self.root, strict), [])

    def test_one_checkout_or_no_config_is_silent(self):
        self.write("alpha/README.md", readme(OVERLAPS[1][0]))
        self.assertEqual(semantic.check(self.root, CONFIG), [])
        self.write("beta/README.md", readme(OVERLAPS[1][1]))
        self.assertEqual(semantic.check(self.root, {}), [])

    def test_the_threshold_sits_between_the_two_sets(self):
        scores = lambda pairs: [semantic.scored_pairs([("a", 1, x), ("b", 2, y)])[0][0] for x, y in pairs]
        self.assertLess(max(scores(NON_OVERLAPS)), THRESHOLD)
        self.assertGreater(min(scores(OVERLAPS)), THRESHOLD)


if __name__ == "__main__":
    unittest.main()
