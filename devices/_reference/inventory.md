# Inventory

Live identifiers, addresses, operating-state checks, and recovery details are kept in ignored `local/configuration/devices/_reference/inventory.md`. Hardware descriptions below are public. See the [documentation privacy policy](../../docs/how-to/keep-local-configuration-private.md).

## HP hardware

| Item | Observed or recorded value | Remaining uncertainty |
|---|---|---|
| HP | EliteDesk 800 G6 Desktop Mini PC; SKU `26L19US#ABA`; board `8711` | Physical mounting and power-adapter details |
| CPU | Intel i5-10500T, 6 cores / 12 threads, VT-x | Diagnostics and sustained-load test pending |
| RAM | 32 GB purchased, 31 GiB usable | Module layout, speed and memory test pending |
| SSD | SK hynix PC711 NVMe 1 TB, 953.9 GiB; firmware 41001131 | SMART passed 9 November; see health summary below |
| Network | Wired Ethernet | Actual interface names, addresses, reservations, and checks are in the private inventory. |
| Rack | DeskPi RackMate T1 recorded | Shelf, fasteners, adapter support and airflow not confirmed |

## HP operating state

Consult the private inventory for current machine-specific details. Device guides describe setup and verification procedures.

## Disk unlock and recovery

Consult the private inventory for current machine-specific details. Device guides describe setup and verification procedures.

## Device names

All three names are applied. The Pi system names were changed at Lloyd's request on 9 November 2026. Both Pi Tailscale DNS names match their system names; fresh SSH through each new name passed.

| Device | Name | Purpose |
|---|---|---|
| HP | `home-lab` | Development and coding agents |
| Pi 5 | `remote-lab` | Existing Coolify hosting |
| Pi 4 | `admin-lab` | Pi-hole and network administration |

Pi services and IP addresses were retained during the rename. A Mac SSH alias is separate from the device's hostname.

## Headless audit results

Consult the private inventory for current machine-specific details. Device guides describe setup and verification procedures.

## Pi operating state

Consult the private inventory for current machine-specific details. Device guides describe setup and verification procedures.

## Pi 4 hardware

Read over SSH on 9 November 2026. Capacities below distinguish the whole device from the mounted filesystem.

| Item | Observed value | Remaining uncertainty |
|---|---|---|
| Board | Raspberry Pi 4 Model B Rev 1.1, ARM64 | Enclosure, cooling and power supply not physically checked |
| CPU | 4 Cortex-A72 cores; configured maximum 1.5 GHz | Sustained performance and thermal throttling not tested |
| RAM | 3.7 GiB usable, consistent with 4 GB model; 199 MiB swap | No memory stress test |
| Network | Wired Ethernet | Actual interface names, addresses, reservations, and checks are in the private inventory. |

## Pi 5 hardware

Read over SSH on 9 November 2026.

| Item | Observed value | Remaining uncertainty |
|---|---|---|
| Board | Raspberry Pi 5 Model B Rev 1.0, ARM64 | Enclosure, cooling and power supply not physically checked |
| CPU | 4 Cortex-A76 cores; configured maximum 2.4 GHz | Sustained performance and thermal throttling not tested |
| RAM | 7.9 GiB usable, consistent with 8 GB model; 199 MiB swap | No memory stress test |
| SSD | KIOXIA EXCERIA G2 NVMe, 931.5 GiB, consistent with 1 TB capacity | Firmware and SMART health not collected; `smartctl` and `nvme` tools absent |
| Network | Wired Ethernet | Actual interface names, addresses, reservations, and checks are in the private inventory. |

Earlier notes name a [Seeed 1 TB SSD](https://www.seeedstudio.com/NVMe-M-2-2280-SSD-1TB-p-5767.html) and an [Argon ONE V3 M.2 NVMe case](https://argon40.com/products/argon-one-v3-m-2-nvme-case). The live SSD identifies as KIOXIA EXCERIA G2. Neither the old purchase identity nor the enclosure can be confirmed from these SSH checks.
