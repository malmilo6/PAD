#CONTAINER_NAME="mysql-container-wds-replica"
#
#MYSQL_USER="root"
#MYSQL_PASSWORD="rootpassword"
#
#REPLICA_USER="replica_user2"
#REPLICA_PASSWORD="replica_password2"
#
## SQL commands
#SQL_COMMANDS="
#STOP SLAVE;
#RESET SLAVE ALL;
#
#CREATE USER IF NOT EXISTS '${REPLICA_USER}'@'%' IDENTIFIED BY '${REPLICA_PASSWORD}';
#GRANT REPLICATION SLAVE ON *.* TO '${REPLICA_USER}'@'%';
#FLUSH PRIVILEGES;
#SHOW MASTER STATUS;
#"
#
#echo "Executing SQL commands inside the MySQL container (${CONTAINER_NAME})..."
#
## Execute the SQL commands inside the Docker container
#docker exec -i "${CONTAINER_NAME}" mysql -u "${MYSQL_USER}" -p"${MYSQL_PASSWORD}" -e "${SQL_COMMANDS}"
#
#if [ $? -eq 0 ]; then
#  echo "Replication user created successfully, and master status fetched."
#else
#  echo "Failed to execute commands. Check container status and credentials."
#  exit 1
#fi

# FUCK IT. DO IT MANUALLY !