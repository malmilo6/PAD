#!/bin/bash

CONTAINER_NAME="mysql-container-wds"

MYSQL_USER="root"
MYSQL_PASSWORD="rootpassword"

REPLICA_USER="replica_user1"
REPLICA_PASSWORD="replica_password1"

# SQL commands
SQL_COMMANDS="
CREATE USER IF NOT EXISTS '${REPLICA_USER}'@'%' IDENTIFIED BY '${REPLICA_PASSWORD}';
GRANT REPLICATION SLAVE ON *.* TO '${REPLICA_USER}'@'%';
FLUSH PRIVILEGES;
SHOW MASTER STATUS;
"

echo "Executing SQL commands inside the MySQL container (${CONTAINER_NAME})..."

# Execute the SQL commands inside the Docker container
docker exec -i "${CONTAINER_NAME}" mysql -u "${MYSQL_USER}" -p"${MYSQL_PASSWORD}" -e "${SQL_COMMANDS}"

if [ $? -eq 0 ]; then
  echo "Replication user created successfully, and master status fetched."
else
  echo "Failed to execute commands. Check container status and credentials."
  exit 1
fi