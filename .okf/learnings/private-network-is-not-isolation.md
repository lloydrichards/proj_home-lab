---
type: Learning
title: "Private networking does not isolate agent tools"
description: "Network reachability, service authentication, and OS permissions solve different problems."
status: draft
sources:
  - id: source-1
    resource: "../../research/remote-coding.md"
  - id: source-2
    resource: "../../home-lab/preparation.md"
---

# Private networking does not isolate agent tools

A private network controls who can reach a service. Service authentication controls who can use it. Operating-system permissions constrain what its processes can access. Passing one check does not establish the others.

The HP plan combines [Tailscale](../technologies/tailscale.md "controls reachability through"), authenticated [OpenSSH](../technologies/openssh.md "controls login through"), and a restricted coding account. [Agent isolation](../technologies/agent-isolation.md "controls tool authority through") remains necessary even when all administration is private.

Loopback binding also leaves access possible from local processes. Keep authentication on agent APIs. This is a conclusion from the security research, not a completed penetration test.
