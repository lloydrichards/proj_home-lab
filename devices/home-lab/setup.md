# Build a private coding host

We will set up an Omarchy host that you can reach from a Mac, run an agent under a separate coding account, and recover a saved conversation from an encrypted cloud backup.

Use a new machine with no data you need to retain. Keep a monitor, keyboard, and installer USB attached until the remote-login and boot checks pass. Individual parts of this route were tested on the [recorded HP](../_reference/inventory.md); the complete fresh-hardware sequence has not been rehearsed end to end.

For an existing installation, use the [task guides](README.md#operate-and-recover) instead of repeating account creation or enrollment. For replacement hardware, recover credentials and agent data through the [recovery guide](how-to/restore-agent-conversation.md#recover-on-replacement-hardware).

## 1. Install the operating system

1. Prepare an installer using the [official Omarchy installation instructions](https://omarchy.org/).
2. Install Omarchy on the intended internal disk. Installation erases that disk.
3. Create the maintenance account as `lloyd` and retain the disk passphrase in your password manager.
4. Connect Ethernet and sign in at the console.
5. Open a terminal and inspect the system:

```bash
	hostnamectl
	findmnt --target /
	findmnt --target /home
	ip -br address
	timedatectl
```

You should see a mounted root filesystem, a Btrfs `/home`, a wired address, and a synchronized clock. Stop if the disk layout differs: the supplied agent backup requires Btrfs. The tested boot method also requires a TPM 2.0 device.

## 2. Name and update the host

On the new host as `lloyd`:

```bash
	sudo hostnamectl set-hostname home-lab
	sudo timedatectl set-timezone Europe/Zurich
	omarchy update
	hostnamectl --static
```

The final command should print `home-lab`. Check the tools before the access setup:

```bash
	pacman -Q openssh tailscale ufw git tmux restic btrfs-progs
```

For each missing package, run `omarchy pkg add PACKAGE` with that package's name. Do not use a partial Arch upgrade to install it. Use the stable Omarchy update channel. If the update requests intervention, finish it before continuing.

This tutorial uses `home-lab`, `lloyd`, and `coder` to match the supplied scripts. If you choose different names or a different timezone, review every [fixed installer input](reference/automation.md#installation-contract) before running them. Another reader must supply their own addresses, keys, domain, and cloud credentials.

## 3. Establish private access

1. Follow [Secure remote access](how-to/secure-remote-access.md) to create `coder`, authorize your Mac key, enroll Tailscale, and validate OpenSSH.
2. Keep the console and the first working session open.
3. From a new Mac terminal, connect to each account using this host's own Tailscale address:

```bash
	ssh lloyd@HOST_TAILSCALE_IP
	ssh coder@HOST_TAILSCALE_IP
```

You should reach `home-lab` under the requested account. A fresh `coder` session must have no general sudo or Docker-group access. The maintenance account should retain password-required administration.

In the `coder` session, clone this notebook so the later script paths exist:

```bash
	mkdir -p ~/projects
	git clone https://github.com/lloydrichards/proj_home-lab.git ~/projects/proj_home-lab
```

Use a trusted existing checkout if it is already present. If you fork the notebook, use your fork's URL. Review the scripts before an administrator installs their root-owned copies.

## 4. Keep the host available

On home-lab as `lloyd`, inspect the current sleep policy:

```bash
	systemd-analyze cat-config systemd/sleep.conf
```

Follow [Configure unattended boot](how-to/configure-unattended-boot.md) to prevent system sleep. If you want automatic disk unlock, complete its TPM path while retaining the working disk passphrase.

Shut down normally, disconnect the monitor, and power on. From the Mac, repeat the two fresh SSH logins. You should connect without entering a disk password at the console if TPM unlock is enabled. If either login fails, reconnect the console before changing networking.

## 5. Run an agent as coder

1. Follow [Install agent tools](how-to/install-agent-tools.md) for Codex, OpenCode, and the shared skills.
2. Sign in to your chosen provider through its supported login flow.
3. On the Mac, connect as `coder` and start the agent in a trusted checkout:

```bash
	ssh coder@HOST_TAILSCALE_IP
	mkdir -p ~/projects
	cd ~/projects
```

Clone a repository you control, change into it, and start `codex`. Send a small read-only question. You should see the agent's response and a saved conversation. Exit the agent after the response. Start and exit OpenCode once to initialize its local data too; the current backup preflight requires that directory. Rex and T3 are optional client paths in the same guide.

Project files remain on the host. Push work you want GitHub to preserve. The selected backup scope excludes project checkouts, unpushed commits, and uncommitted edits.

## 6. Deliver a private report

If you want browser previews or HTML reports, follow [Publish reports and previews](publishing.md). Open the returned private report URL from the Mac.

You should see the report and its assets through private HTTPS. A successful server-side request alone does not verify the Mac browser. Skip this step if you do not need browser delivery.

## 7. Back up and reopen the conversation

1. Follow [Back up agent sessions](how-to/back-up-agent-sessions.md) to prepare protected R2 credentials and install the backup job.
2. Wait for its local and cloud restore checks to pass before enabling routine use.
3. Follow [Restore an agent conversation](how-to/restore-agent-conversation.md) to reopen a saved Codex conversation in a disposable profile.
4. Confirm that the old user message and assistant reply appear, then close and remove only the test copy.

You should now have a verified cloud recovery path for agent data. Repeating a successful upload without opening the restored history does not complete this exercise.

## 8. Check the next scheduled run

After 04:00 Europe/Zurich on the following day, on home-lab as `lloyd`:

```bash
	systemctl show lab-agent-backup.service -p Result -p ExecMainStatus -p ExecMainExitTimestamp
	systemctl list-timers 'lab-agent-backup*' --all
```

Expect `Result=success`, `ExecMainStatus=0`, and a completion timestamp from the scheduled run. If the job failed, use [backup diagnosis](how-to/back-up-agent-sessions.md#run-pause-or-diagnose).

The host is ready for this workflow when fresh remote logins, unattended startup, a model response, a cloud restore, and a scheduled backup all pass. Our remaining checks belong in [preparation](preparation.md); your new machine needs its own results.
