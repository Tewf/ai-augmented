"""Tests of checks/local/three_arms.py and checks/local/scope_table.py: each warns or fails where it should and stays
silent where it should not.

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


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, REPOSITORY / "checks" / "local" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


arms, scope = load("three_arms"), load("scope_table")

SCOPE = """# A member

**Shape:** [scope table](../shapes/scope-table.md)

## Scope

| | What | Why |
|---|---|---|
| in | the first thing | a reason |
| later | the second thing | not yet |
| out | the third thing | [elsewhere](https://github.com/Tewf/elsewhere) |
"""


class Base(unittest.TestCase):
    """A temporary repository; files are written with `put`."""
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, True)

    def put(self, name: str, text: str) -> None:
        (self.root / name).write_text(text, encoding="utf-8")


class ThreeArms(Base):
    CONFIG = {"three_arms": {}}

    def run_check(self, text: str):
        self.put("a.md", text)
        return arms.check(self.root, self.CONFIG)

    def test_all_three_arms_pass(self) -> None:
        table = "| Arm | Result |\n|---|---|\n| Human alone | 0.5 |\n| Model alone | 0.6 |\n| Combination | 0.7 |\n"
        self.assertEqual(self.run_check(table), [])

    def test_missing_arm_warns_and_names_it(self) -> None:
        found = self.run_check("| Arm | Result |\n|---|---|\n| Human alone | 0.5 |\n| Combination | 0.7 |\n")
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].kind, "warning")
        self.assertIn("model alone", found[0].message.split("but not")[1])

    def test_combination_alone_is_not_a_comparison(self) -> None:
        self.assertEqual(self.run_check("| Question | Holder |\n|---|---|\n| Is the combination better? | Vaccaro 2024 |\n"), [])

    def test_model_alone_without_the_others_warns(self) -> None:
        self.assertEqual(len(self.run_check("| Arm | Result |\n|---|---|\n| AI alone | 0.6 |\n")), 1)

    def test_table_without_an_arm_is_silent(self) -> None:
        self.assertEqual(self.run_check("| Term | Meaning |\n|---|---|\n| checker | a program |\n"), [])

    def test_prose_and_fenced_tables_are_not_read(self) -> None:
        self.assertEqual(self.run_check("The combination wins.\n\n```\n| Combination |\n|---|\n```\n"), [])

    def test_word_must_be_whole(self) -> None:
        self.assertEqual(self.run_check("| Term |\n|---|\n| combinations of the parts |\n"), [])

    def test_no_settings_means_silent(self) -> None:
        self.put("a.md", "| Combination |\n|---|\n| x |\n")
        self.assertEqual(arms.check(self.root, {}), [])

    def test_exempt_file_is_skipped(self) -> None:
        self.put("a.md", "| Combination |\n|---|\n| x |\n")
        self.assertEqual(arms.check(self.root, {"three_arms": {"exempt": ["a.md"]}}), [])


class ScopeTable(Base):
    CONFIG = {"scope_table": {}}

    def run_check(self, text: str):
        self.put("a.md", text)
        return scope.check(self.root, self.CONFIG)

    def test_good_table_passes(self) -> None:
        self.assertEqual(self.run_check(SCOPE), [])

    def test_document_without_shape_line_is_not_read(self) -> None:
        self.assertEqual(self.run_check(SCOPE.replace("**Shape:**", "Shape")), [])

    def test_wrong_header_fails(self) -> None:
        found = self.run_check(SCOPE.replace("| | What | Why |", "| | Item | Reason |"))
        self.assertEqual([f.kind for f in found], ["error"])

    def test_missing_heading_fails(self) -> None:
        self.assertEqual(len(self.run_check(SCOPE.replace("## Scope", "## Range"))), 1)

    def test_unknown_kind_fails(self) -> None:
        found = self.run_check(SCOPE.replace("| later |", "| soon |"))
        self.assertTrue(any("not in, later or out" in f.message for f in found))

    def test_order_is_in_later_out(self) -> None:
        text = SCOPE.replace("| later | the second thing | not yet |\n", "") + "| later | late | not yet |\n"
        self.assertTrue(any("order is in, later, out" in f.message for f in self.run_check(text)))

    def test_empty_why_fails(self) -> None:
        found = self.run_check(SCOPE.replace("a reason", ""))
        self.assertTrue(any("Why cell" in f.message for f in found))

    def test_no_in_row_fails(self) -> None:
        found = self.run_check(SCOPE.replace("| in |", "| later |"))
        self.assertTrue(any("no 'in' row" in f.message for f in found))

    def test_out_row_saying_others_do_it_passes(self) -> None:
        found = self.run_check(SCOPE.replace("[elsewhere](https://github.com/Tewf/elsewhere)", "others do it"))
        self.assertEqual(found, [])

    def test_out_row_with_nothing_warns_only(self) -> None:
        found = self.run_check(SCOPE.replace("[elsewhere](https://github.com/Tewf/elsewhere)", "not ours"))
        self.assertEqual([f.kind for f in found], ["warning"])

    def test_skeleton_in_fenced_code_declares_nothing(self) -> None:
        self.assertEqual(self.run_check("```markdown\n" + SCOPE + "```\n"), [])


if __name__ == "__main__":
    unittest.main()
