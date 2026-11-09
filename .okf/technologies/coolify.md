---
type: Concept
title: "Coolify"
description: "Pi deployment management, recovery dependencies and backup boundaries."
status: draft
sources:
  - id: source-1
    resource: "../../devices/remote-lab/coolify.md"
  - id: source-2
    resource: "../../devices/remote-lab/coolify-cloudflare.md"
  - id: source-3
    resource: "../../devices/_reference/services.md"
  - id: backup-operations
    resource: "../../devices/remote-lab/backups.md"
---

# Coolify

SSH inspection on 9 November 2026 initially confirmed Coolify 4.4.7, then 4.7.2 during backup setup, on the Pi 5 alongside a [Cloudflare tunnel](cloudflare-tunnel.md "accessed through"). Repairing the tunnel network restored six tested public routes. The service register owns current placement and access details.

On 9 November Lloyd authorized nightly backups from remote-lab to home-lab through a dedicated account. The installed workflow uses an external collector rather than Coolify's scheduled backups. It stops application writes, makes PostgreSQL dumps, archives cold volumes and bind mounts, then restarts containers before transfer. This trades a brief nightly outage for consistency across SQLite databases and application files; the first sequence took 83.6 seconds. [Restic](restic.md "retains encrypted history through") keeps independently controlled history on the HP. Three successful source generations allow catch-up after an outage; source and destination share the same premises.

An instance database dump alone excludes application data and the `APP_KEY` needed to decrypt saved credentials. Recovery must include volumes, configuration and the original key. First checks restored all four PostgreSQL clusters, restored the separate Coolify dump, and decrypted a restored credential using the archived key. Nine SQLite databases restored with accompanying WAL files passed integrity checks; the off-machine file restore and nightly SQLite main-file checks passed separately. Full dashboard and end-to-end application recovery remain untested. Images and writable container layers are not included; custom apps need their source for rebuilding. Native host tunnel configuration outside mounted storage remains outside this backup scope.

The historical installation guide configures localhost as the deployment server. The tunnel guide attaches cloudflared to the Coolify container network and routes traffic to its proxy. Live inspection confirmed this tunnel-to-proxy topology on 9 November 2026.

[Docker](docker.md "uses in the historical deployment recipe") permissions and port publication affect this design. A tunnel alone does not establish an authorization policy for the dashboard.

The HP plan [keeps Pi hosting separate](../decisions/keep-pi-hosting-separate.md "is retained by") until there is a reason to migrate and a tested restore plan.
