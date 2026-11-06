---
type: Learning
title: "Measure tools before increasing agent concurrency"
description: "Cloud-hosted inference leaves build and browser costs on the HP."
status: draft
sources:
  - id: source-1
    resource: "../../docs/hp-preparation.md"
  - id: source-2
    resource: "../../docs/research/remote-coding.md"
---

# Measure tools before increasing agent concurrency

The proposed HP workflow starts with at most two heavy build or browser-test jobs while measuring CPU, RAM, disk use, and build time. The research estimates for connected conversations are planning experiments, not benchmark results.

[Pi](../technologies/pi-coding-agent.md "applies to") and [OpenCode](../technologies/opencode.md "applies to") may wait for remote model responses, while their compilers, tests, browsers, and language servers consume local resources. Counting agent conversations alone does not predict the load.

Measure heavy jobs separately from connected conversations and increase concurrency only after checking resource use. No delivered-hardware measurements are recorded.
