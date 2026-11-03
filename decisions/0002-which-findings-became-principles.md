# 0002: Which findings became principles

**Decision:** Of the review's findings, one became a principle with a measured grade, and the rules the repository
already enforces or shapes became two principles of convention; the rest stay findings.

**Status:** accepted, 2026-11-03. **Shape:** [decision record](https://github.com/Tewf/reader-ergonomics/blob/4f99372093729dacf982e9174e94f6b8793c513d/shapes/decision-record.md).

## Context

- The review in [family-name](../evidence/family-name/README.md) graded its findings, and the extension contract asks a
  principle for each finding that earned measured or supported with caveat, and for each rule a program enforces.
- Only one finding earned a measured grade as a rule: Vaccaro 2024, the combination against each part alone. The
  teaming reviews (O'Neill 2020, Berretta 2023) earned supported with caveat, but they name a field and give no rule.
- The repository enforces one rule by a program already, scope-overlap, and states another in its front page, the
  scope table that the program reads.
- A principle must name a registered check, or the standard's principle-coverage fails.

## Decision

- Write [Compare with each part alone](../principles/claims/compare-with-each-part-alone.md), graded clause by clause, with a new check, `three-arms`.
- Write [One owner per claim](../principles/scope/one-owner-per-claim.md), convention, checked by the existing `scope-overlap`.
- Write [A scope table says why](../principles/scope/scope-table-with-why.md), convention, with a new check, `scope-table`, and the shape [scope table](../shapes/scope-table.md).
- Leave as findings: the names of the field, the teaming fit, the third role of the checking machine, and the rule that the model decides nothing.

## Consequences

- **Good:** each principle names a check that runs in CI, and the one measured finding is a rule a case can be held to.
- **Good:** the scope table, which the overlap check could only read, is now defined in one place with an example.
- **Bad:** `three-arms` is a heuristic over tables; it warns on a glossary that explains the word combination.
- **Bad:** the field's names, the teaming fit and the third role are not rules, so no check holds them; they live in the review only.
- **To keep it true:** when the third role or the rule that the model decides nothing is measured, write it as a principle with its grade; until then, it stays a finding.

## See also

[Decisions](README.md); [the standard card](../standard.md); [the review](../evidence/family-name/README.md).
