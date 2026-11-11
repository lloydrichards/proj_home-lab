# admin-lab

The Raspberry Pi 4 runs Pi-hole. `admin-lab` is its applied system and Tailscale name.

SSH inspection on 9 November 2026 confirmed hostname `admin-lab`, access as `lloyd@192.168.8.138`, a healthy Pi-hole Docker container, and a successful DNS query. Debian 12 and Pi-hole versions are now recorded in the service register. Pi-hole DHCP is disabled; network DHCP ownership and upstream DNS remain unknown. Tailscale sign-in and fresh private SSH as `lloyd` passed. Current addresses live in the service register.

Since 10 November, human maintenance as `lloyd` requires password-authenticated sudo, with no direct Docker group access in fresh sessions. Use `sudo docker` when needed. Root SSH was disabled on 11 November; fresh Mac lloyd login and sudo checks passed. See [permissions and checks](../_reference/services.md#pi-maintenance-permissions).

Portainer was stopped with automatic restart disabled on 11 November 2026. Application containers stayed running. Its data remains available for [recovery](../_reference/services.md#portainer-retirement). Lloyd reports that Pi-hole browser access is currently unavailable and has deferred investigation until the new network is ready; container health alone does not verify DNS or browser access.

## Start here

Establish which devices depend on Pi-hole and who supplies network DHCP before a restart, rename, or DNS change. The [service register](../_reference/services.md) owns the inspection gaps and dependency guidance. The [inventory](../_reference/inventory.md) owns hardware and naming facts; purchases stay in the [BOM](../_reference/bom.md).

There is no verified Pi-hole setup or recovery recipe yet. Record the repeatable procedure here after inspecting the device. The historical Pi 5 recipes in [remote-lab](../remote-lab/README.md) do not establish this Pi's configuration.

## Pending Pi-hole image freshness check

On **9 November 2026**, [upstream latest](https://api.github.com/repos/pi-hole/docker-pi-hole/releases/latest) reported [Docker tag 2026.10.1](https://github.com/pi-hole/docker-pi-hole/releases/tag/2026.10.1). Its release notes refresh Alpine to **3.24.3** for security fixes; this is not evidence of a specific exploitable CVE on this host. Recorded Core **6.5**, Web **6.6.1** and FTL **6.8** already match their upstream latest releases, but do not establish the container's base-image freshness. The deployed image tag and digest remain unknown; **2026.10.1 is a conditional target, not a confirmed upgrade or deployment**.

Before any separately authorized restart:

1. Identify the Pi-hole container with `docker ps --format '{{.Names}}\t{{.Image}}\t{{.Status}}'`, then inspect only its image reference and ID with `docker inspect --format '{{.Config.Image}} {{.Image}}' CONTAINER_NAME`. Avoid full inspection output containing secrets.
2. Compare its image digest with the target; do not infer freshness from an installed component version or a floating tag. `docker manifest inspect pihole/pihole:2026.10.1` can recheck platform support without pulling layers. The reviewed multi-platform digest is `sha256:30f803ad5dd60ff96cc0a63008a2e9271af481c1b0399a182192b2e91152c1f9`, including **linux/arm64**.
3. Establish DNS consumers, upstream DNS, DHCP ownership and independent access. Save and test recovery for configuration and volumes; retain the old image ID and private launch settings. An image rollback alone does not reverse a data migration.
4. If the deployed image is older, use the explicit target tag or digest in its owning deployment configuration during a DNS maintenance window. Keep mounts, ports, capabilities and DHCP settings unchanged. If already current, leave it alone; if newer, do not downgrade.
5. Check container health, dashboard access and `dig @192.168.8.138 example.com` from a client, plus a known blocked-domain lookup. Recover the saved image and compatible data if checks fail.

No DNS service or host was changed by this notebook review.

## Choices and knowledge

The [Pi-hole concept](../../.okf/technologies/pi-hole.md) records the current knowledge and questions. The shared [hosting boundary](../../.okf/decisions/keep-pi-hosting-separate.md) and [recovery-first decision](../../.okf/decisions/recovery-before-reliance.md) guide future changes.

Add device-specific decisions under `.okf/decisions/admin-lab/` when a real choice needs recording, then link them here. Return to [all devices and lab records](../../README.md).
