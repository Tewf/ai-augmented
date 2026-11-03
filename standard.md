# The AI-augmented standard

What a family of repositories on AI-augmented work shares, as far as the evidence goes.
A claim about a person and a model is set against each alone, and every member states its scope in a table, once. It extends
[reader-ergonomics](https://github.com/Tewf/reader-ergonomics/blob/4f99372093729dacf982e9174e94f6b8793c513d/standard.md): read that one first. This page adds only what a person, a model and a machine on one project change.

Grades mean what they mean in [reader-ergonomics](https://github.com/Tewf/reader-ergonomics/blob/4f99372093729dacf982e9174e94f6b8793c513d/standard.md#grades): measured, supported with caveat,
convention, not supported. Each principle states its grade and never claims more.

## How to use it

1. **Pick the shape** from [shapes/](shapes/README.md), and name it in the document with a `**Shape:**` line that links it.
2. **Write to the principles** below, and to those of reader-ergonomics, which still hold.
3. **Check:** run the standard's checks on the repository. `scope-table` reads each document that declares the shape,
   `three-arms` reads every table, and `scope-overlap` compares the members.

## Principles

<!-- principles:start -->

### Claims: saying that a person with a model does better

| Principle | Claim | Grade |
|---|---|---|
| [Compare with each part alone](principles/claims/compare-with-each-part-alone.md) | a claim that a person with a model does better sets the combination against the person alone and the model alone. | measured for the finding that a combination does worse, on average, than the better part alone (106 experiments, secondary); convention for the rule that every claim carries the three arms |

### Scope: what each member of the family owns

| Principle | Claim | Grade |
|---|---|---|
| [One owner per claim](principles/scope/one-owner-per-claim.md) | a thing is in the scope of one member of the family, and every other member links it. | convention, argued from the standard's one-place-per-fact principle; untested for scope tables |
| [A scope table says why](principles/scope/scope-table-with-why.md) | a member's scope is a table of in, later and out rows, and every row says why. | convention, untested |

<!-- principles:end -->

## Where the evidence is

Every principle links its review in [evidence/](evidence/README.md), and every work cited is listed once in the
[bibliography](evidence/bibliography.md).
