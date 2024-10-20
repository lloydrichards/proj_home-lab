# Home Lab

Documentation and configurations on how my home lab server is setup.

## Hardware

- [Raspberry Pi 5 Model B 8GB](https://www.raspberrypi.com/products/raspberry-pi-5/)
- [1 TB NVMe M.2 2280 SSD](https://www.seeedstudio.com/NVMe-M-2-2280-SSD-1TB-p-5767.html)
- [Argon ONE V3 M.2 NVME Raspberry Pi 5 Case](https://argon40.com/products/argon-one-v3-m-2-nvme-case)

## Software

- [Raspberry Pi OS (64bit)](https://www.raspberrypi.org/software/operating-systems/)
- [Docker](https://www.docker.com/)
- [Portainer](https://www.portainer.io/)
- [Cloudflare](https://www.cloudflare.com/)
- [Coolify](https://coolify.io/)

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
