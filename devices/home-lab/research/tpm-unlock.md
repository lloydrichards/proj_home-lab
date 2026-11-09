# HP automatic disk unlock with TPM

Investigated 9 November 2026 for the installed Omarchy 4.5.0 system. Primary-source rationale for the installed method. Current observations live in the [inventory](../../_reference/inventory.md); remaining work lives in [preparation](../preparation.md).

## Starting evidence

The assistant's SSH inspection found a TPM 2.0 device at `/dev/tpmrm0`, systemd 262, a Limine boot loader, and a systemd-stub unified kernel image. Secure Boot is disabled. The root partition is LUKS-encrypted `/dev/nvme0n1p2`. A controlled reboot remained unreachable until Lloyd entered the disk password; SSH and Ethernet then started normally. TPM unlock was subsequently configured and passed a monitor-free cold startup. The following sections explain the method and its limits.

## Method and policy

Use the installed systemd tools rather than adding Clevis. `systemd-cryptenroll` adds a TPM enrollment alongside existing password slots. Keep the working disk passphrase. Do not use `--wipe-slot=password`, `--wipe-slot=all`, or clear the TPM. Enrollment requires entering the existing disk passphrase locally; it must not be sent through chat or stored in a script. The current manual defaults to no PCR binding, so specify the chosen policy explicitly. PCRs are TPM measurements used to limit when a sealed key is released. [systemd-cryptenroll manual](https://man.archlinux.org/man/systemd-cryptenroll.1)

A PCR 7-only policy is an availability-oriented compromise while Secure Boot remains off. PCR 7 records the Secure Boot policy, not the identity of the kernel or initramfs. Binding to the disabled state does not establish that trusted boot software ran. It can keep an SSD removed from this TPM encrypted, but must not be presented as protection against boot tampering on a stolen whole HP. This is an inference from the documented PCR meanings. [systemd PCR definitions](https://man.archlinux.org/man/systemd-cryptenroll.1)

For stronger boot integrity, configure and test Secure Boot and a maintained signed UKI/PCR policy as a separate change. A raw PCR 11 value captured after startup is unsuitable as a quick substitute because its value changes across boot phases and kernel/initramfs updates. Signed PCR policies support multiple approved images but require update integration. [systemd policy options](https://man.archlinux.org/man/systemd-cryptenroll.1)

## Inspect before changing boot files

Read `/etc/mkinitcpio.conf.d/*.conf`, the active kernel preset, and the installed `sd-encrypt` hook. Reading `/etc/mkinitcpio.conf` alone does not establish effective hooks. A preset supplying a separate configuration file can bypass normal drop-ins. Rebuild through the installed Omarchy/Limine path, and inspect the actual UKI before rebooting. [mkinitcpio manual](https://man.archlinux.org/man/mkinitcpio.8.en)

The systemd initramfs method needs `systemd` and `sd-encrypt`. Configure root unlock in the early boot environment using `tpm2-device=auto`, preserving existing UUID, mapping name, discard, and workqueue options. A regular late-boot `/etc/crypttab` entry alone is insufficient for an encrypted root. `/etc/crypttab.initramfs` or an appropriate `x-initrd.attach` entry can supply early configuration. Existing `rd.luks.*` command-line options must be checked for precedence. [Arch disk configuration](https://wiki.archlinux.org/title/dm-crypt/System_configuration), [crypttab manual](https://man.archlinux.org/man/crypttab.5)

## Version-sensitive check and recovery

Arch's mkinitcpio 42 added the PCR OS separator service and changed measurements of PCRs 0–7, 9, and 12–14. An existing enrollment may therefore need re-enrollment. Inspect the installed hook and current boot before choosing PCR values; do not copy values from an older recipe. [Arch release notice](https://archlinux.org/news/mkinitcpio-42-requires-manual-intervention-for-tpm2-based-unlocking-of-luks-devices/)

Keep a root-only LUKS header backup outside Git and copies of changed configuration before enrollment. Keep the monitor, keyboard, installer, and tested disk passphrase available. After configuration, verify that the TPM token was added without removing the password slot, verify the generated boot image contains the TPM libraries and early crypttab configuration, and test boot without touching the console. If automatic unlock fails, use the retained disk passphrase, inspect the boot logs, and correct or remove only the newly created TPM enrollment and configuration. A failed TPM policy should lead to passphrase recovery, not a reinstall.
