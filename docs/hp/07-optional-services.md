# Add services after remote development works

Add one service at a time, after the base acceptance checks pass. Record each service's identity, listening address, data directory, backup method, resource use, and removal steps.

| Service | When useful | Initial placement |
|---|---|---|
| Private app previews | Browser tests or a local application UI | HP loopback with SSH tunnel |
| Persistent OpenCode backend | A stable browser URL or local TUI attach is needed | Non-root user service, loopback, authentication |
| Development database | A project needs state | Disposable data first; private network and scoped credentials |
| Docker-dependent agent builds | A trusted build requires Docker | Prefer a dedicated VM; do not grant agents the host daemon |
| Coolify migration | Pi capacity or reliability becomes limiting | Keep on Pi until separate migration/restore plan passes |
| Backup timer | First manual restore drill passed | Separate reviewed service and protected destination |
| Monitoring | Missed backups or failures need notice | Start with failed-unit, disk, and backup freshness checks |
| Remote graphical desktop | A task genuinely requires the desktop | Separate research; authenticate and restrict to Tailscale |
| UPS | Power interruptions affect availability | Test shutdown, restart, and encrypted unlock behavior |
| Hardware console/KVM | Recovery without physical access is necessary | Separate security and network review |

Do not install Portainer, a reverse proxy, Kubernetes, a public tunnel, or a monitoring stack merely because this is a home lab. Every management service adds credentials, listening ports, updates, and recovery work.

Before adopting a VM or container isolation design, define what the agent may access. Decide how source files, Git credentials, model credentials, outbound network access, browser tests, and resource limits cross that boundary. A container with the host socket or privileged mode does not provide the intended host protection.
