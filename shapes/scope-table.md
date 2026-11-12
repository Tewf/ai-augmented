# Shape: scope table

This shape states what one member of the family holds. Its first reader is a person deciding where a piece of work
belongs; its second is the overlap check, which reads the table. It has three kinds of row: what is in, what is
later, and what is out with the member that holds it, and each row says why.

## When to use it

- On the front page of every member of the family, under the heading Scope.
- When a thing might belong to two members: write it in one table and link it from the other.
- Not for the hub, which holds the map and the words and claims no scope of its own.
- Not for a list of tasks: a scope says what the member answers, not what is left to do.

## How each part maps to the evidence

| Part | What it does | Evidence | Grade |
|---|---|---|---|
| Header, empty then What then Why | the form the overlap check reads | [scope-overlap](https://github.com/Tewf/ai-augmented/blob/master/checks/local/scope_overlap.py) | convention |
| In rows | what the member claims | [one owner per claim](../principles/scope/one-owner-per-claim.md) | convention, untested |
| Later rows | what is wanted and not yet held | the family's rule that a member answers one question | convention |
| Out rows | what another member holds, linked | [one place per fact](https://github.com/Tewf/reader-ergonomics/blob/65e42472e2d4cbfd994c2a86e95a47e5dc7301ca/principles/collection/one-place-per-fact.md) | supported with caveat, from the standard |
| Why column | the reason for the row | [a scope table says why](../principles/scope/scope-table-with-why.md) | convention, untested |

## The principles it applies

| Part | Principle |
|---|---|
| One table, three kinds of row | [signal the structure](https://github.com/Tewf/reader-ergonomics/blob/65e42472e2d4cbfd994c2a86e95a47e5dc7301ca/principles/page/signal-the-structure.md) |
| An out row links the member | [one place per fact](https://github.com/Tewf/reader-ergonomics/blob/65e42472e2d4cbfd994c2a86e95a47e5dc7301ca/principles/collection/one-place-per-fact.md) |
| Each member claims once | [one owner per claim](../principles/scope/one-owner-per-claim.md) |

## The skeleton

```markdown
## Scope

| | What | Why |
|---|---|---|
| in | <what the member claims, as a noun phrase> | <the reason it is claimed> |
| later | <what is wanted and not yet held> | <why it waits> |
| out | <what another member holds> | <the reason, and [the member](link) that holds it> |
```

## Where each part comes from

- The in rows come from the problem the member answers, one row per part of the answer.
- The out rows come from the neighbours: each thing a reader might expect here and finds elsewhere.
- The Why comes from the maintainer's reason for the boundary, in a sentence.

## The rules

1. The header is exactly `| | What | Why |`; the overlap check reads no other.
2. The first cell is in, later or out, and the rows come in that order.
3. There is at least one in row.
4. A What is a noun phrase, so that two members' phrases can be compared.
5. No cell is empty: a row without a reason is a guess.
6. An out row links the member that holds the thing, or says who does, or that nobody does.
7. A thing is in at most one member's table. If two want it, one owns it and the other links it.

## Worked example

[The scope of ai-augmented-agents](examples/agents-scope.md), copied from that member's front page as it stood on
2026-11-03: four in rows, three out rows, and a reason on each. It carries the Shape line, so the checks run on it as
on any scope table.
