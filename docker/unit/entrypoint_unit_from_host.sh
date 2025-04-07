#!/bin/bash

# export .env
export $(grep -v '^#' .env | xargs)

# jump to the venv folder
cd ../../frontend

source venv_unit/bin/activate
pip install -r ../docker/unit/requirements_django.txt
pip install -r ../docker/unit/requirements_djangotest.txt
cd ally
# Function to check database connection
check_db_connection() {
  python -c "
import django
import os
from django.db import connection
from django.db.utils import OperationalError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ally.settings')
django.setup()

try:
    connection.ensure_connection()
    print('Database connection successful')
except OperationalError as e:
    print(f'Database connection failed: {e}')
    exit(1)
except Exception as e:
    print(f'An unexpected error occurred: {e}')
    exit(1)
"
}

# Retry connection until successful or max retries reached
max_retries=5
retry_count=0
until check_db_connection || [ $retry_count -ge $max_retries ]; do
  echo "Retrying database connection... ($((retry_count+1))/$max_retries)"
  retry_count=$((retry_count+1))
  sleep 5  # Wait for 5 seconds before retrying
done

if [ $retry_count -ge $max_retries ]; then
  echo "Max retries reached. Database connection failed."
  exit 1
fi

# Check if migrations have been run
if ! python manage.py migrate --plan | grep -q "^[ ]+applying"; then
    echo "Migrations have already been applied."
else
    echo "Applying migrations..."
    python manage.py migrate
fi

# Check if superuser exists before creating one
SUPERUSER_EXISTS=$(python -c "
import django
import os
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ally.settings')
django.setup()

User = get_user_model()
if User.objects.filter(username='admin').exists():
    print('EXISTS')
")

if [ "$SUPERUSER_EXISTS" != "EXISTS" ]; then
    echo "Superuser 'admin' does not exist. Creating it..."
    python manage.py createsuperuser --noinput || echo "Failed to create superuser."
else
    echo "Superuser 'admin' already exists."
fi

# Start the Django server.
echo "Starting Django server..."
cd ..
echo "Starte Endlosschleife für pytest Unit-Tests..."
echo "Drücke Strg+C (Ctrl+C) zum Beenden."
echo "----------------------------------------------"

while true; do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Führe pytest aus..."

    # Dein pytest-Befehl
    pytest -m unit -n 3 ally/home ally/ally ally/products ally/authentication ally/focoquiz ally/recipes --html=tests/unittestreport.html --self-contained-html

    # Prüfung des Exit-Codes von pytest (optional, falls du den Status sehen willst)
    if [ $? -eq 0 ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Pytest erfolgreich abgeschlossen."
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Pytest mit Fehlern abgeschlossen (Exit-Code: $?)."
        # Wenn du willst, dass das Skript bei Fehlern stoppt, füge hier 'break' ein:
        # break
    fi

    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Warte 10 Sekunden..."
    sleep 10
    echo "----------------------------------------------"
done

# Dieser Teil wird normalerweise nicht erreicht, da die Schleife endlos ist,
# es sei denn, 'break' wird oben verwendet oder das Skript wird extern beendet.
echo "Skript beendet."
