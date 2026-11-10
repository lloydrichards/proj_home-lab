---
type: Concept
title: "Tailscale"
description: "Private connectivity, authentication modes and access checks across the lab."
status: draft
sources:
  - id: live-access
    resource: "../../devices/_reference/services.md"
  - id: source-1
    resource: "../../research/private-access.md"
  - id: ssh-guide
    resource: "../../devices/_reference/ssh-access.md"
---

# Tailscale

The lab uses Tailscale to connect the laptop to the server without publishing administration endpoints. The HP joined Tailscale on 9 November 2026. Lloyd confirmed Mac SSH through its private address; assistant access as `lloyd` also passed. A monitor-free cold start passed for both accounts. Access-policy denial and device-expiry checks remain pending. The service register owns addresses and accounts.

Tailscale supplies connectivity and tailnet access policy. [OpenSSH](openssh.md "authenticates Linux logins over") separately authenticates the laptop key and selects the Linux account. Tailscale SSH is a different mode with separate identity and policy behavior; the HP baseline leaves it disabled. Pi 4 also uses ordinary OpenSSH, while Pi 5 currently enables Tailscale SSH.

The access research warns that a narrow new grant does not cancel an existing broad allow. Review effective access across existing ACLs and grants, and test denial from an unauthorized device. Device expiry and recovery also need an explicit plan.

The pending maintenance guidance in source-1 distinguishes the stable **1.104.5** target checked on 9 November 2026 from installed versions. Prioritize checking Pi 5 because it enables Tailscale SSH; HP uses ordinary OpenSSH. Apply HP updates through Omarchy with independent recovery access. This research does not record a deployed update.

Tailscale Serve is a researched option for private HTTPS. Funnel publishes publicly and is excluded from the [private development decision](../decisions/home-lab/private-development.md "implements"). Neither private transport nor a policy rule replaces [application authentication](../learnings/private-network-is-not-isolation.md "does not replace").

On 9 November 2026, LAN inspection found Pi 5 Tailscale logged out and Pi 4 without a host installation. Pi 4 installation and daemon enablement completed; both Pis subsequently signed in. Pi 4 passed fresh private SSH; Pi 5 also passed after Lloyd completed the additional Tailscale SSH identity check. Pi 4 settings disable DNS acceptance to avoid changing its resolver. The Mac client was stopped; reconnecting it restored fresh HP logins for both accounts. A running server daemon alone does not prove client connectivity or successful enrollment. The service register cited above owns current access facts.

Both Pi system names and Tailscale DNS names now match the notebook names. Fresh SSH through `admin-lab` and `remote-lab` passed on 9 November 2026. Name preference changes alone were not immediate proof of advertised DNS; the later private-name login established it.

On 10 November 2026, the Pi short names resolved through MagicDNS from home-lab, while the Mac reported name-resolution failures and succeeded by Tailscale IP. SSH aliases with explicit private IPs avoid this client DNS dependency without changing Pi-hole's resolver configuration. Lloyd reported the Mac shortcut setup worked; a full source-to-destination access matrix remains untested. The shared SSH guide separates these shortcuts from key authorization and Tailscale SSH identity checks.
