# Getting the Raspberry Pi Setup

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
