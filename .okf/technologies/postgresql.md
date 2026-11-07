---
type: Concept
title: "PostgreSQL"
description: "A database documented in the earlier Pi Compose setup."
status: draft
sources:
  - id: source-1
    resource: "../../remote-lab/postgres.md"
  - id: source-2
    resource: "../../research/backups.md"
  - id: source-3
    resource: "../../research/remote-coding.md"
---

# PostgreSQL

The historical guide describes a PostgreSQL container with persistent host storage, a published database port, and a pgAdmin web interface. It does not prove that this stack is currently deployed. Its YAML and commands have not been revalidated by this library expansion.

The guide mixes the terms Adminer and pgAdmin while its image is pgAdmin. Treat that naming mismatch as a documentation gap before reusing the procedure. It also uses floating image tags; choose versions deliberately before a new deployment.

For future HP use, the access research recommends an unpublished database on a private [Docker](docker.md "can run under") network when only containers need it. Database recovery needs an application-consistent dump or a documented quiesce procedure rather than an unqualified copy of live files.

A real migration belongs under the [recovery-first decision](../decisions/recovery-before-reliance.md "requires"), with a restore check before cutover.
