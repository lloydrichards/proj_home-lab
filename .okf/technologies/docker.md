---
type: Concept
title: "Docker"
description: "Container hosting in historical Pi guides and a restricted option for the HP."
status: draft
sources:
  - id: source-1
    resource: "../../remote-lab/docker.md"
  - id: source-2
    resource: "../../remote-lab/postgres.md"
  - id: source-3
    resource: "../../research/private-access.md"
  - id: source-4
    resource: "../../research/remote-coding.md"
---

# Docker

The historical Pi guide installs Docker and Portainer; another guide runs [PostgreSQL](postgresql.md "hosts in the historical Compose recipe") in Compose. These recipes establish prior documentation, not which containers are running now. The user reports [Coolify](coolify.md "supports deployment managed by") on the existing Pi, but live inspection is deferred.

The proposed HP baseline gives the coding account neither Docker group membership nor access to the host socket. The Docker group and daemon socket grant extensive host control. A container with privileged mode or the host socket does not provide the intended [agent isolation](agent-isolation.md "can undermine").

The access research warns that published ports can bypass ordinary UFW input filtering. Prefer unpublished database ports or explicit loopback publication when needed, and test actual reachability. See [exposure verification](../learnings/test-effective-exposure.md "requires").

The historical direct port publishing and group membership are not recommendations for the HP.
