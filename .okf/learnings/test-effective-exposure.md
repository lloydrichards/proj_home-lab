---
type: Learning
title: "Test effective network exposure"
description: "Declared firewall intent does not establish service reachability."
status: draft
sources:
  - id: source-1
    resource: "../../research/private-access.md"
  - id: source-2
    resource: "../../research/remote-coding.md"
  - id: source-3
    resource: "../../devices/home-lab/preparation.md"
---

# Test effective network exposure

The remote-coding and access research calls for checking host listeners, container port mappings, firewall rules, tailnet policy, and reachability from other devices. Include IPv6 and repeat after material service or network changes.

[Docker](../technologies/docker.md "requires checking mappings for") publishes ports through its own networking rules, so an ordinary UFW deny is insufficient evidence. [Tailscale](../technologies/tailscale.md "requires checking effective policy for") grants must be reviewed with existing broad rules.

Loopback publication reduces network exposure but does not replace authentication against local clients. These are proposed checks, not recorded test results. They support the [private-development decision](../decisions/home-lab/private-development.md "validates").
