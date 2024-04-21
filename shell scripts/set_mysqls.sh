#4

docker run -d --name=source --hostname=source --net orchnet --ip "172.20.0.17" \
  -e MYSQL_ROOT_PASSWORD=mypass \
  -p 3009:3306 \
  mysql/mysql-server:8.0 \
  --server-id=1 \
  --enforce-gtid-consistency='ON' \
  --log-slave-updates='ON' \
  --gtid-mode='ON' \
  --log-bin='mysql-bin-1.log'