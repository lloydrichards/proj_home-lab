[[raspberry pi]], [[docker]]

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