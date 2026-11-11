# Configure unattended boot

Use the local HP console as the maintenance account. This procedure targets the recorded Omarchy, Limine, systemd, and encrypted-root arrangement. Stop if your boot stack differs. Keep the disk passphrase, recovery USB, monitor, and keyboard available.

Read the [boot explanation](../explanations/unattended-boot.md) before choosing a TPM policy. Recheck the [version-sensitive TPM research](../research/tpm-unlock.md) against your installed release. The existing machine's working enrollment is not a command to enroll it again.

## Prevent system-managed sleep

Skip the TPM sections if you only need the host to stay awake. On home-lab as `lloyd`:

1. Inspect existing overrides before adding a policy. Reuse an existing lab sleep-policy drop-in if present; the recorded host uses the filename below. Save its current contents privately before editing.

```bash
	systemd-analyze cat-config systemd/sleep.conf
	sudo install -d -m 755 /etc/systemd/sleep.conf.d
	sudoedit /etc/systemd/sleep.conf.d/90-home-lab-no-sleep.conf
```

2. Set the drop-in to:

```ini
[Sleep]
AllowSuspend=no
AllowHibernation=no
AllowSuspendThenHibernate=no
AllowHybridSleep=no
```

3. Run `systemd-analyze cat-config systemd/sleep.conf` again. Confirm no later override re-enables these settings. Retain desktop screen locking; disabling it does not prevent power sleep.
4. Check fresh SSH access after leaving the host idle overnight. This policy does not cover shutdown or firmware AC-loss behavior. To roll back, restore the saved contents if the file already existed. Remove it only if you created it in this procedure.

## Preserve password recovery

1. Identify the encrypted device and active boot configuration:

```bash
	lsblk -o NAME,FSTYPE,UUID,MOUNTPOINTS
	findmnt --target /
	ls /dev/tpm*
	sudo cat /etc/mkinitcpio.conf.d/*.conf
	sudo cat /etc/default/limine
```

Inspect the kernel preset and effective hooks too. Do not assume a drop-in is active when a preset selects another configuration file.

2. Set `LUKS_DEVICE` in this shell to the encrypted partition identified above. Replace the placeholder before running subsequent commands:

```bash
	LUKS_DEVICE=/dev/YOUR_ENCRYPTED_PARTITION
	sudo cryptsetup luksDump "$LUKS_DEVICE"
	sudo cryptsetup open --test-passphrase "$LUKS_DEVICE"
```

Enter the retained disk passphrase. Stop if the device is wrong, no password slot exists, or the passphrase test fails. Do not copy the installed HP's device name or UUID to new hardware.

3. Save a private LUKS header backup outside the affected disk. Set `HEADER_BACKUP` to that destination, then run:

```bash
	sudo cryptsetup luksHeaderBackup "$LUKS_DEVICE" --header-backup-file "$HEADER_BACKUP"
```

Keep the header file private. Save copies of each boot file you will change alongside your recovery material. Preserve the password slot throughout this procedure.

## Configure the matching boot stack

1. If you choose the recorded PCR 7 policy, add the TPM enrollment:

```bash
	sudo systemd-cryptenroll "$LUKS_DEVICE" --tpm2-device=auto --tpm2-pcrs=7
```

Enter the disk passphrase locally. Do not wipe password slots or clear the TPM. Reinspect slots and confirm both the password and TPM enrollment exist.

2. Configure the systemd initramfs path with `systemd` and `sd-encrypt`, preserving the other hooks your installation needs. The installed HP uses `/etc/mkinitcpio.conf.d/zzzz-local-tpm.conf`.
3. Edit the active Limine root-unlock options in `/etc/default/limine`. Preserve the real root UUID, mapping, and existing required options. Add `tpm2-device=auto,token-timeout=10s` to the root-unlock options. Keep any corresponding `/etc/kernel/cmdline` configuration consistent.
4. Rebuild through the installed Omarchy/Limine integration:

```bash
	sudo limine-mkinitcpio
```

Stop if the rebuild fails. Check the generated boot entry, TPM support, and early root-unlock configuration before rebooting. If the generated image or entry differs from this recorded layout, resolve it with the matching [mkinitcpio and crypttab sources](../research/tpm-unlock.md#inspect-before-changing-boot-files).

5. On the recorded layout, compare the primary Limine entry's BLAKE2b digest with the actual image:

```bash
	b2sum /boot/EFI/Linux/omarchy_linux-omarchy.efi
	sudo cat /boot/limine.conf
```

Do not inspect the live image with an `objcopy` invocation that can rewrite it. Work from a scratch copy if section extraction is needed.

## Test startup and recover

1. Reboot with the console attached. Let the machine start without entering the disk password.
2. From the Mac, establish fresh SSH connections to both accounts. Check `systemctl --failed` and the current boot logs.
3. After that passes, test a cold start without a monitor and record the result. Keep overnight idle and AC-loss tests separate in [preparation](../preparation.md).

If automatic unlock fails, use the retained disk passphrase at the console. Restore your reviewed password-based boot configuration and rebuild through the matching boot integration. Inspect the saved recovery material before using it; the installed HP's private recovery path belongs in the [inventory](../../_reference/inventory.md), not in a new machine's commands.
