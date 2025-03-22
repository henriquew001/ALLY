#!/bin/bash

set -e

# Function to check database connection
check_db_connection() {
  python -c "
import django
import os
from django.db import connection
from django.db.utils import OperationalError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cofi.settings')
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
  sleep 5
done

if [ $retry_count -ge $max_retries ]; then
  echo "Max retries reached. Database connection failed."
  exit 1
fi

echo "Database connection successful"

# Apply migrations
echo "Applying migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Migrations applied successfully."

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Static files collected."

# Check if superuser exists before creating one
SUPERUSER_EXISTS=$(python -c "
import django
import os
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cofi.settings')
django.setup()

User = get_user_model()
if User.objects.filter(email='admin@example.com').exists():
    print('EXISTS')
")

if [ "$SUPERUSER_EXISTS" != "EXISTS" ]; then
    echo "Superuser 'admin' does not exist. Creating it..."
    python manage.py createsuperuser --noinput
    if [ $? -ne 0 ]; then
        echo "Failed to create superuser."
        exit 1
    fi
else
    echo "Superuser 'admin' already exists."
fi

echo "Superuser check completed."

# Start Django server
echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000 --verbosity 3 --traceback
echo "Nach dem Start des Django Servers..."