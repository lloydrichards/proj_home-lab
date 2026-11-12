# admin-lab

The Pi 4 runs Pi-hole for DNS filtering. Hardware and naming facts belong in the [inventory](../_reference/inventory.md). Addresses, permissions, service versions, and dated checks belong in the [service register](../_reference/services.md).

## Understand and check DNS

- [How the DNS service fits into the lab](explanations/dns-service.md).
- [Set up Pi-hole as the LAN DNS server](how-to/set-up-pihole.md).
- [Check DNS, container health, and dashboard access](how-to/check-dns.md).
- [Connect with private SSH](../../docs/how-to/connect-with-ssh.md).
- [Review the dated image-maintenance investigation](research/image-maintenance.md).

The shared [architecture](../../docs/explanations/architecture.md), [security](../../docs/explanations/security-and-access.md), and [recovery](../../docs/explanations/backup-and-recovery.md) explanations describe the wider lab.

## Rebuild boundary

The router now advertises Pi-hole through IPv4 DHCP, and dashboard login works. IPv6 still advertises the router DNS resolver and can bypass filtering. Lloyd chose to stop before router console changes. The service register owns the dated evidence.

There is no verified rebuild or configuration-restore recipe for this Pi. Persistent mounts, complete client dependencies, and restore compatibility need inspection before replacement. The separate Pi 4 PostgreSQL service also has unknown consumers and backup coverage.

The historical Pi 5 recipes do not establish admin-lab's configuration. Keep working DNS and independent maintenance access available while investigating. The service register owns these gaps, so this page does not maintain another task list.

## Choices and sources

The [Pi-hole concept](../../.okf/technologies/pi-hole.md) connects the evidence. The [hosting boundary](../../.okf/decisions/keep-pi-hosting-separate.md) and [recovery-first decision](../../.okf/decisions/recovery-before-reliance.md) explain why DNS changes stay separate from HP development setup. Return to [all devices](../../README.md).
