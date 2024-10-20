# Home Lab

Documentation and configurations on how my home lab server is setup.

## Hardware

- [Raspberry Pi 4 Model B 8GB](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/)
- [64GB SanDisk Ultra microSDXC UHS-I Card](https://www.sandisk.com/home/memory-cards/microsd-cards/ultra-microsd-400gb)

## Software

- [Raspberry Pi OS (64bit)](https://www.raspberrypi.org/software/operating-systems/)
- [Docker](https://www.docker.com/)
- [Portainer](https://www.portainer.io/)

## Architecture

```mermaid
graph LR

A[Client]
M[GitHub Repo] --pull--> J
M <--push/pull--> F
subgraph Cloudflare
    B[SSH Tunnel]
    H[App Tunnel]
    N[DNS]
end

subgraph localNetwork
    subgraph homelab
        subgraph Docker
            C[Portainer] --> K(Apps)
            C --> L[(Database)]
            L <-.-> K
            J(Apps) --hosted--> D
            D[Coolify] --proxy--> I[Caddy]
            I --:80--> E([Cloudflared])
        end

        G([Cloudflared])
    end

    F[[MacBook]] --:9000--> C
    F --:3000--> K
    F --:5432--> L
end

G --ssh--> B --ssh--> A
E --http--> H --https--> A






```
