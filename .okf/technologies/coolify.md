---
type: Concept
title: "Coolify"
description: "Deployment authority, routing dependencies, and application recovery."
status: draft
sources:
  - id: routing
    resource: "../../devices/remote-lab/coolify-cloudflare.md"
  - id: current-evidence
    resource: "../../devices/_reference/services.md"
  - id: backup-contract
    resource: "../../devices/remote-lab/reference/backups.md"
  - id: restore-guide
    resource: "../../devices/remote-lab/how-to/restore-backups.md"
---

# Coolify

Coolify manages public workloads on remote-lab while HP development stays separate under the [hosting decision](../decisions/keep-pi-hosting-separate.md "is retained by"). Its root SSH deployment connection remains intentional. Removing privileges from the separate coolify host account did not reduce that deployment credential's authority.

The [Cloudflare tunnel](cloudflare-tunnel.md "receives traffic through") reaches a Docker proxy. Human dashboard authentication, GitHub event delivery, and application login require separate controls. A browser gate must not accidentally block machine webhooks, while a webhook bypass must not waive signature validation. Current route and callback verification limits belong in the service register.

Instance URLs and proxy redirects need to match the tunnel origin. The applied public HTTPS URL retains an HTTP proxy site for the HTTP origin. A URL-only change previously caused a self-redirect; the operating guide owns its repair. Generated proxy files are output, not the configuration authority.

Application destinations reduce direct network sharing, but they do not establish complete host isolation. Plastic Map moved through a configuration clone; the original remained stopped for recovery. Outlier moved in place through an inspected same-server metadata change outside the documented UI workflow. It retained its volume and pinned image. Its saved ingress label also needed correction: changing destination metadata did not reconcile every proxy setting. Neither route is a generic stateful data-migration recipe.

Recovery requires more than Coolify's database dump. Application storage and the original `APP_KEY` are needed to recover encrypted credentials and workloads. [Restic](restic.md "retains verified data through") stores local/cloud history; isolated data and credential drills passed. Full restored dashboard operation, complete app cutover, and replacement-host recovery remain untested.

The [backup reference](../../devices/remote-lab/reference/backups.md) owns scope and service contracts. The service register owns version, deployment, and test facts. Further network isolation and build-secret work remain explicitly deferred.
