# Pi-hole image-maintenance evidence

This investigation was checked on 9 November 2026. It is dated evidence, not a current upgrade recommendation or proof that the installed image changed.

## Component versions do not identify the image

[Upstream latest](https://api.github.com/repos/pi-hole/docker-pi-hole/releases/latest) reported [Docker tag 2026.10.1](https://github.com/pi-hole/docker-pi-hole/releases/tag/2026.10.1). Its release notes refresh Alpine to 3.24.3 for security fixes. That does not establish a specific exploitable CVE on this host.

Recorded Core 6.5, Web 6.6.1, and FTL 6.8 matched their upstream latest releases at that check. Component versions do not establish container base-image freshness. The deployed image tag and digest remain unknown.

The reviewed multi-platform digest was `sha256:30f803ad5dd60ff96cc0a63008a2e9271af481c1b0399a182192b2e91152c1f9`, including `linux/arm64`. Tag 2026.10.1 was a conditional target then. Recheck the release and platform before any later maintenance; do not downgrade a newer installed image to match this note.

## Evidence needed before replacement

The [read-only service checks](../how-to/check-dns.md) identify the running container's image reference and ID. A floating tag alone cannot identify its contents. A manifest query can inspect a candidate without pulling layers:

```bash
	sudo docker manifest inspect pihole/pihole:2026.10.1
```

The command uses the historical candidate above. It is not an instruction to deploy that version.

Safe replacement also needs known DNS consumers, upstream DNS, DHCP ownership, and independent maintenance access. Configuration and volume recovery must be tested first. Retain the old image and private launch settings. An image rollback alone does not reverse a data migration.

Any future maintenance procedure must preserve mounts, ports, capabilities, and DHCP settings, then test DNS, filtering, dashboard access, and container health separately. No such upgrade or complete recovery procedure has been verified here. The [service register](../../_reference/services.md) owns installed-state evidence and remaining gaps.
