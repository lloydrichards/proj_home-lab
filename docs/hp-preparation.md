# Prepare for the HP

The purchased EliteDesk 800 G6 Mini is arriving soon: i5-10500T, 32 GB RAM, 1 TB SSD. No installation or live checks have run.

## Before it arrives

- [ ] Have Ethernet, a monitor, a wired keyboard, and an installation USB ready.
- [ ] Confirm rack mounting, power-adapter support, airflow, and cable clearance.
- [ ] Choose a first off-machine backup destination. See [backup research](research/backups.md).

## When it arrives, work through this together

- [ ] Check the delivered hardware, firmware, memory, and SSD health; update the inventory.
- [ ] Recheck the current Omarchy installer and install using the chosen unencrypted boot route.
- [ ] Establish private laptop access and separate maintenance from coding permissions.
- [ ] Try one trusted project with Pi or OpenCode and a persistent terminal session.
- [ ] Check fresh login, disconnect/reconnect, idle access, reboot, and unintended network exposure.
- [ ] Back up and restore an uncommitted file and saved agent session before relying on the host.

Write and verify each setup recipe as we do it. Keep only instructions worth repeating or useful for recovery.

## Context when needed

The [HP workflow concept](../.okf/technologies/private-remote-development.md) connects the proposed tools. The [boot choice](../.okf/decisions/unattended-boot.md) records the confirmed unencrypted preference and its physical-access tradeoff. [Private development](../.okf/decisions/private-development.md) explains the proposed access boundary.

Research is available for [Omarchy](research/omarchy-headless.md), [private access](research/private-access.md), [Pi and terminal workflows](research/remote-coding.md), and [OpenCode](research/opencode-v2.md). These are dated findings, not a completed installation plan. Refresh version-sensitive details at the point of use.
