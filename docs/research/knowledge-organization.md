# Organizing the home lab knowledge

Researched 6 November 2026. This is a proposed organization, not evidence of installed services.

## Use Markdown as the knowledge store

Use an Open Knowledge Format bundle under `.okf/` for concepts and technologies. Keep hardware records, installation guides, purchases, and dated operating notes under `docs/`. This is a repository convention chosen for this lab.

OKF v0.2 represents knowledge as Markdown with YAML metadata. A concept needs `type`; `title` and `description` help discovery. Paths without `.md` identify concepts. Its optional lifecycle values are `draft`, `stable`, and `deprecated`. These describe the document's lifecycle, not whether a service is deployed. [OKF specification, sections 2–5](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md)

Record deployment evidence separately in the body. Distinguish user reports, live observations with a date, proposals, and unknowns. A guide does not prove that its instructions have been applied.

## Connect concepts to their evidence

Use file-relative links for relationships such as "runs on", "provides DNS for", or "uses for remote access". This follows the [OKF maintenance skill](https://github.com/lloydrichards/proj_okf-graph/blob/main/apps/okf-graph/src/skills/okf/SKILL.md) and keeps links useful in repository viewers.

Add `sources` entries for the material behind each concept. Keep official product documentation alongside relevant repository records. The CLI's conformance tests show that a source inside the bundle creates a graph edge, while a source outside it does not. Guides outside `.okf/` remain useful citations, but do not become nodes in this graph. [CLI conformance tests](https://github.com/lloydrichards/proj_okf-graph/blob/main/packages/okf/src/conformance/OkfConformance.test.ts)

Keep each durable fact in one owning document. A Coolify concept can explain why it is used and link to the host inventory and installation guide without copying either. Add a concept when a question or relationship needs it, rather than creating empty entries for every possible technology.

Use `verified` only after a human or deterministic process checks the claim. Writing or reading a document is not verification of the running machine. Put unsettled research in `draft`. [OKF specification, section 5](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md)

## Tooling checked locally

The sibling `proj_okf-graph` checkout has CLI package version `0.3.0`, installed dependencies, and a working Bun entry point. No global `okf-graph` command was found. Both `validate --help` and `eval --help` ran successfully on 6 November 2026. This checks command availability, not a home lab bundle.

From this repository, use the existing checkout without installing another package:

```bash
bun run ../proj_okf-graph/apps/okf-graph/src/index.ts validate ./.okf --json
bun run ../proj_okf-graph/apps/okf-graph/src/index.ts eval ./.okf --json
bun run ../proj_okf-graph/apps/okf-graph/src/index.ts graph neighbors ./.okf technologies/coolify --json
```

The final command assumes `.okf/technologies/coolify.md` exists. Validate structure and links before inspecting graph quality. Neither result proves that a technical claim is true. The validation command reports `valid` and `issues` and exits with a failure for an invalid bundle. [Validation implementation](https://github.com/lloydrichards/proj_okf-graph/blob/main/apps/okf-graph/src/commands/validate.ts)

The sibling path is a local convenience. For use on another machine, select and record a released CLI version rather than relying on an unpinned `latest`. The project's [README](https://github.com/lloydrichards/proj_okf-graph/blob/main/README.md) describes installation and `skill write`, which installs the supplied maintenance skill into a repository.

## Keep the first bundle small

Start with the technologies already discussed: Coolify, Cloudflare Tunnel, Pi-hole, private remote access, and persistent coding sessions. Link them to current and planned hosts. Keep pending research questions visible in the relevant concept. Record a comparison or decision when it changes a setup choice.

Keep receipts, private addresses, and raw inspection output in ignored local storage when appropriate. Publish reviewed inventory facts and a short dated observation with its source. A database server or separate graph service can wait until Markdown search and the CLI no longer answer the questions we actually ask.
