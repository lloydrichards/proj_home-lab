# Prepare for the HP

The purchased HP is arriving soon. Hardware details are in the [inventory](../reference/inventory.md). No installation or live checks have run.

Chosen on 7 November 2026: use devvm locally on the MacBook for selected projects, and ordinary remote coding on the HP over Tailscale and SSH. HP project VMs are deferred. The daily client is still undecided.

This is the single list of upcoming HP work. After installing Omarchy, follow the [HP setup guide](setup.md) in order and mark progress here. Research supplies the evidence behind the guide.

## Before it arrives

- [ ] Have Ethernet, a monitor, a wired keyboard, and an installation USB ready.
- [ ] Confirm rack mounting, power-adapter support, airflow, and cable clearance.
- [ ] Choose a first off-machine backup destination. See [backup research](../research/backups.md).

## When it arrives, work through this together

- [ ] Check the delivered hardware, firmware, memory, and SSD health; update the inventory.
- [ ] Recheck the current Omarchy installer and install using the chosen unencrypted boot route.
- [ ] Set the planned hostname `home-lab` before Tailscale enrollment; confirm its actual private name and record it in the inventory. Leave Pi renaming for separate maintenance.
- [ ] Record the installed release, update through Omarchy, and check networking, clock synchronization, firmware, and SSD health. See [setup steps 1 and 2](setup.md#1-record-the-machine-and-check-basic-operation).
- [ ] Establish private laptop access and separate maintenance from coding permissions; check key-only login and rejection of unauthorized access.
- [ ] Review enabled listeners, remove unused sharing exceptions, set the host sleep policy, and check AC-loss recovery. See [setup step 7](setup.md#7-remove-unused-listeners-and-prevent-sleep).
- [ ] Try one trusted project with Pi or OpenCode and a persistent terminal session. Compare a Mac client from the [remote agent tools research](../research/remote-agent-tools.md) before choosing the daily interface. Use separate worktrees for concurrent tasks and measure resource use before adding more jobs.
- [ ] Check fresh login, disconnect/reconnect, idle access, reboot, and unintended network exposure, including browser authentication if used. Keep console and boot recovery available.
- [ ] Check a Git handoff between a Mac project and an HP checkout. Keep each active task on one machine and preserve uncommitted work separately from branch transfers.
- [ ] Back up and restore an uncommitted file and saved agent session before relying on the host.
- [ ] Configure scheduled backups for the chosen destination, agree retention, and test missing-destination failure reporting.

The guide is researched and has not run on the HP. As we work through it, correct commands for the installed release and record observations in the inventory and service register. Configure backup scheduling, retention, and failure notifications once the destination is chosen.

## Context when needed

The [HP workflow concept](../.okf/technologies/private-remote-development.md) connects the proposed tools. The [boot choice](../.okf/decisions/home-lab/unattended-boot.md) records the confirmed unencrypted preference and its physical-access tradeoff. [Private development](../.okf/decisions/home-lab/private-development.md) explains the proposed access boundary.

Research is available for [Omarchy](research/omarchy.md), [private access](../research/private-access.md), [Pi and terminal workflows](../research/remote-coding.md), and [OpenCode](../research/opencode-v2.md). These are dated findings supporting the setup guide, not evidence of an installation. Refresh version-sensitive details at the point of use.
