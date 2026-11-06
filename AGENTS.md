# Maintain an assistant-supported home lab notebook

Help Lloyd set things up, troubleshoot, and remember what we explored and why. Maintain this notebook as part of doing the work. The user should not need to read the repository end to end or synchronize several records by hand. Start with `README.md`; find the relevant recipe or research through `docs/README.md`.

## Plain-language responses

- Lead with the answer, result, or decision.
- Write for the reader's likely level of knowledge. Use familiar, concrete words and define necessary jargon once.
- Keep technical names, code, commands, identifiers, and error text exact.
- Structure longer responses so readers can quickly find the decision, evidence, risks, and next action.
- Prefer short sentences and paragraphs when they make the meaning clearer.
- Remove filler, repetition, vague hedging, and unnecessary caveats.
- Use a small concrete example when it helps explain a complex idea.
- Before sending, check that the reader can find, understand, and use the information.

## Keep only useful material

- Keep `README.md` short: what runs where, known access details, the next task, and links when needed.
- Keep `docs/hp-preparation.md` as the single list of upcoming HP work. Research and OKF explain the reasons and test details, linking to that list rather than maintaining parallel task lists.
- Keep arriving hardware in a preparation checklist. Expand setup instructions when we perform the work, recording checks and recovery steps worth repeating.
- Update device, service, and purchase facts in `docs/reference/` when new evidence changes them. Link related records rather than repeating full specifications.
- Use `.okf/` for concepts, why we prefer an approach, alternatives considered, unresolved questions, and reusable learnings. The existing `.okf/decisions/` entries own choice reasoning; do not create parallel ADRs.
- Keep detailed research in `docs/research/` only when its sources or investigation help a real question. Recheck release-sensitive facts at the point of use.
- Add a troubleshooting note when it helps diagnose or recover from a recurring problem. Do not create routine activity logs, copied historical snapshots, or completion reports. Git keeps change history.
- Maintain the affected notes as we work and give the user a short account of the result and remaining uncertainties. Routine edits do not need new documents.

## Maintain OKF alongside the work

Use the [OKF skill](.agents/skills/okf/SKILL.md). Read `.okf/index.md`, then the relevant concepts and sources. Update existing concepts before adding new ones. Link meaningful relationships and update the index when adding an entry.

Keep commands in a recipe or detailed research note. Keep their purpose and tradeoffs in OKF. Cite evidence through file-relative `sources[].resource` metadata and link concepts with file-relative Markdown links. User choices can be recorded directly in a concept with the date and context; do not invent a separate evidence document just to cite it.

Distinguish user-reported facts, live observations with host and date, researched behavior, proposals, and unknowns. A written recipe is not evidence that its steps ran. `draft`, `stable`, and `deprecated` describe knowledge maturity, not deployment. Use `verified` only for claims actually checked. Report conflicts with a user choice rather than silently changing the choice.

A read-only request authorizes findings, not edits. Keep secrets and raw private machine output outside Git, using ignored `local/` when useful.

## Check the result

Validate `.okf/` after concept edits and inspect affected graph neighborhoods. Check local links and source paths after moves or deletions. If a check cannot run, say so.

With an installed CLI, use `okf-graph validate .okf --json` and `okf-graph graph neighbors .okf <concept-id> --json`. Concept IDs are bundle-relative paths without `.md`.

The sibling checkout is a fallback when Bun and its dependencies are available:

```bash
bun run ../proj_okf-graph/apps/okf-graph/src/index.ts validate .okf --json
bun run ../proj_okf-graph/apps/okf-graph/src/index.ts graph neighbors .okf <concept-id> --json
```

Confirm tool availability. For substantial graph changes, run `eval .okf --json` and review findings without adding links just to improve metrics.
