---
name: maintain-lab-docs
description: Add, update, or review home-lab documentation using Diátaxis, shared versus device ownership, concise Mermaid explanations, and evidence-aware operating guides. Use for notebook content and structure; use alongside the OKF skill for graph mechanics.
---

# Maintain lab documentation

Help a reader understand the lab, perform a task, or rebuild a machine without reading the repository end to end. Apply this workflow to the requested change; a small correction does not need a reorganization.

Start at [README.md](../../../README.md) and follow the affected device or shared guide. Read [AGENTS.md](../../../AGENTS.md) for repository conventions and the [OKF index](../../../.okf/index.md) for existing decisions. Use the available technical-writing skill for prose and the [OKF skill](../okf/SKILL.md) for concept maintenance. A review-only request produces findings without edits.

## Choose the owner before writing

| Content | Owner |
|---|---|
| How the whole lab fits together | `docs/explanations/` |
| A task spanning hosts or a common client procedure | `docs/how-to/` |
| Device installation, operation, recovery, or behavior | `devices/<device>/` with `setup.md`, `how-to/`, `explanations/`, or `reference/` as needed |
| Current hardware, service facts, addresses, and dated checks | Existing records under `devices/_reference/` |
| Choices, alternatives, tradeoffs, and reusable lessons | Existing `.okf/` concepts and decisions |
| Sources and unresolved investigation | `research/` for shared topics, or `devices/<device>/research/` |
| Upcoming HP work | `devices/home-lab/preparation.md` |

Update an existing owner before adding a page. Device pages link shared explanations rather than copying them. A collector running on the HP can still have its contract owned by the Pi backup reference; location alone does not determine ownership.

Do not create matching folders or guides for every device just for symmetry. A new device can start with a short README. Unknown dependencies or missing recovery evidence can justify a diagnostic guide without a complete setup tutorial.

## Give each page one job

| Diátaxis mode | Reader need | Include |
|---|---|---|
| Tutorial | Build something for the first time | An ordered route, prerequisites, visible outcomes, and links to task guides |
| How-to | Complete a specific task | Host/account, required inputs, commands, expected results, stop conditions, and recovery where needed |
| Explanation | Understand how or why it works | Relationships, authority, dependencies, limitations, and useful diagrams |
| Reference | Look up exact facts or contracts | Paths, interfaces, units, schedules, scope, and errors |

Use the mode to remove digressions. Link from a procedure to the explanation instead of teaching the architecture between commands. Keep script contracts in reference and execution steps in how-tos. Root and device READMEs are short navigation pages, not copies of their guides.

For a new-machine route, state what was actually tested. Reorganizing historical recipes does not validate them. Do not turn old Docker-group membership, public SSH, floating database images, or broad privilege into a current prerequisite merely because an earlier recipe contains it.

## Write concise, visual guidance

- Lead with the outcome. Use short connected prose, a compact comparison table, or steps when order matters. Cut repeated role descriptions, verification narratives, and schedule tables.
- Use Mermaid when a flow, dependency, or authority boundary is clearer as a diagram. Label arrows. Distinguish permitted traffic from observed dependencies, public requests from deployment control, and backups from recovery tests. Do not add a diagram that only repeats a simple list.
- Keep commands with the host and account that run them. Make placeholders explicit, preserve required context between blocks, and account for the client's shell. A Mac command must not silently rely on Bash-only prompt syntax.
- Preserve literal symbols, error messages, and command text. When moving a page, rewrite actual links and source metadata, not arbitrary parenthesized text or inline code.
- Make optional checks conditional. Unknown DNS policy, for example, cannot support a mandatory known-blocked-domain test.
- Link each fact to its owner instead of maintaining another inventory, task list, or decision record. Keep dated research useful by separating its old observations from current deployment.

## Preserve the evidence boundary

Distinguish user reports, live checks with host and date, researched behavior, proposals, and unknowns. Record that distinction in the owning reference; summaries should link there.

A healthy container does not prove browser access. Timer enablement does not prove a scheduled run. A restored file does not prove application reopening. A working data restore does not prove replacement-host cutover. Keep each acceptance claim as narrow as the evidence.

When implementation changes, update the operating guide and contract, then reconcile affected facts and OKF. Prepared code is not deployed code. Put outstanding installation or recovery checks in their existing owner. Preserve accepted scope exclusions and deferred work rather than silently expanding them.

For recovery guides, identify required credentials, persistent data, compatible versions, and independent access. Prefer private staging over overwriting live state. Do not imply that GitHub preserves uncommitted or unpushed work. Keep secrets and raw private evidence outside Git.

## Review the result

1. Read the changed page as the intended operator. Can they identify the goal, machine, inputs, expected result, failure boundary, and next step without following every reference?
2. Search for repeated claims and tables. Keep each maintained fact or procedure in one owner. Update nearby navigation and callers after moves; retain a short compatibility link only when it helps existing readers.
3. Check local links, heading anchors, and OKF source paths. Inspect literal errors and commands after automated moves. Do not rewrite valid repository links solely to silence an OKF tool's outside-bundle warnings.
4. Parse changed Mermaid diagrams and check executable shell/Python examples without running live installation or destructive commands. Historical placeholders are not runnable validation targets. State what was not checked.
5. Follow the OKF skill's validation and neighborhood checks after concept edits. Tool validation checks structure; it does not certify the facts or deployment.
6. Review a substantial rewrite independently when delegation is authorized, with distinct attention to procedures, duplication, and ownership. Fix concrete findings; do not create a review report or activity log for routine work.

Summarize what changed and any material uncertainty. Commit, push, open a PR, or change a live machine only within the user's authorized scope.
