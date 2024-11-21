#CONTAINER_NAME="mysql-container-wds-replica"
CONTAINER_NAME="mysql-container-wds-replica2"
#CONTAINER_NAME="mysql-container-wds-replica3"

MYSQL_USER="root"
MYSQL_PASSWORD="rootpassword"

# SQL commands
SQL_COMMANDS="
STOP SLAVE;

CHANGE MASTER TO
    MASTER_HOST='db_wds',
    MASTER_USER='replica_user',
    MASTER_PASSWORD='replica_password',
    MASTER_LOG_FILE='mysql-bin.000007',
    MASTER_LOG_POS=123297,
    GET_MASTER_PUBLIC_KEY=1;

START SLAVE;

SHOW SLAVE STATUS\G;

STOP SLAVE;
RESET SLAVE;
START SLAVE;
"

echo "Executing SQL commands inside the MySQL container (${CONTAINER_NAME})..."

# Execute the SQL commands inside the Docker container
docker exec -i "${CONTAINER_NAME}" mysql -u "${MYSQL_USER}" -p"${MYSQL_PASSWORD}" -e "${SQL_COMMANDS}"

if [ $? -eq 0 ]; then
  echo "Subscribed to MASTER"
else
  echo "Failed to execute commands."
  exit 1
fi