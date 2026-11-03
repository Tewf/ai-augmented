# Reader style: agent

The reader style of an agent handed a brief. It has three parts: who the agent is, five overrides with their grades, and what is not yet known.

## Who

- **Reader:** an agent, a language model that is handed `START.md`, `memory/INDEX.md` and a `brief.md`, acts on a project with tools, and has its output checked by programs.
- **Expertise:** broad and shallow, as in [the language-model style](https://github.com/Tewf/reader-ergonomics/blob/4f99372093729dacf982e9174e94f6b8793c513d/reader-styles/llm-reader.md). It knows the field and nothing of this project.
- **Medium:** a context window, with tools to read more files and to run commands.
- **Reading mode:** front to back once, then back to the brief to check what it was asked.

This style extends the language-model style. Everything that style and the [standard](https://github.com/Tewf/reader-ergonomics/blob/4f99372093729dacf982e9174e94f6b8793c513d/standard.md) say still holds. Only what this family's own evidence adds is listed.

## Overrides

| Principle | Change | Why |
|---|---|---|
| [overview first](https://github.com/Tewf/reader-ergonomics/blob/4f99372093729dacf982e9174e94f6b8793c513d/principles/document/overview-first.md) | strengthen: the brief, with its four headings, halves the failures of a cheap model against no brief; naming the checks adds nothing once the tests are hidden | 0 of 60 with no brief, 30 of 60 with the convention brief, 29 of 60 with the checks added, on hidden tests (Brief test 2026, round two; the brief: measured, descriptive, two tiers, three tasks; naming the checks: not supported) |
| [one place per fact](https://github.com/Tewf/reader-ergonomics/blob/4f99372093729dacf982e9174e94f6b8793c513d/principles/collection/one-place-per-fact.md) | strengthen: the start file carries one sentence giving the repository precedence over a stale instruction | a stale file was followed in 90.1% of choices; one sentence of precedence raised the share following the code from 4.2% to 91.4% (Xu 2026; measured, secondary) |
| [size is a prompt](https://github.com/Tewf/reader-ergonomics/blob/4f99372093729dacf982e9174e94f6b8793c513d/principles/collection/size-is-a-prompt.md) | strengthen: the start file and the memory index each stay under a bound, and the rest is read on demand | the method's design; no study sets the length (convention, PROVISIONAL) |
| [overview first](https://github.com/Tewf/reader-ergonomics/blob/4f99372093729dacf982e9174e94f6b8793c513d/principles/document/overview-first.md) | add: when several agents work on one project, a central check runs on their results | errors grew 17.2 times without central checking and 4.4 times with it (Kim 2025; measured) |
| (decisions) | add: the agent decides nothing that no program or person has checked | the blueprint's position and the method's decision 0003, from Vaccaro 2024 (convention) |

Sources: Brief test 2026 is the experiment of ai-augmented-agents. Round two is in its [results](https://github.com/Tewf/ai-augmented-agents/blob/master/experiments/brief-test/results-2.md) and [decision 0005](https://github.com/Tewf/ai-augmented-agents/blob/master/decisions/0005-listing-the-checks-is-not-a-gain-on-unseen-cases.md). Round one was 5 of 10 with the checks listed, 1 of 10 rescored on hidden cases. The others are in the [bibliography](../evidence/bibliography.md).

## Thresholds

The bound is read from configuration, never typed into a file.

```toml
[agent_reader]
start_file_max_lines = 200   # PROVISIONAL: from the method's design, no study sets it
index_max_lines = 200        # PROVISIONAL: same
```

## Open questions

- Whether the brief effect holds beyond one task and one small model: not measured.
- Whether 200 lines is the right bound: not measured, and a vendor gives under 200 as practice only.
- Whether the precedence sentence helps when the stale file is short: not measured.
- Whether a central check pays for its cost with two agents rather than many: not measured here.
