//1

for N in 1 2 3 4 5
do docker run -d --name=mysqlorchdb$N --net orchnet \
  -e MYSQL_ROOT_PASSWORD=mypass \
  mysql/mysql-server:8.0 \
  --server-id=100 \
  --enforce-gtid-consistency='ON' \
  --log-slave-updates='ON' \
  --gtid-mode='ON' \
  --log-bin='mysql-bin-1.log'
done