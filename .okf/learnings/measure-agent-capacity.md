---
type: Learning
title: "Measure tools before increasing agent concurrency"
description: "Cloud-hosted inference leaves build and browser costs on the HP."
status: draft
sources:
  - id: source-1
    resource: "../../docs/devices/home-lab/preparation.md"
  - id: source-2
    resource: "../../docs/research/remote-coding.md"
  - id: vm-research
    resource: "../../docs/research/remote-agent-tools.md"
---

# Measure tools before increasing agent concurrency

The proposed HP workflow starts with at most two heavy build or browser-test jobs while measuring CPU, RAM, disk use, and build time. The research estimates for connected conversations are planning experiments, not benchmark results.

[Pi](../technologies/pi-coding-agent.md "applies to") and [OpenCode](../technologies/opencode.md "applies to") may wait for remote model responses, while their compilers, tests, browsers, and language servers consume local resources. Counting agent conversations alone does not predict the load.

Measure heavy jobs separately from connected conversations and increase concurrency only after checking resource use. No delivered-hardware measurements are recorded.

HP VMs are deferred under the chosen local-devvm approach. If revisited, the earlier planning estimate for the reported 32 GB, six-core HP was two active project VMs at 8 GiB each, with a possible third light VM after measurements. An alternative is three guests at 6 GiB each if their real workloads fit. Leave roughly 8 GiB for Omarchy and host services, plus room for virtualization overhead. These are starting budgets, not measured capacity or guaranteed memory reservations. Stop unused guests and schedule heavy builds separately. Virtual CPUs share the same physical processor; allocating more does not create more cores.
