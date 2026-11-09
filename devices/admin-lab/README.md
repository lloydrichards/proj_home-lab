# admin-lab

The Raspberry Pi 4 runs Pi-hole. `admin-lab` is its applied system and Tailscale name.

SSH inspection on 9 November 2026 confirmed hostname `admin-lab`, access as `lloyd@192.168.8.138`, a healthy Pi-hole Docker container, and a successful DNS query. Debian 12 and Pi-hole versions are now recorded in the service register. Pi-hole DHCP is disabled; network DHCP ownership and upstream DNS remain unknown. Tailscale sign-in and fresh private SSH as `lloyd` passed. Current addresses live in the service register.

## Start here

Establish which devices depend on Pi-hole and who supplies network DHCP before a restart, rename, or DNS change. The [service register](../_reference/services.md) owns the inspection gaps and dependency guidance. The [inventory](../_reference/inventory.md) owns hardware and naming facts; purchases stay in the [BOM](../_reference/bom.md).

There is no verified Pi-hole setup or recovery recipe yet. Record the repeatable procedure here after inspecting the device. The historical Pi 5 recipes in [remote-lab](../remote-lab/README.md) do not establish this Pi's configuration.

## Choices and knowledge

The [Pi-hole concept](../../.okf/technologies/pi-hole.md) records the current knowledge and questions. The shared [hosting boundary](../../.okf/decisions/keep-pi-hosting-separate.md) and [recovery-first decision](../../.okf/decisions/recovery-before-reliance.md) guide future changes.

Add device-specific decisions under `.okf/decisions/admin-lab/` when a real choice needs recording, then link them here. Return to [all devices and lab records](../../README.md).
