# Home Lab

Documentation and configurations on how my home lab server is setup.

## Hardware

- [Raspberry Pi 4 Model B 8GB](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/)
- [64GB SanDisk Ultra microSDXC UHS-I Card](https://www.sandisk.com/home/memory-cards/microsd-cards/ultra-microsd-400gb)

## Software

- [Raspberry Pi OS (64bit)](https://www.raspberrypi.org/software/operating-systems/)
- [Docker](https://www.docker.com/)
- [Portainer](https://www.portainer.io/)

## Getting the Raspberry Pi Setup

1. Install Raspberry Pi OS (64bit) on the microSD card, using the
   [Raspberry Pi Imager](https://www.raspberrypi.com/documentation/computers/getting-started.html#raspberry-pi-imager).
1. Configure the OS with SSH and WiFi.
1. Add a new user
1. Insert the microSD card into the Raspberry Pi and power it on.
1. Find the IP address of the Raspberry Pi.

   ```bash
   ping raspberry.local
   ```

1. SSH into the Raspberry Pi.

   ```bash
   ssh <username>@<rpi hostname>
   ```

1. Update the Raspberry Pi.

   ```bash
    sudo apt update
    sudo apt upgrade
   ```

## Hardening the SSH

1. Create ssh-users group:

   ```bash
   sudo groupadd ssh-users
   sudo usermod -a -G ssh-users $USER
   ```

1. (From Local machine) Create and copy over the SSH key to the Raspberry Pi.

   ```bash
   ssh-keygen -t ed25519 -a 777
   ssh-copy-id -i <pub key> <username>@<rpi hostname>
   ```

1. SSH into raspberry pi and edit `/etc/ssh/sshd_config` with the following
   configuration changes:

   ```text
   PermitRootLogin no PubkeyAuthentication yes
   PasswordAuthentication no
   UsePAM no
   X11Forwarding no
   AllowGroups ssh-users
   ```

1. Restart ssh to apply the configuration:

   ```bash
   sudo systemctl restart ssh
   ```

## Installing Docker

1. Install Docker:

   ```bash
   curl -fsSL https://get.docker.com | sh
   ```

1. Add the user to the docker group:

   ```bash
    sudo usermod -aG docker $USER
   ```

1. Log out and log back in to apply the changes.
1. Install Portainer:

   ```bash
   sudo docker pull portainer/portainer-ce:latest
   sudo docker run -d -p 9000:9000 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest
   ```

1. Access Portainer at `http://<rpi hostname>:9000`.
1. Create a new user and password.
