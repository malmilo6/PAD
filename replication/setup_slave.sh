CONTAINER_NAME="mysql-container-wds-replica"
#CONTAINER_NAME="mysql-container-wds-replica2"
#CONTAINER_NAME="mysql-container-wds-replica3"

MYSQL_USER="root"
MYSQL_PASSWORD="rootpassword"

# SQL commands. In order to subscribe to new master, add RESET SLAVE ALL; after STOP SLAVE;
SQL_COMMANDS="
STOP SLAVE;

CHANGE MASTER TO
    MASTER_HOST='db_wds',
    MASTER_USER='replica_user1',
    MASTER_PASSWORD='replica_password1',
    MASTER_LOG_FILE='mysql-bin.000003',
    MASTER_LOG_POS=27484,
    GET_MASTER_PUBLIC_KEY=1;

START SLAVE;

SHOW SLAVE STATUS\G;

STOP SLAVE;
RESET SLAVE;
START SLAVE;
"

# Subscribe to new master
#SQL_COMMANDS="
#STOP SLAVE;
#
#CHANGE MASTER TO
#    MASTER_HOST='db_wds_replica',
#    MASTER_USER='replica_user2',
#    MASTER_PASSWORD='replica_password2',
#    MASTER_LOG_FILE='mysql-bin.000003',
#    MASTER_LOG_POS=29042,
#    GET_MASTER_PUBLIC_KEY=1;
#
#START SLAVE;
#
#SHOW SLAVE STATUS\G;
#
#STOP SLAVE;
#RESET SLAVE;
#START SLAVE;
#"

echo "Executing SQL commands inside the MySQL container (${CONTAINER_NAME})..."

# Execute the SQL commands inside the Docker container
docker exec -i "${CONTAINER_NAME}" mysql -u "${MYSQL_USER}" -p"${MYSQL_PASSWORD}" -e "${SQL_COMMANDS}"

if [ $? -eq 0 ]; then
  echo "Subscribed to MASTER"
else
  echo "Failed to execute commands."
  exit 1
fi