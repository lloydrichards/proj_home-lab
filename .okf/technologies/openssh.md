---
type: Concept
title: "OpenSSH"
description: "Key-based login and selected port forwarding for remote development."
status: draft
sources:
  - id: source-1
    resource: "../../research/private-access.md"
---

# OpenSSH

The HP research proposes ordinary OpenSSH over [Tailscale](tailscale.md "runs over"), with separate maintenance and coding accounts. Its example disables root and password login while retaining selected local TCP forwarding. These are proposed settings, not observed configuration.

For browser previews, SSH forwards a loopback listener on the laptop to a loopback service on the HP. Inspect the actual listener and keep application authentication; another local process may still reach that service.

The access research recommends validating syntax and effective settings before reload and checking a fresh second login while recovery access remains open. This is the basis of the [access-change learning](../learnings/access-changes-need-recovery.md "requires").

Do not forward the laptop's SSH agent into the coding account. Use narrowly scoped server credentials as part of [agent isolation](agent-isolation.md "protects credentials within").
