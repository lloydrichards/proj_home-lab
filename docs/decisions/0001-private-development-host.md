# Decision 0001: Keep remote development private

Status: architecture proposed; Pi coding agent identity and unencrypted unattended-boot preference confirmed by the user on 6 November 2026. Installation remains unverified.

Date: 6 November 2026.

## Context

The HP runs remote coding sessions, builds, and tests. Omarchy provides a local desktop, but most access is headless. The Pi already hosts Coolify. Principal risks are leaked credentials, unsafe agent tool execution, accidental service exposure, and loss of access after an update or reboot.

## Decision

Use bare-metal Omarchy, Ethernet, Tailscale networking, and ordinary OpenSSH keys. Run interactive agents inside tmux under an account without sudo or Docker access. Bind browser interfaces to loopback and forward selected ports from the laptop. Use the user-selected unencrypted disk for unattended restarts. Keep off-machine backups encrypted and limit physical access to the rack.

Do not add router forwarding, Tailscale Funnel, public agent APIs, public SSH, or a public management dashboard. Keep existing Pi deployments separate.

## Consequences

The laptop needs Tailscale. Coding does not require the graphical desktop. An unencrypted SSD can be read by someone with physical access; unattended startup still requires firmware, service, and network testing. All agents under one Unix account share its readable files and credentials. A backup destination and local recovery access are needed before relying on the host.

## Deferred alternatives

- Tailscale SSH: reconsider with its separate policy and recovery tests.
- Public Cloudflare or Funnel access: only for a selected application with authentication and an exposure review.
- Per-agent VMs: useful for untrusted work, after selecting an isolation model and measuring resources.
- A server distribution: operationally simpler, but the user explicitly wants Omarchy.
