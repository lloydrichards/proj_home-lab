# Inventory and verification record

The HP is purchased and arriving soon. The user reports two running Pis: one with Coolify and a Cloudflare tunnel, and a Raspberry Pi 4 with Pi-hole. Live inspection is pending. See the [service register](services.md) and [bill of materials](bom.md).

Reviewed 6 November 2026. Purchased or reported specifications are not measurements of the delivered machine.

| Item | Recorded value | Still to verify |
|---|---|---|
| HP | EliteDesk 800 G6 Desktop Mini | Product number and firmware |
| CPU | i5-10500T, six cores, twelve threads | `lscpu` |
| RAM | 32 GB | Module count, speed, memory test |
| SSD | 1 TB | Model, interface, health, capacity |
| Network | Ethernet; purchased offer excluded Wi-Fi | Interface name and link speed |
| Rack | DeskPi RackMate T1 | Shelf, fasteners, cable clearance |
| Client | MacBook, user confirmed 6 November 2026 | Model, macOS, SSH and Tailscale versions |
| Coolify host | Raspberry Pi 5, user identified 7 November 2026; RAM unresolved | Model, RAM, OS, storage, and running configuration |
| Historical Pi storage | [1 TB NVMe M.2 2280 SSD](https://www.seeedstudio.com/NVMe-M-2-2280-SSD-1TB-p-5767.html) | Current use, model, capacity, and health |
| Historical Pi enclosure | [Argon ONE V3 M.2 NVME case](https://argon40.com/products/argon-one-v3-m-2-nvme-case) | Current use and cooling configuration |
| DNS host | Raspberry Pi 4 with Pi-hole, user reported | RAM, OS, storage, DNS upstream, and DHCP role |

HP's [manufacturer datasheet](https://cdn.cs.1worldsync.com/syndication/feeds/hp/inline-content/GA/A/C/F/9/F/ACF9F36F11E43449CA2400614E308C88AF3ECC2E_source.PDF) describes two memory sockets, up to 64 GB RAM, and storage options. Refurbished modules and storage may differ from the original configuration.

The Pi SSD and enclosure were listed in the original repository overview. Their current use remains unverified. Record actual versions, hardware health, and access details as we inspect each host; keep private raw output under ignored `local/`.

## Planned device names

Proposed on 7 November 2026 from Lloyd's `home_lab`, `remote_lab`, and `admin_lab` naming idea. Use hyphens for OS hostnames and DNS. These names have not been applied or live-verified.

| Device | Planned hostname | Meaning |
|---|---|---|
| HP EliteDesk | `home-lab` | Main home development and agent machine |
| Raspberry Pi 5, user identified | `remote-lab` | Existing app hosting through Coolify and Cloudflare Tunnel |
| Raspberry Pi 4 | `admin-lab` | Existing Pi-hole and network administration |

`remote-lab` describes the Pi's hosted services; the HP also supports remote access. If names should describe only the current service, `apps-lab` and `dns-lab` are more explicit Pi alternatives. The guide uses Lloyd's preferred scheme with hyphens for now.

Set the HP name before Tailscale enrollment. Keep the OS hostname, router reservation label, and Tailscale machine name consistent where those records exist. A Mac SSH alias is a client shortcut and can point at the verified Tailscale IP or full MagicDNS name.

Rename the running Pis only during a separate maintenance session. First inspect their current names and dependencies, especially Pi-hole DHCP and local DNS entries, Coolify URLs, monitoring, SSH configuration, and tunnel destinations. Keep current access working until the replacement name resolves. Changing a hostname does not migrate a service or create a DNS record by itself.

References: [systemd hostnames](https://www.freedesktop.org/software/systemd/man/258/hostname.html) and [Tailscale machine names](https://tailscale.com/docs/concepts/machine-names).
