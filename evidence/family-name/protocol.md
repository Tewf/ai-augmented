# Protocol: how the pool was built

A first pass by one reviewer on 2026-11-02, after Garousi 2019. It aims for 15 to 25 sources and held 23 on 2026-11-02; a forward pass on 2026-11-03 added 4 (27 in all).

**Shape:** [protocol](https://github.com/Tewf/reader-ergonomics-review/blob/a7f405f26f14cd188291e2a86b630121c4302a94/shapes/protocol.md)

## Why grey literature

Garousi's seven questions, answered for this topic.

| Question | Answer |
|---|---|
| Is the subject complex and not solvable by formal studies alone? | yes: it joins a person, a model and checks |
| Is the practice ahead of the research? | yes: agent files and agent patterns run ahead of studies |
| Is the context important? | yes: one project, one maintainer |
| Is there little formal evidence? | yes, on language models in a project |
| Do practitioners seek the answer? | yes |
| Is the topic multi-disciplinary? | yes: economics, human factors, software |
| Is the answer in practitioners' hands? | partly |

## Questions

Q1 to Q4 are in [frame](frame.md).

## Existing reviews

Searched first, and placed in strand 0 of [review](review.md): Vaccaro 2024, O'Neill 2020, Berretta 2023, Mosqueira-Rey 2022, Wu 2022b, Zou 2025.

## Formal search

OpenAlex, title and abstract, no identity sent, run on 2026-11-02. Counts as the service returned them.

| String | Hits |
|---|---|
| "intelligence augmentation" | 265 |
| "hybrid intelligence" | 2,099 |
| "human-AI teaming" | 1,261 |
| "human-autonomy teaming" | 547 |
| "human-in-the-loop" | 20,235 |
| "human-AI collaboration" | 10,309 |
| "augmented intelligence" | 1,369 |
| "centaur" and "human-AI" | 66 |
| "human-AI collaboration" and "language model" | 1,453 |

Titles were then screened with title searches sorted by citations: human-agent collaboration survey, human-AI teaming review, intelligence augmentation.
The seminal works (Engelbart, Licklider, Parasuraman) were added by recall and verified on Crossref.
No forward snowballing was run.

## Grey search

Producers read in full: one report, one working paper, one preprint, one essay, one company engineering post, one convention site.
No search engine was run for grey literature; the pool is of leads from the formal pass. This is a limit.

## Stopping rule

Effort bounded, with saturation: a string stopped after 5 consecutive results that added no concept.
The pool stopped at 23, inside the 15 to 25 the brief asked. The forward pass of 2026-11-03 brings it to 27, inside the 40 the rules allow.

## Selection and quality

- Included: defines or measures a person working with a machine or model, or is a survey of one name.
- Excluded: single-domain applications (medicine, hydrology) that use a name without defining it.
- Grey sources are scored on Garousi's 20 criteria; below 10 they are examples of practice only.

## Extraction and synthesis

Definition, task, effect size and sample size where given; synthesis is narrative by question.

## Forward citations, 2026-11-03

Seeds: the three works the review cites most. Counted across the family-name files, they are Akata 2020 (8 mentions),
Vaccaro 2024 (7) and Parasuraman 2000 (6). The count in review.md alone ties at 2 and 1, so the wider count breaks the tie.

| Seed (OpenAlex id) | Filter string | Citing works (count) | Retrieved and screened |
|---|---|---|---|
| Akata 2020 (W3046399757) | cites, publication year after 2023 | 273 | 200, by citation count |
| Vaccaro 2024 (W4403839497) | cites, publication year after 2023 | 596 | 200, by citation count |
| Parasuraman 2000 (W2123179704) | cites, publication year after 2023 | 1,127 | 200, by citation count |

- Unique citing works across the three: 586.
- Titles read on a concept filter (hybrid intelligence, augmentation, teaming, human-automation, human-in-the-loop, complementarity, agentic and similar): 191.
- Candidates whose abstract was read: 6. Two had no abstract in the index and were not graded.
- Added: 4 (Richardson 2025, González 2026, Hemmer 2025, Gómez 2025). Each sharpens a finding in review.md section 4.
- The later journal version of Dell'Acqua 2023 (W7135096569) was found; it is the same study, so it is not a new work.
- Abstract numbers are marked secondary. The 105 articles of Gómez 2025 is read in the abstract.
- The key was read from the environment only and no identity was sent, only the API key.
- Polite rate: one request per second, and a pause between seeds.

## Second rater on the grey sources, 2026-11-03: not completed

Garousi's criteria were pasted into one prompt per source, and each source went through ask-mistral, one call per source.
Six sources were sent: Engelbart 1962, Dell'Acqua 2023, Peng 2023, Case 2018, Anthropic 2024 and Agentic AI Foundation 2026.
Every call returned no output and timed out. The endpoint did not answer a one-word test either.
So no independent score exists, and agreement (mean absolute difference, kappa on the threshold) is not reported.
No score in sources.md was changed. The text sent was the source's full text where it was reachable (Engelbart first 40000 of about 295000 characters, Peng complete, Anthropic and the convention site complete).
Dell'Acqua 2023 and Case 2018 are not reachable as text (HTTP 403 to a plain client, and no User-Agent change allowed); the rater would have had only the abstract.
The rerun is the next step once the endpoint answers.

## Not searched

- Forward citations of works beyond the three seeds.
- Semantic Scholar, as a second source for forward citations.
- Google Scholar, ACM and IEEE search interfaces.
- Grey literature by search engine; Q/A sites; practitioner surveys.
- Work in French or other languages.

## Limits

One reviewer, no agreement check. Numbers marked (secondary) were read in an abstract returned by a service, not in the paper.
