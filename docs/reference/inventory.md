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
| Client | Laptop | OS, SSH and Tailscale versions |
| Coolify host | Earlier notes identify Raspberry Pi 5, RAM unresolved | Model, RAM, OS, storage, and running configuration |
| Historical Pi storage | [1 TB NVMe M.2 2280 SSD](earlier-pi-overview.md#hardware) | Current use, model, capacity, and health |
| Historical Pi enclosure | [Argon ONE V3 M.2 NVME case](earlier-pi-overview.md#hardware) | Current use and cooling configuration |
| DNS host | Raspberry Pi 4 with Pi-hole, user reported | RAM, OS, storage, DNS upstream, and DHCP role |

HP's [manufacturer datasheet](https://cdn.cs.1worldsync.com/syndication/feeds/hp/inline-content/GA/A/C/F/9/F/ACF9F36F11E43449CA2400614E308C88AF3ECC2E_source.PDF) describes two memory sockets, up to 64 GB RAM, and storage options. Refurbished modules and storage may differ from the original configuration.

## Record locally on the HP

Save output in ignored `local/` files or a private note. Review serial numbers, addresses, and usernames before sharing.

```bash
hostnamectl
lscpu
free -h
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS,MODEL
ip -brief address
systemctl --failed
uname -r
pacman -Q
```

After installing the tools, record `ssh -V`, `tailscale version`, `tmux -V`, `node --version`, `npm --version`, `pi --version`, `opencode --version`, and `restic version`. Record the installed Omarchy release, backup destination, acceptance results, and recovery-key location. Keep actual keys outside this repository.
