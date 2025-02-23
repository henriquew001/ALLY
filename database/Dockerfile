FROM mariadb:latest

COPY database/mariadb.cnf /etc/mysql/mariadb.conf.d/
COPY database/init/ /docker-entrypoint-initdb.d/
