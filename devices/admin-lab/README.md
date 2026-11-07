# admin-lab

The Raspberry Pi 4 is the user-reported Pi-hole host. `admin-lab` is its planned hostname, not a verified access address. SSH details, hardware configuration, OS, service version, upstream DNS, and DHCP ownership remain unknown.

## Start here

Establish whether Pi-hole supplies DHCP and which devices depend on it before a restart, rename, or DNS change. The [service register](../reference/services.md) owns the inspection gaps and dependency guidance. The [inventory](../reference/inventory.md) owns hardware and planned-name facts; purchases stay in the [BOM](../reference/bom.md).

There is no verified Pi-hole setup or recovery recipe yet. Record the repeatable procedure here after inspecting the device. The historical Pi 5 recipes in [remote-lab](../remote-lab/README.md) do not establish this Pi's configuration.

## Choices and knowledge

The [Pi-hole concept](../.okf/technologies/pi-hole.md) records the current knowledge and questions. The shared [hosting boundary](../.okf/decisions/keep-pi-hosting-separate.md) and [recovery-first decision](../.okf/decisions/recovery-before-reliance.md) guide future changes.

Add device-specific decisions under `.okf/decisions/admin-lab/` when a real choice needs recording, then link them here. Return to [all devices and lab records](../README.md).
