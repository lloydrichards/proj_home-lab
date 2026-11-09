---
type: Decision
title: "Use TPM for unattended boot"
description: "Installed TPM disk unlock with password recovery and remaining recovery checks."
status: draft
sources:
  - id: maintenance-guide
    resource: "../../../research/backups.md"
  - id: source-1
    resource: "../../../devices/home-lab/preparation.md"
  - id: installed-inventory
    resource: "../../../devices/_reference/inventory.md"
  - id: tpm-research
    resource: "../../../devices/home-lab/research/tpm-unlock.md"
  - id: source-3
    resource: "../../../devices/home-lab/research/omarchy.md"
---

# Use TPM for unattended boot

On 9 November 2026, Lloyd chose TPM automatic unlock for the installed encrypted HP disk, replacing the earlier unencrypted-install preference. Keep the working disk password as recovery. A monitor-free cold startup passed: both `lloyd` and `coder` authenticated over Tailscale without local input. The inventory owns the observed configuration and test results.

The TPM enrollment binds to PCR 7 while Secure Boot is disabled. This supports unattended startup and keeps an SSD removed from the HP encrypted. It does not authenticate the boot software against whole-machine physical tampering. Stronger boot integrity would require a separately maintained Secure Boot and measured-boot policy; see the TPM research.

Firmware changes can prevent automatic unlock. Keep console access and the disk passphrase available, preserve password slots, and test unattended startup after boot-related updates. Local recovery copies do not replace off-machine [backups](../../technologies/restic.md "requires alongside").

[Omarchy](../../technologies/omarchy.md "must configure") and [systemd](../../technologies/systemd.md "uses for power and services") provide the boot and service integration. Overnight idle availability, AC-loss recovery, and off-machine recovery copies remain open in the preparation checklist.
