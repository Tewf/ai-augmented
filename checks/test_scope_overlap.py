"""Tests of checks/local/scope_overlap.py: each rule warns where it should and stays silent where it should not.

Run: READER_ERGONOMICS_CHECKS=checks/out/standard/checks python3 -m unittest discover -s checks
The standard's checks/ folder must be importable: set READER_ERGONOMICS_CHECKS to it, or check
reader-ergonomics out beside this repository (as CI does, under the name standard).
"""
import importlib.util
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
REPOSITORY = HERE.parents[1]
CANDIDATES = [os.environ.get("READER_ERGONOMICS_CHECKS", ""),
              REPOSITORY.parent / "standard" / "checks", REPOSITORY.parent / "reader-ergonomics" / "checks"]
sys.path.insert(0, str(next(Path(c) for c in CANDIDATES if c and (Path(c) / "framework").is_dir())))
SPEC = importlib.util.spec_from_file_location("scope_overlap", REPOSITORY / "checks" / "local" / "scope_overlap.py")
scope = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(scope)

CONFIG = {"scope_overlap": {"front_page": "README.md", "min_words": 3}}
FRONT = """# Hub

| Member | Problem | Status |
|---|---|---|
| [alpha](https://github.com/Tewf/alpha) | the first | scope only |
| [beta](https://github.com/Tewf/beta) | the second | scope only |
| [gamma](https://github.com/Tewf/gamma) | the third | scope only |

After the table.
"""


def readme(*rows: str, header: str = "| | What | Why |") -> str:
    """A member README whose scope table holds the given rows, each 'kind | what | why'."""
    body = "\n".join(f"| {row} |" for row in rows)
    return f"# Member\n\nIntro.\n\n## Scope\n\n{header}\n|---|---|---|\n{body}\n\n## Next\n\nText.\n"


class Base(unittest.TestCase):
    """A temporary folder holding the hub as 'hub' and the members beside it; no tests of its own."""
    def setUp(self) -> None:
        self.folder = Path(tempfile.mkdtemp())
        self.root = self.folder / "hub"
        self.write("hub/README.md", FRONT)
        self.member("gamma", "in | zebra quilt window | why")   # a third member that overlaps with nothing

    def tearDown(self) -> None:
        shutil.rmtree(self.folder)

    def write(self, path: str, text: str) -> None:
        (self.folder / path).parent.mkdir(parents=True, exist_ok=True)
        (self.folder / path).write_text(text, encoding="utf-8")

    def member(self, name: str, *rows: str, **keywords) -> None:
        self.write(f"{name}/README.md", readme(*rows, **keywords))

    def remove(self, *names: str) -> None:
        for name in names:
            shutil.rmtree(self.folder / name)

    def run_check(self, config: dict = CONFIG) -> list:
        return scope.check(self.root, config)


class SharedPhrase(Base):
    def test_a_shared_phrase_of_three_words_warns_once_for_the_pair(self):
        self.member("alpha", "in | the checker verdict beside each part | why")
        self.member("beta", "in | shows checker verdict beside the title | why")
        found = self.run_check()
        self.assertEqual(len(found), 1)
        self.assertIn("alpha", found[0].message)
        self.assertIn("beta", found[0].message)
        self.assertIn("checker verdict beside", found[0].message)

    def test_every_finding_is_a_warning(self):
        self.member("alpha", "in | the checker verdict beside each part | why")
        self.member("beta", "in | checker verdict beside the title | why")
        self.member("gamma", "in | checker verdict beside it | why")
        found = self.run_check()
        self.assertEqual(len(found), 3)
        self.assertEqual({finding.kind for finding in found}, {"warning"})
        self.assertFalse(scope.EXACT)

    def test_overlapping_grams_merge_into_the_longest_phrase(self):
        self.member("alpha", "in | red green blue black white | why")
        self.member("beta", "in | xx red green blue black white yy | why")
        found = self.run_check()
        self.assertEqual(len(found), 1)
        self.assertIn("red green blue black white", found[0].message)

    def test_two_shared_words_are_not_enough(self):
        self.member("alpha", "in | checker verdict | why")
        self.member("beta", "in | checker verdict | why")
        self.assertEqual(self.run_check(), [])

    def test_min_words_is_read_from_the_config(self):
        self.member("alpha", "in | checker verdict | why")
        self.member("beta", "in | checker verdict | why")
        self.assertEqual(len(self.run_check({"scope_overlap": {"min_words": 2}})), 1)

    def test_a_function_word_ends_a_phrase(self):
        self.member("alpha", "in | red apple with big stones | why")
        self.member("beta", "in | red apple and big stones | why")
        self.assertEqual(self.run_check(), [])

    def test_punctuation_ends_a_phrase(self):
        self.member("alpha", "in | red apple, green pear | why")
        self.member("beta", "in | green pear red apple | why")
        self.assertEqual(self.run_check(), [])

    def test_of_joins_two_words(self):
        self.member("alpha", "in | any tree of topics | why")
        self.member("beta", "in | a tree of topics only | why")
        found = self.run_check()
        self.assertEqual(len(found), 1)
        self.assertIn("tree of topic", found[0].message)

    def test_a_phrase_cannot_end_on_of(self):
        self.member("alpha", "in | red apple of the farm | why")
        self.member("beta", "in | red apple of a market | why")
        self.assertEqual(self.run_check(), [])

    def test_plural_and_possessive_and_case_do_not_hide_a_match(self):
        self.member("alpha", "in | The Checkers' verdict beside | why")
        self.member("beta", "in | checker's verdict beside it | why")
        self.assertEqual(len(self.run_check()), 1)

    def test_links_and_markup_are_read_as_their_text(self):
        self.member("alpha", "in | **checker** [verdict](http://x.y) `beside` it | why")
        self.member("beta", "in | checker verdict beside it | why")
        self.assertEqual(len(self.run_check()), 1)


class WhichRows(Base):
    def test_out_and_later_rows_are_not_claims(self):
        self.member("alpha", "in | something unrelated here | why", "out | checker verdict beside | x", "later | checker verdict beside | x")
        self.member("beta", "in | checker verdict beside | why")
        self.assertEqual(self.run_check(), [])

    def test_the_why_cell_is_not_read(self):
        self.member("alpha", "in | something unrelated here | checker verdict beside")
        self.member("beta", "in | checker verdict beside | other")
        self.assertEqual(self.run_check(), [])

    def test_a_phrase_across_two_rows_of_one_member_is_not_an_overlap(self):
        self.member("alpha", "in | checker verdict beside | a", "in | checker verdict beside | b")
        self.member("beta", "in | something else entirely | why")
        self.assertEqual(self.run_check(), [])

    def test_only_the_scope_section_is_read(self):
        text = readme("in | something unrelated here | why") + "\n## Other\n\n| | What | Why |\n|---|---|---|\n| in | checker verdict beside | x |\n"
        self.write("alpha/README.md", text)
        self.member("beta", "in | checker verdict beside | why")
        self.assertEqual(self.run_check(), [])


class Unreadable(Base):
    def test_a_table_of_another_shape_is_named_not_skipped(self):
        self.member("alpha", "in | checker verdict beside | why")
        self.member("beta", "in | checker verdict beside | why", header="| Kind | What | Why |")
        found = self.run_check()
        self.assertEqual(len(found), 1)
        self.assertIn("beta: scope table not read", found[0].message)

    def test_a_member_without_a_scope_heading_is_named(self):
        self.write("alpha/README.md", "# Member\n\nNothing here.\n")
        self.member("beta", "in | checker verdict beside | why")
        found = self.run_check()
        self.assertEqual(len(found), 1)
        self.assertIn("alpha: scope table not read (no '## Scope' heading)", found[0].message)

    def test_a_member_without_an_in_row_is_named(self):
        self.member("alpha", "out | checker verdict beside | x")
        self.member("beta", "in | checker verdict beside | why")
        found = self.run_check()
        self.assertEqual(len(found), 1)
        self.assertIn("no 'in' row", found[0].message)

    def test_a_missing_checkout_is_named_when_two_others_are_present(self):
        self.member("alpha", "in | one thing here | why")
        self.member("beta", "in | another thing there | why")
        self.remove("gamma")
        found = self.run_check()
        self.assertEqual(len(found), 1)
        self.assertIn("gamma: no checkout", found[0].message)
        self.assertEqual(found[0].kind, "warning")

    def test_fewer_than_two_checkouts_is_silent(self):
        self.member("alpha", "in | checker verdict beside | why")
        self.remove("gamma")
        self.assertEqual(self.run_check(), [])

    def test_no_table_in_the_config_is_silent(self):
        self.member("alpha", "in | checker verdict beside | why")
        self.member("beta", "in | checker verdict beside | why")
        self.assertEqual(self.run_check({}), [])


class FrontPage(Base):
    def test_members_are_the_links_of_the_first_column_with_their_line(self):
        self.assertEqual(scope.members_of(FRONT), [("alpha", 5), ("beta", 6), ("gamma", 7)])

    def test_links_outside_the_member_table_are_not_members(self):
        text = FRONT + "\nSee [delta](https://github.com/Tewf/delta).\n"
        self.assertEqual([name for name, _ in scope.members_of(text)], ["alpha", "beta", "gamma"])

    def test_a_front_page_without_the_table_has_no_members(self):
        self.assertEqual(scope.members_of("# Hub\n\nNothing.\n"), [])


if __name__ == "__main__":
    unittest.main()
