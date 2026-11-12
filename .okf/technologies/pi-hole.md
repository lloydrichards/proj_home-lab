---
type: Concept
title: "Pi-hole"
description: "DNS filtering, dependency discovery, and maintenance boundaries on admin-lab."
status: draft
sources:
  - id: source-1
    resource: "../../devices/_reference/services.md"
  - id: source-2
    resource: "../../devices/_reference/inventory.md"
  - id: image-maintenance
    resource: "../../devices/admin-lab/research/image-maintenance.md"
  - id: dns-explanation
    resource: "../../devices/admin-lab/explanations/dns-service.md"
  - id: pihole-setup
    resource: "../../devices/admin-lab/how-to/set-up-pihole.md"
  - id: service-checks
    resource: "../../devices/admin-lab/how-to/check-dns.md"
---

# Pi-hole

Pi-hole runs on admin-lab, the Raspberry Pi 4. The ignored local service register owns exact addresses, versions, deployment paths, and dated checks. Public guides use example values; the public register summarizes service roles. On 12 November 2026, Lloyd recovered a stale DHCP lease after replacing the router. The Fibre X6 owns network DHCP; Pi-hole DHCP was disabled at inspection. Pi-hole's configured upstreams are Cloudflare DNS. Explicit DNS tests and Mac dashboard login passed.

The router advertises Pi-hole through IPv4 DHCP, but its IPv6 router advertisements and DHCPv6 still advertise the router resolver. Unique direct router queries were absent from Pi-hole's refreshed log. Working IPv4 DNS does not establish complete network filtering. A VPN resolver override also prevented normal Mac queries from reaching Pi-hole earlier in the investigation.

Lloyd chose on 12 November to stop at this partial setup and declined router console writes. Preserve that boundary. The console investigation was read-only; proposed IPv6 changes were not applied. Revisit them only if Lloyd chooses to resume the work. The setup guide records the accepted web-form configuration and client checks.

Before a restart or migration, inspect persistent configuration and client dependencies and keep independent maintenance access. A tested Pi-hole restore is still missing.

The image-maintenance source separates current Pi-hole component versions from the unknown deployed image digest. Docker **2026.10.1**, checked on 9 November 2026, is a conditional base-image maintenance target, not an observed update. Backups and DNS dependency checks must precede replacement.

The [keep-existing-hosting decision](../decisions/keep-pi-hosting-separate.md "needs dependency review alongside") keeps DNS and hosting changes separate from HP development setup. The device explanation separates container health, explicit resolver tests, and dashboard reachability. Its checks distinguish resolver advertisement, explicit reachability, and normal client queries. A full rebuild procedure still needs persistent-data inspection and a tested configuration restore. The [recovery-first rule](../decisions/recovery-before-reliance.md "should guide future service changes through") provides a pattern for planning that work.
