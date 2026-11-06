---
type: Decision
title: "Choose unencrypted unattended boot"
description: "A user-confirmed boot preference with physical-access consequences."
status: draft
sources:
  - id: source-1
    resource: "../../docs/decisions/0001-private-development-host.md"
  - id: source-2
    resource: "../../docs/hp/00-design.md"
  - id: source-3
    resource: "../../docs/research/omarchy-headless.md"
---

# Choose unencrypted unattended boot

The user selected an unencrypted HP installation on 6 November 2026 so restarts do not require a local disk unlock. The preference is confirmed; installation and restart behavior are not verified.

The tradeoff is exposure of SSD contents to someone with physical access. The plan compensates with physical protection, scoped credentials, and encrypted off-machine [backups](../technologies/restic.md "requires alongside"). These measures do not make the SSD encrypted.

Unencrypted storage alone does not establish availability. Firmware AC-loss recovery, Ethernet, network services, sleep policy, and cold boot still need tests. [Omarchy](../technologies/omarchy.md "must configure") and [systemd](../technologies/systemd.md "uses for power and services") settings address parts of that behavior.

Encrypted unlock alternatives in the research preserve the reasoning behind the choice. They do not supersede this preference.
