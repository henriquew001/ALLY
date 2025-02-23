+---------------------+      +----------------------+
|       Backend       | ---> |         DB (MariaDB) |
|   (Python/API)      |      |                      |
|  (Port 8000:8000)   |      |  (Port 3306:3306)   |
|  DATABASE_URL:      |      |  Volumes: mariadb_data|
|  mysql+pymysql://   |      |                      |
|  root:je@db/        |      +----------------------+
|  conscious_fit      |
+---------------------+
^
| depends_on
|
+---------------------+
