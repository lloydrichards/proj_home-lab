# Add Postgres Server on Docker

1. Create a new directory for the Postgres server:

   ```bash
   sudo mkdir -p /opt/stacks/postgresql
   ```

1. Create Docker compose file:

   ```bash
   cd /opt/stacks/postgresql
   sudo nano docker-compose.yml
   ```

1. Add the docker service for db, replace `<USERNAME>` and `<PASSWORD>` with
   your desired values:

   - `<USERNAME>`: This is the username you want to use to access your super
     admin and its database.
   - `<PASSWORD>`: This is the password you want to use to access your super
     admin and its database.

   ```yaml
   services:
     db:
       image: postgres:latest
       restart: always
       environment:
         - POSTGRES_USER=<USERNAME>
         - POSTGRES_PASSWORD=<PASSWORD>
       ports:
         - 5432:5432
       volumes:
         - ./data:/var/lib/postgresql/data
   ```

1. Add the docker service for the adminer, replace `<USERNAME>` and `<PASSWORD>`
   with your desired values:

   - `<PGADMIN_EMAIL>`: This is the email you want to use to access your super
     admin and its database.
   - `<PGADMIN_PASSWORD>`: This is the password you want to use to access your
     super admin and its database.

   ```yaml
   services:
    ...
     pgadmin:
       image: dpage/pgadmin4:latest
       environment:
         PGADMIN_DEFAULT_EMAIL: <PGADMIN_EMAIL>
         PGADMIN_DEFAULT_PASSWORD: <PGADMIN_PASSWORD>
         ports:
           - 8080:80
   ```

1. Close and save the file. Press `Ctrl + X`, then press `Y`, and then press
   `Enter`.
1. Start the Postgres server:

   ```bash
   sudo docker-compose up -d
   ```

1. Access the adminer by visiting `http://localhost:8080` in your browser.
1. Add a new server:

   - Host name/address: `db`
   - Port: `5432`
   - Username: `<USERNAME>`
   - Password: `<PASSWORD>`
