# Documentation workflow

Use this repository for the whole lab. Keep a running system's observed state separate from a proposed setup.

| Material | Location | What belongs here |
|---|---|---|
| Devices and services | `reference/` | Current inventory, dependencies, BOM, and verification gaps |
| Setup and operations | `hp/` and existing Pi guides | Repeatable procedures with checks and recovery steps |
| Concepts and technologies | `../.okf/` | Short explanations, relationships, lab relevance, and links to evidence |
| Research | `research/` | Questions, primary sources, findings, alternatives, and open questions |
| Decisions | `decisions/` | Chosen approach, reasons, consequences, and superseded choices |
| Logs and learnings | `logs/` | Dated changes, incidents, outcomes, and lessons |
| Configuration | `../config/` | Reviewed examples without secrets |
| Private evidence | `../local/` | Raw SSH output and private details, ignored by Git |

## Record new work

1. Start a research note for an unresolved question. Record source URLs, the date checked, and release-sensitive details.
2. Add or update a concept when the finding is useful beyond that investigation. Link it to related concepts and the research note.
3. Record a decision when an option is selected. A researched option does not mean it is installed.
4. Update a guide when there is a repeatable procedure. Include verification and recovery steps.
5. After a real change, add a dated log entry and update the inventory or service register from observed evidence.
6. Validate the OKF bundle after concept edits.

Use [the research template](templates/research.md) and [the log template](templates/log-entry.md). Use `draft` for unsettled OKF concepts and `stable` for settled explanations. These statuses describe knowledge maturity, not deployment or live verification. State deployment and evidence explicitly in the text.

The repository includes the [OKF maintenance skill](../.agents/skills/okf/SKILL.md). Follow [AGENTS.md](../AGENTS.md) to keep concepts aligned with research, setup changes, decisions, and learnings. The [organization research](research/knowledge-organization.md) records the format and validation approach.
