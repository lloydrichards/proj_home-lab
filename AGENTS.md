# Maintain an assistant-supported home lab notebook

Help Lloyd set things up, troubleshoot, and remember what we explored and why. Maintain this notebook as part of doing the work. The user should not need to read the repository end to end or synchronize several records by hand. Start with `README.md`, then follow the relevant device page or shared record.

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
- Keep `devices/home-lab/preparation.md` as the single list of upcoming HP work. Research and OKF explain the reasons and test details, linking to that list rather than maintaining parallel task lists.
- Keep lab-wide explanations in `docs/explanations/` and shared operating procedures in `docs/how-to/`. Device guides link these rather than copying them. Keep device-specific explanations and procedures with their device.
- Keep device guides under `devices/`, starting with `home-lab`, `remote-lab`, and `admin-lab`. Each device README links its status, guides, research, and relevant OKF decisions. A directory name is not evidence that the hostname has been applied.
- Keep arriving hardware in a preparation checklist. Expand setup instructions when we perform the work, recording checks and recovery steps worth repeating.
- Keep lab-wide inventory, BOM, and the service register in `devices/_reference/`. Update these owning records when device, service, or purchase facts change. Device pages summarize purpose and status and link the records rather than copying specifications or maintaining another inventory.
- Use `.okf/` for concepts, why we prefer an approach, alternatives considered, unresolved questions, and reusable learnings. Keep device-specific choices in `.okf/decisions/<device>/` and cross-device choices directly in `.okf/decisions/`. Link decisions from the relevant device README. Do not create parallel ADRs or duplicate decisions in device guide directories.
- Keep research spanning devices or the Mac client in `research/`. Put device-specific research under `devices/<device>/research/`. Retain research only when its sources or investigation help a real question, and recheck release-sensitive facts at the point of use.
- Add future devices under `devices/` with a directory and a short README. Create guide, research, or decision directories only when they have useful content. Keep historical Pi recipes marked as unverified after moves; reorganizing a recipe does not validate its commands or deploy its services.
- Add a troubleshooting note when it helps diagnose or recover from a recurring problem. Do not create routine activity logs, copied historical snapshots, or completion reports. Git keeps change history.
- Maintain the affected notes as we work and give the user a short account of the result and remaining uncertainties. Routine edits do not need new documents.

## Maintain OKF alongside the work

Use the [OKF skill](.agents/skills/okf/SKILL.md). Read `.okf/index.md`, then the relevant concepts and sources. Update existing concepts before adding new ones. Link meaningful relationships and update the index when adding an entry.

### Find context before researching

Before new research, setup proposals, or troubleshooting, use OKF to find the existing context:

1. Read `.okf/index.md` or run `okf-graph bundle index .okf`. Start with the relevant device's entry point and narrow the question.
2. Use `rg` on concept titles, descriptions, and cited source paths to find the owning concept. Read it with `okf-graph concept .okf <concept-id>`, then inspect `okf-graph graph neighbors .okf <concept-id> --json`.
3. Follow the relevant decisions, related concepts, and `sources[].resource` files before browsing. Use `okf-graph graph path .okf <from-id> <to-id> --json` when you need to understand how two topics connect. A graph path suggests related context; read the relationships before treating it as a dependency.
4. Research the unanswered question or recheck facts that may have changed. Existing notes can direct the investigation, but dated research and historical recipes do not prove current versions or deployment.
5. Incorporate durable findings into the owning concept and its source note. Add file-relative links to concepts whose relationship matters, with a clear relation in the link title. Create a concept only when none owns the topic; link it from the index and the relevant concept or device page. Preserve user choices and distinguish proposals from observations.

Use the installed CLI when available, otherwise the Bun fallback below. Keep discovery focused; do not read the whole bundle or add reciprocal links solely to improve metrics. For a read-only task, report findings without editing the notebook.

Keep commands in a recipe or detailed research note. Keep their purpose and tradeoffs in OKF. Cite evidence through file-relative `sources[].resource` metadata and link concepts with file-relative Markdown links. User choices can be recorded directly in a concept with the date and context; do not invent a separate evidence document just to cite it.

Distinguish user-reported facts, live observations with host and date, researched behavior, proposals, and unknowns. A written recipe is not evidence that its steps ran. `draft`, `stable`, and `deprecated` describe knowledge maturity, not deployment. Use `verified` only for claims actually checked. Report conflicts with a user choice rather than silently changing the choice.

A read-only request authorizes findings, not edits. Keep secrets and raw private machine output outside Git, using ignored `local/` when useful.

## Check the result

Validate `.okf/` after concept edits and inspect affected graph neighborhoods. Check local links and source paths after moves or deletions. If a check cannot run, say so.

With an installed CLI, use `okf-graph validate .okf --json` and `okf-graph graph neighbors .okf <concept-id> --json`. Concept IDs are bundle-relative paths without `.md`.

The sibling checkout is a fallback when Bun and its dependencies are available:

```bash
bun run ../proj_okf-graph/apps/okf-graph/src/index.ts bundle index .okf
bun run ../proj_okf-graph/apps/okf-graph/src/index.ts concept .okf <concept-id>
bun run ../proj_okf-graph/apps/okf-graph/src/index.ts graph neighbors .okf <concept-id> --json
bun run ../proj_okf-graph/apps/okf-graph/src/index.ts graph path .okf <from-id> <to-id> --json
bun run ../proj_okf-graph/apps/okf-graph/src/index.ts validate .okf --json
bun run ../proj_okf-graph/apps/okf-graph/src/index.ts eval .okf --json
```

Confirm tool availability. For substantial graph changes, run `eval .okf --json` and review findings alongside the changed concepts and sources. Evaluation describes structure and navigation; it does not certify factual accuracy, freshness, or deployment. Report tool findings separately from your content assessment. Do not invent a numeric tool grade or add links just to improve metrics.

## Commit and PR titles

Use Conventional Commits without emojis or emoji shortcodes, such as `docs: simplify HP preparation`. Apply the same style to PR titles.
