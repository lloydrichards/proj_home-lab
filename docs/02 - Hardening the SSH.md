[[raspberry pi]], [[security]]

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
