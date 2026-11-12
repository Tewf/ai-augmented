# 0003: The overlap check gains a semantic pass

**Decision:** The scope-overlap check compares "in" rows by embedding as well as by shared words, in a second check of the meaning tier, with a provisional threshold of 0.70.

**Status:** accepted, 2026-11-03. **Shape:** [decision record](https://github.com/Tewf/reader-ergonomics/blob/65e42472e2d4cbfd994c2a86e95a47e5dc7301ca/shapes/decision-record.md).

## Context

- The textual check finds a shared run of three words. It finds nothing on the six members, and cannot see two rows that say the same thing in other words.
- The standard's meaning tier already embeds text with one small model (all-MiniLM-L6-v2, through fastembed), and skips itself when the library is absent.
- The threshold has no study behind it. The tests can fix it against fixtures: unrelated rows score 0.06, related but distinct rows up to 0.65, planted paraphrases from 0.76.

## Decision

- Add `scope_overlap_semantic.py` beside `scope_overlap.py`, in the meaning tier, reading the same tables from the same checkouts.
- Warn for each pair of rows of two different members at or above `semantic_threshold`, set to 0.70 in `checks/config.toml` and tagged PROVISIONAL.
- Clone the members in the meaning job of the checks workflow, so the pass runs in CI.

## Consequences

- **Good:** two rows in other words are found. On the six members it warns on one pair, at 0.76, the project and ide rows on what the model is handed, which the maintainer may rightly keep apart.
- **Good:** the textual pass stays in the program tier, free and exact in what it reads.
- **Bad:** the threshold separates its fixtures, not the family's future rows; a score is a question, not a verdict.
- **Bad:** the meaning job needs the clones, a network step that can fail; a failed clone is a warning in the log.
- **To keep it true:** when the maintainer has judged ten warnings, set the threshold from how many were real.

## See also

[Decisions](README.md); [one owner per claim](../principles/scope/one-owner-per-claim.md); the check's docstring in `checks/local/scope_overlap_semantic.py`.
