# Inventory and verification record

HP and both Pis inspected over SSH on 9 November 2026. See the [service register](services.md) and [BOM](bom.md).

## HP hardware

| Item | Observed or recorded value | Remaining uncertainty |
|---|---|---|
| HP | EliteDesk 800 G6 Desktop Mini PC; SKU `26L19US#ABA`; board `8711` | Physical mounting and power-adapter details |
| Firmware | S21 02.16.20, dated 8 September 2023 | Current update availability and AC-loss setting not checked |
| CPU | Intel i5-10500T, 6 cores / 12 threads, VT-x | Diagnostics and sustained-load test pending |
| RAM | 32 GB purchased, 31 GiB usable | Module layout, speed and memory test pending |
| SSD | SK hynix PC711 NVMe 1 TB, 953.9 GiB; firmware 41001131 | SMART passed 9 November; see health summary below |
| Storage | 2 GiB FAT boot partition; LUKS root with Btrfs; about 37 GiB used | Backup restore not tested |
| Network | `eno1`, 1 Gbit/s Ethernet; DHCP `192.168.8.223/24`, gateway `192.168.8.1` | DHCP reservation not confirmed; purchased offer excluded Wi-Fi |
| Rack | DeskPi RackMate T1 recorded | Shelf, fasteners, adapter support and airflow not confirmed |
| Mac client | macOS 27.2, OpenSSH 10.5p1; Tailscale access works | Exact Mac model and Tailscale version not collected |

## HP operating state

- Hostname and Tailscale name: `home-lab`. Addresses and connection commands live in the [service register](services.md).
- Omarchy 4.5.0; kernel `7.2.15-1-omarchy`; timezone Europe/Zurich; clock synchronized.
- `lloyd`, UID/GID 1000, home `/home/lloyd`, maintenance account in `wheel`. The username-specific sudo rule in `/etc/sudoers.d/07_home-lab` names `lloyd` and passed privileged policy validation. Root password set by user, never recorded here.
- `coder`, UID/GID 1001, home `/home/coder`, primary group only. User-provided sudo policy showed no positive command grant. Projects belong under `/home/coder/projects`.
- Key-only OpenSSH permits `lloyd` and `coder`; password, keyboard-interactive and root SSH login disabled. Fresh key logins passed. Tailscale SSH is disabled; ordinary OpenSSH handles authentication.
- OpenSSH 10.6p1-2, Tailscale 1.104.2-1, tmux 3.8-1 and Git 2.56.0 installed. `sshd` and `tailscaled` enabled. smartmontools 7.5-2 installed; `restic` remains absent.
- No failed system services. Snapshot temperatures: CPU package about 48 C, NVMe about 45 C; these are idle observations, not a load test.
- Automatic desktop login selects `lloyd`. Desktop locking and disk unlock are separate. TPM-backed disk unlock passed an untouched reboot; monitor-free cold power-on passed on 9 November 2026; idle access and AC-loss tests remain open.

## Disk unlock and recovery

Password slot 0 remains; TPM slot 1 binds to PCR 7. Secure Boot is off. This allows automatic unlock but does not authenticate boot software against physical tampering. The monitor-free cold-start check unlocked root in about 2.56 seconds.

Configuration uses `/etc/mkinitcpio.conf.d/zzzz-local-tpm.conf`, `/etc/default/limine`, and `/etc/kernel/cmdline`. Root-only backups and a rollback script are at `/root/tpm-unlock-backup.4I3jrh`; account-rename backup is under `/root/account-rename.*`. A LUKS header backup also exists at `/root/home-lab-luks-before-tpm.img`. These on-host copies are not off-machine backups.

Limine's image hash mismatch was repaired by rebuilding through `limine-mkinitcpio` and checking BLAKE2b without modifying the image. Old temporary `check-tpm-boot.sh`, `enable-tpm-unlock.sh` and `fix-tpm-boot.sh` scripts must not be reused: their `objcopy --dump-section` invocation could rewrite the input image. See the [setup recovery notes](../home-lab/setup.md#installed-configuration-and-recovery).

## Device names

All three names are applied. The Pi system names were changed at Lloyd's request on 9 November 2026. Both Pi Tailscale DNS names match their system names; fresh SSH through each new name passed.

| Device | Name | Purpose |
|---|---|---|
| HP | `home-lab` | Development and coding agents |
| Pi 5 | `remote-lab` | Existing Coolify hosting |
| Pi 4 | `admin-lab` | Pi-hole and network administration |

Pi services and IP addresses were retained during the rename. A Mac SSH alias is separate from the device's hostname.

## Headless audit results

Lloyd supplied the privileged audit output on 9 November 2026. `/etc/systemd/sleep.conf.d/90-home-lab-no-sleep.conf` sets suspend, hibernation, hybrid sleep and suspend-then-hibernate to `no`. Removing that drop-in restores the previous system policy. Actual overnight availability remains untested.

UFW is active with default incoming denial, outgoing allowance and routed traffic disabled. It allows SSH from `192.168.8.0/24` and TCP 22 on `tailscale0`; port 53317 TCP/UDP remains broadly allowed for IPv4/IPv6, with Docker DNS exceptions retained. No service was observed listening on 53317 at the earlier SSH audit; its owning app and need remain unverified. Router forwarding and Tailscale access policy have not been inspected.

Sudo syntax validation passed. `lloyd` has administrator permission plus Omarchy's scoped helper rules; `coder` has only the negated asdcontrol rule and no positive command grant. The effective-SSH output was not collected successfully; the installed SSH drop-in and connection tests are the evidence for the recorded SSH settings.

NVMe SMART returned exit status 0 and passed: critical warning 0, spare 100%, estimated wear used 2%, temperature 45 C, 6,715 power-on hours, 920 power cycles, 59 unsafe shutdowns, zero media errors and zero error-log entries. Unsafe shutdowns are a lifetime counter, not evidence of current failure. These observations do not replace backups or a sustained-load test. The primary Limine BLAKE2b hash matches the UKI.

RAM module layout remains unknown because `dmidecode` is not installed. Usable memory is already observed through Linux. Module identification is useful inventory follow-up, not a blocker for disconnecting a display.

Monitor-free cold startup passed on 9 November 2026: Lloyd reported normal shutdown, monitor disconnection and power-on with no local input. After two minutes, fresh assistant key connections over Tailscale authenticated as both `lloyd` and `coder`; hostname was `home-lab`, no system services failed, and disk unlock completed in about 2.56 seconds. Overnight idle and firmware AC-loss recovery remain untested.

## Pi operating state

LAN key logins passed on 9 November 2026 as `lloyd`. Pi 4 hostname is `admin-lab`; Pi 5 hostname is `remote-lab`. Both had zero failed system units, though Pi 4 cloudflared was activating. Pi names are now applied. Current services, SSH policy and Tailscale gaps live in the [service register](services.md#access-cleanup).

## Pi 4 hardware

Read over SSH on 9 November 2026. Capacities below distinguish the whole device from the mounted filesystem.

| Item | Observed value | Remaining uncertainty |
|---|---|---|
| Board | Raspberry Pi 4 Model B Rev 1.1, ARM64 | Enclosure, cooling and power supply not physically checked |
| CPU | 4 Cortex-A72 cores; configured maximum 1.5 GHz | Sustained performance and thermal throttling not tested |
| RAM | 3.7 GiB usable, consistent with 4 GB model; 199 MiB swap | No memory stress test |
| Storage | 59.5 GiB microSD, device name `SN64G`; 512 MiB FAT boot partition; 59 GiB ext4 root partition | Card health and exact retail model unknown |
| Root filesystem | 58 GiB usable, 17 GiB used, 31% used | Usage is a dated snapshot; backup and restore untested |
| OS | Debian 12 Bookworm, kernel `6.12.109+rpt-rpi-v8` | General package upgrades not performed in this pass |
| Network | Ethernet `eth0` at 1 Gbit/s; `192.168.8.138/24`; Wi-Fi `wlan0` also active at `192.168.1.100/24` | Reservations, route preference and dependencies of both networks not checked |

## Pi 5 hardware

Read over SSH on 9 November 2026.

| Item | Observed value | Remaining uncertainty |
|---|---|---|
| Board | Raspberry Pi 5 Model B Rev 1.0, ARM64 | Enclosure, cooling and power supply not physically checked |
| CPU | 4 Cortex-A76 cores; configured maximum 2.4 GHz | Sustained performance and thermal throttling not tested |
| RAM | 7.9 GiB usable, consistent with 8 GB model; 199 MiB swap | No memory stress test |
| SSD | KIOXIA EXCERIA G2 NVMe, 931.5 GiB, consistent with 1 TB capacity | Firmware and SMART health not collected; `smartctl` and `nvme` tools absent |
| Partitions | 512 MiB FAT boot; 931 GiB ext4 root | Backup and restore untested |
| Root filesystem | 917 GiB usable, 34 GiB used, 4% used | Usage is a dated snapshot |
| OS | Debian 12 Bookworm, kernel `6.12.109+rpt-rpi-2712` | General package upgrades not performed in this pass |
| Network | Ethernet `eth0` at 1 Gbit/s; `192.168.8.142/24`; Wi-Fi `wlan0` also active at `192.168.1.143/24` | Reservations, route preference and dependencies of both networks not checked |

Earlier notes name a [Seeed 1 TB SSD](https://www.seeedstudio.com/NVMe-M-2-2280-SSD-1TB-p-5767.html) and an [Argon ONE V3 M.2 NVMe case](https://argon40.com/products/argon-one-v3-m-2-nvme-case). The live SSD identifies as KIOXIA EXCERIA G2. Neither the old purchase identity nor the enclosure can be confirmed from these SSH checks.
