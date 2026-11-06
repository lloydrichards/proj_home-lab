# Verify the host before relying on it

All checks start **not run**. Record dates, versions, results, and failures in ignored `local/acceptance.md`. Do not replace an unchecked box with a pass based only on documentation review.

## Hardware and boot

- [ ] Record delivered CPU, RAM modules, SSD health, firmware, and actual Omarchy release.
- [ ] Confirm mount security, airflow, and cable strain relief.
- [ ] Complete a memory test and a representative sustained build without errors.
- [ ] Test cold boot and the chosen disk-unlock route with the monitor attached.
- [ ] Verify the machine stays reachable after overnight idle and after disconnecting its display.
- [ ] Record actual idle power and fan behavior if these matter; no measurements are assumed here.

## Access controls

- [ ] Verify HP host-key fingerprints from the local console.
- [ ] Open a second fresh key-only SSH session as `coder` and as the admin account.
- [ ] Reject password-based SSH and root login.
- [ ] Confirm Tailscale SSH is disabled for the OpenSSH-based design.
- [ ] Confirm `coder` lacks sudo, `wheel`, Docker group, and host Docker socket access.
- [ ] Confirm `coder` cannot read the administration account's private files.
- [ ] Test access from the laptop over an external network.
- [ ] Test denial from an unauthorized tailnet device and a LAN device without Tailscale, including IPv6.
- [ ] Review tailnet grants for broad rules and record device-expiry recovery.
- [ ] Confirm no router port forwarding or Funnel exposes SSH, agents, or management tools.

## Remote workflow

- [ ] Start a harmless task in tmux, disconnect the laptop, and reattach to the still-running session.
- [ ] Run a real project build and tests as `coder` without administrator access.
- [ ] Keep concurrent tasks in separate workspaces and branches.
- [ ] If using OpenCode web, bind only loopback and reject unauthenticated API/browser requests.
- [ ] Open the interface through the SSH tunnel and verify LAN access to its backend port fails.
- [ ] Measure RAM and build time with one, then two heavy jobs before increasing concurrency.
- [ ] Reboot deliberately and distinguish resumed conversations from processes that must be restarted.

## Maintenance and recovery

- [ ] Complete an off-machine backup with no unexplained errors.
- [ ] Restore an uncommitted file and a saved agent session into a private test directory.
- [ ] Check a backup repository and record the last successful backup externally.
- [ ] Confirm the recovery passphrase or secret is available outside the HP.
- [ ] Complete an update with fresh SSH and workload checks afterward.
- [ ] Confirm local access to the boot menu and bootable USB.
- [ ] Document how to revoke a lost laptop and rotate Git and provider credentials.

Do not remove the local recovery path until access, cold-boot, and restore checks pass. A public service, a new container stack, or a persistent agent API adds its own acceptance tests.
