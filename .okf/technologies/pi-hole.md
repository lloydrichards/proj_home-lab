---
type: Concept
title: "Pi-hole"
description: "User-reported DNS service on the Raspberry Pi 4."
status: draft
sources:
  - id: source-1
    resource: "../../devices/_reference/services.md"
  - id: source-2
    resource: "../../devices/_reference/inventory.md"
---

# Pi-hole

The user reports Pi-hole running on a Raspberry Pi 4. SSH inspection on 9 November 2026 confirmed a healthy Pi-hole Docker container and a successful DNS query from the Mac. The inventory owns observed hostname, address and storage. Hardware and OS have been inspected; the service register records Pi-hole versions and disabled Pi-hole DHCP. Upstream DNS, network DHCP ownership and client settings remain unknown.

Before a restart, migration, or DNS change, confirm network DHCP ownership and which devices depend on DNS. In particular, the HP's actual DNS dependency must be observed rather than inferred from the two devices sharing a lab.

The [keep-existing-hosting decision](../decisions/keep-pi-hosting-separate.md "needs dependency review alongside") avoids treating the arriving HP as an automatic reason to move services. Record the Pi-hole setup and recovery procedure after inspection. The [recovery-first rule](../decisions/recovery-before-reliance.md "should guide future service changes through") provides a pattern for planning that work.
