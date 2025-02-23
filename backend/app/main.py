import pymysql
import os

def main():
    try:
        connection = pymysql.connect(
            host=os.environ.get("DB_HOST"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            database=os.environ.get("DB_NAME"),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        with connection.cursor() as cursor:
            # Beispielabfrage
            cursor.execute("SELECT VERSION()")
            result = cursor.fetchone()
            print("MariaDB Version:", result['VERSION()'])

            # Weitere Abfragen hier möglich
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print("Verbindung erfolgreich: ", result)

    except pymysql.MySQLError as e:
        print(f"Fehler bei der Verbindung zur MariaDB: {e}")

    finally:
        if "connection" in locals() and connection.open:
            connection.close()

if __name__ == "__main__":
    main()
