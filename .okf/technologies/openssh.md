---
type: Concept
title: "OpenSSH"
description: "Key-based login and selected port forwarding for remote development."
status: draft
sources:
  - id: live-access
    resource: "../../devices/_reference/services.md"
  - id: source-1
    resource: "../../research/private-access.md"
  - id: ssh-guide
    resource: "../../devices/_reference/ssh-access.md"
---

# OpenSSH

Account-local `Host` aliases with an explicit Tailscale IP in `HostName` make SSH shortcuts independent of short-name DNS. They do not configure system DNS. Each source account needs its own configuration and key authorization; installing one source key does not create reverse access. The shared guide records setup, host verification, and fresh-login checks. On 10 November 2026, `coder` on home-lab passed key logins to admin-lab over Tailscale and remote-lab over LAN. Remote-lab's Tailscale endpoint still authenticates through Tailscale SSH, so a login there does not prove OpenSSH public-key acceptance.

The HP research proposes ordinary OpenSSH over [Tailscale](tailscale.md "runs over"), with separate maintenance and coding accounts. Its example disables root and password login while retaining selected local TCP forwarding. The HP installed configuration and successful logins are recorded in the service register; effective privileged settings still need a successful HP audit. Pi 4 effective settings disable passwords, while Pi 5 permits them. Both Pis permit root key login.

For browser previews, SSH forwards a loopback listener on the laptop to a loopback service on the HP. Inspect the actual listener and keep application authentication; another local process may still reach that service.

The access research recommends validating syntax and effective settings before reload and checking a fresh second login while recovery access remains open. Disable connection sharing for that check so it cannot reuse an authenticated session. Switching a Tailscale endpoint between Tailscale SSH and ordinary OpenSSH changes its host identity; verify the replacement through trusted access and update only the affected client trust entry. Rollback must restore trust for the returning identity. The shared SSH guide records the procedure and upstream sources. This is the basis of the [access-change learning](../learnings/access-changes-need-recovery.md "requires").

Do not forward the laptop's SSH agent into the coding account. Use narrowly scoped server credentials as part of [agent isolation](agent-isolation.md "protects credentials within").
