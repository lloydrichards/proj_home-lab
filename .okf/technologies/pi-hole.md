---
type: Concept
title: "Pi-hole"
description: "User-reported DNS service on the Raspberry Pi 4."
status: draft
sources:
  - id: source-1
    resource: "../../reference/services.md"
  - id: source-2
    resource: "../../reference/inventory.md"
---

# Pi-hole

The user reports Pi-hole running on a Raspberry Pi 4. There is no Pi-hole setup guide or successful live inspection in the repository yet. RAM, OS, storage, service version, upstream DNS, and client settings remain unknown.

Before a restart, migration, or DNS change, establish whether it also supplies DHCP and which devices depend on it. In particular, the HP's actual DNS dependency must be observed rather than inferred from the two devices sharing a lab.

The [keep-existing-hosting decision](../decisions/keep-pi-hosting-separate.md "needs dependency review alongside") avoids treating the arriving HP as an automatic reason to move services. Record the Pi-hole setup and recovery procedure after inspection. The [recovery-first rule](../decisions/recovery-before-reliance.md "should guide future service changes through") provides a pattern for planning that work.
