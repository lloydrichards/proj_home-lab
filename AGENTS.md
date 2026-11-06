# Working in this repository

This repository records the home lab's hardware, services, setup procedures, research, decisions, and learnings. Start with `README.md` and `docs/README.md` for navigation and document ownership.

## Plain-language responses

- Lead with the answer, result, or decision.
- Write for the reader's likely level of knowledge. Use familiar, concrete words and define necessary jargon once.
- Keep technical names, code, commands, identifiers, and error text exact.
- Structure longer responses so readers can quickly find the decision, evidence, risks, and next action.
- Prefer short sentences and paragraphs when they make the meaning clearer.
- Remove filler, repetition, vague hedging, and unnecessary caveats.
- Use a small concrete example when it helps explain a complex idea.
- Before sending, check that the reader can find, understand, and use the information.

## Keep the knowledge library current

Use the repository's [OKF skill](.agents/skills/okf/SKILL.md) when exploring or maintaining `.okf/`. Read `.okf/index.md`, then inspect relevant concepts and their sources before changing them.

After research, a setup change, a decision, or a useful learning, check whether the library's claims, relationships, or open questions have changed. Update affected concepts in the same task when authorized to edit the repository. A read-only request authorizes findings, not edits.

- Research belongs in `docs/research/`, with primary sources and dates for release-sensitive findings. Promote durable findings into the owning concepts and link related technologies, decisions, and learnings.
- Setup and operating procedures belong in the guides. Update the inventory and service register from observed changes. Update concepts when the role, dependency, exposure, or recovery approach changes.
- Decisions belong in `docs/decisions/`. Reflect their rationale and consequences in the relevant OKF decision and link affected technologies. Preserve the distinction between proposals and user-confirmed choices.
- Record actual changes, incidents, and outcomes in `docs/logs/`. Capture reusable lessons in `.okf/learnings/` with their supporting evidence. Do not present a conclusion from documentation as an observed incident result.
- Revise an existing concept before adding a near-duplicate. Add focused, meaningful relationships and update `.okf/index.md` for new entries.
- Leave the library unchanged when existing claims remain accurate. Formatting changes, repeated checks, and routine file edits do not need new concepts or log entries.

Keep detailed commands and volatile version information in the owning guides or research notes. Concepts explain meaning, relationships, and lab relevance without duplicating those procedures. Cite repository evidence through file-relative `sources[].resource` metadata. Use file-relative Markdown links between concepts, with a short relation phrase in the link title when useful.

## Distinguish evidence from plans

State whether a claim is user-reported, observed on a named host and date, researched in documentation, proposed, historical, or unknown. A setup guide is not evidence that its steps ran. A failed connection does not establish a machine's configuration.

Use OKF `draft`, `stable`, and `deprecated` for document lifecycle, not deployment state. Add `verified` only for the claims a human or deterministic check actually verified. Structural validation does not verify hardware, security, or running services.

If observed behavior conflicts with a recorded decision, report the conflict. Do not silently rewrite the decision to match the machine. Preserve historical context when superseding a choice or recipe.

Keep credentials, tokens, private keys, and raw private machine evidence outside Git. Use ignored `local/` for private output and add only reviewed summaries to tracked documents.

## Validate knowledge changes

Use the repository's configured CLI or check script if one is added. Otherwise, with `okf-graph` installed:

```bash
okf-graph validate .okf --json
okf-graph graph neighbors .okf <changed-concept-id> --json
```

The existing sibling checkout is a local fallback when Bun and its dependencies are available:

```bash
bun run ../proj_okf-graph/apps/okf-graph/src/index.ts validate .okf --json
bun run ../proj_okf-graph/apps/okf-graph/src/index.ts graph neighbors .okf <changed-concept-id> --json
```

Concept IDs are bundle-relative paths without `.md`, such as `technologies/tailscale`. Confirm command availability rather than assuming the sibling checkout exists. Run `eval .okf --json` for substantial graph changes and review its findings without adding links merely to improve metrics.

Check that source paths resolve as well as concept links. Fix validation errors and review warnings. Report changed concepts, checks performed, and unresolved gaps. If validation cannot run, state that explicitly.
