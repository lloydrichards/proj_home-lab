# Install Omarchy and prepare headless operation

Status: proposed procedure. Run these steps on the HP, not on the laptop. Keep a monitor and wired keyboard attached until the acceptance checks pass. Sources and release-sensitive details are in [Omarchy research](../research/omarchy-headless.md).

## Prepare the machine

1. Record the HP product number, firmware version, RAM, and SSD model in a private inventory.
2. Check the SSD's health and run a memory test before storing important work. Review firmware updates through HP's official support for the actual product number.
3. Connect Ethernet. Reserve a LAN address in the router if useful for local recovery; Tailscale provides a separate address.
4. Check the rack mounting and keep the front intake and rear exhaust clear. Support the power adapter separately.
5. Keep another device and a bootable USB available for recovery.

## Use the chosen cold-boot behavior

The user selected **an unencrypted installation for unattended restart** on 6 November 2026. Confirm the target SSD before formatting. The alternatives remain here to explain the tradeoff:

| Route | Cold boot | Consequence |
|---|---|---|
| Default encrypted disk | Unlock locally | Protects a removed or stolen powered-off SSD |
| Explicit unencrypted install | Can start unattended | A person holding the SSD can read its contents |
| Separate remote-unlock design | Depends on tested pre-boot system | Extra credentials, network dependencies, and recovery work |

Use the second route for this installation. A removed SSD will expose source code, agent state, and locally stored credentials. Keep physical access restricted and backups encrypted. If the decision changes later, redesign and test the boot process rather than assuming ordinary SSH can unlock a pre-boot encrypted disk.

## Install from the official ISO

1. Read the [current installation instructions](https://omarchy.org/manual/getting-started/) and download the official ISO.
2. Verify the release signature using the [published security instructions](https://omarchy.org/manual/security/). Do not treat a checksum fetched from an unrelated site as authenticity proof.
3. Record the existing firmware settings. Follow the current installer requirements for Secure Boot. Do not routinely clear TPM keys.
4. Boot the USB and select the actual target SSD. A full-disk installation destroys its existing contents. Back up anything needed first.
5. Create the maintenance account `labadmin`, or record your chosen replacement name. Use a strong unique password.
6. Select the documented **no-encryption** option. The researched manual uses Ctrl-c at disk-format confirmation to opt out; read the screen and current instructions for the exact ISO. Verify the completed installation matches that choice.
7. Finish the installation and sign in locally. Record the resulting version and partition layout.

## Install the small set of missing tools

Use Omarchy's documented package interface, as the maintenance user. Review each installation before accepting it:

```bash
omarchy pkg add openssh
omarchy pkg add tailscale
omarchy pkg add tmux
omarchy pkg add restic
omarchy pkg add smartmontools
```

Skip tools already installed. Do not run old Raspberry Pi `apt` or Docker convenience-script instructions on this Arch-based host. Use `omarchy update` for system updates, rather than bypassing its migrations through a separate system-upgrade command. See [packages](https://omarchy.org/manual/other-packages/) and [updates](https://omarchy.org/manual/updates/).

## Prevent sleep and retain local locking

Install the reviewed [sleep policy example](../../config/systemd/90-home-lab-sleep.conf.example) as `/etc/systemd/sleep.conf.d/90-home-lab.conf`. Create the directory if missing. Inspect any other drop-ins for overriding values. The policy disables systemd-managed suspend and hibernation, not power-off or firmware behavior.

Keep screen locking enabled. Omarchy's menu toggle for Suspend does not disable all system sleep paths. Test overnight idle access after installing the policy. To undo it, remove only this drop-in and recheck the effective configuration.

Inspect login and graphical startup before changing them:

```bash
systemctl get-default
systemctl cat getty@tty1.service
systemctl cat display-manager.service
loginctl list-sessions
```

A missing display-manager service is possible. Establish remote access first. Do not assume one display manager or remove Omarchy's desktop packages. If you later disable graphical autologin, document the actual unit and shell changes with their rollback.

## Test a controlled restart

Complete [private access](02-private-access.md) first. With the console still attached, reboot and verify the chosen unlock process, Ethernet, Tailscale, and a fresh SSH login. Check whether firmware supports automatic restoration after AC loss, but enable it only if that behavior matches the chosen unlock plan.
