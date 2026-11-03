# A scope table says why

**Claim:** a member's scope is a table of in, later and out rows, and every row says why.

- **Grade:** convention, untested.
- **Evidence:** the table on the [front page](../../README.md#the-rules) and in each member; [signal the structure](https://github.com/Tewf/reader-ergonomics/blob/2e5b6f0c3e67d2dc8195a63cf882d46170e79a5a/principles/page/signal-the-structure.md) in the standard for a table over prose.
- **Check:** `scope-table` (exact: the header, the kinds and their order, a reason in every row).
- **Reader styles:** none.

## What it asks

- Under a heading Scope, a table with the header `| | What | Why |`, so the overlap check can read it.
- The first cell is in, later or out, and the rows come in that order.
- An out row names the member that holds the thing, or says that nobody does.
- The Why of a row is its reason, not a restatement of the What.

## Why

- A reader sees the boundary at a glance: what is held, what waits, what is elsewhere.
- A program can read the form, which is what makes the previous principle checkable.
- A row with a reason can be disputed; a row without one can only be accepted.

## Limits

- No experiment compares this form with prose for stating a scope.
- The check decides the form and not the truth: it cannot tell whether a row is accurate or its reason good.
- The shape is [scope table](../../shapes/scope-table.md); it has one filled example.
