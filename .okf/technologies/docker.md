---
type: Concept
title: "Docker"
description: "Container data, network exposure, and host-control boundaries."
status: draft
sources:
  - id: current-authority
    resource: "../../devices/_reference/services.md"
  - id: security
    resource: "../../docs/explanations/security-and-access.md"
  - id: backup-contract
    resource: "../../devices/remote-lab/reference/backups.md"
  - id: historical-recipe
    resource: "../../devices/remote-lab/docker.md"
---

# Docker

A container boundary depends on its permissions, mounts, and networks. Docker-group membership and daemon-socket access grant extensive host authority. Privileged mode or a host socket can defeat the intended [agent isolation](agent-isolation.md "can undermine"). A read-only socket mount does not limit Docker API methods.

The HP coding account has no general host Docker access. Human Pi maintenance uses password-required sudo rather than Docker-group membership. Existing sessions can retain prior groups. Coolify retains its root deployment connection and Caddy/Sentinel retain socket access; removing the separate coolify account's privileges did not remove those management paths. Portainer is stopped with its data retained. Current facts belong in the service register.

Published container ports can bypass ordinary UFW input filtering. Unpublished ports and explicit loopback binding reduce exposure, but actual reachability needs [verification](../learnings/test-effective-exposure.md "requires"). A separate Docker network does not prove isolation from host services or a shared proxy.

Data volumes, container images, and writable container layers have different recovery requirements. The Pi backup preserves cold data and database dumps, not complete images or writable layers. Keep source access and compatible images available alongside [restic](restic.md "recovers data through").

Outlier's move exposed tag drift: a floating local PostgreSQL tag named a different image from the running container. Pinning its observed digest and retaining the explicit volume separated a network move from an image upgrade. Recreation and data checks passed; the service register owns their evidence. Historical direct-port and group-membership recipes are not the HP baseline.
