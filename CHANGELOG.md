# Changelog

The releases this repository pins, newest first, in the form of [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
A pin move is recorded here, not in decisions/.

## [Unreleased]

### Changed

- Pinned reader-ergonomics v1.24.2 (`65e4247`), from v1.21.0 (`2e5b6f0`): fixes that remove false findings in the sentence, term and figure checks, and `[defined_terms] cues`.

## [0.1.1] - 2026-11-04

### Changed

- Pinned reader-ergonomics v1.21.0 (`2e5b6f0`), from v1.20.0 (`4f99372`): duplication skips the lines a declared shape prescribes
- The agent reader style: the brief with its four headings halves a cheap model's failures against no brief (measured,
  descriptive); naming the checks adds nothing once tests are hidden (not supported). Brief test, round two, 180 calls.
- Pinned reader-ergonomics v1.20.0 (`4f99372`), from v1.19.2 (`b9732b9`): the runner's verdicts file (`--out`), and hand-written llms.txt lines kept through a rebuild

### Added

- A semantic pass of the scope-overlap check (`checks/local/scope_overlap_semantic.py`, meaning tier), with a provisional
  threshold of 0.70 in `checks/config.toml` and 8 unit tests; the checks workflow clones the members for it.
- Decision 0003, which records the threshold and why the pass is a check of its own.
- Tag v0.1.1 and a GitHub release of the same name.

## [0.1.0] - 2026-11-03

### Added

- The first release: the map of the two families, the shared words, and the rule of one repository per problem.
- A first-pass review of the family's name in `evidence/family-name/`, 23 sources, naming its baseline H1.
- The card `standard.md` and three principles: compare with each part alone, one owner per claim, a scope table says why.
- The scope-table shape with a filled example, and the reader style of an agent handed a brief.
- Three checks in `checks/local/` (scope overlap, three arms, scope table) with 44 unit tests.
- Two decision records, and a take-it block on both front pages.
- Pinned reader-ergonomics v1.19.2 (`b9732b9`), as below.

## 2026-11-02

### Added

- Pinned reader-ergonomics v1.19.2 (`b9732b9`), at the repository's start: the standard's pin, link, changelog and
  decision-record checks, which this skeleton is written to pass.
