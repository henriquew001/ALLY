#!/bin/bash

# Function to check database connection
check_db_connection() {
  python -c "
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cofi.settings')  # Replace 'cofi.settings' with your project's settings
django.setup()
from django.db import connection
from django.db.utils import OperationalError

try:
    connection.ensure_connection()
    print('Database connection successful')
    exit(0)  # Connection successful
except OperationalError as e:
    print(f'Database connection failed: {e}')
    exit(1)  # Connection failed
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

# Check if migrations have been run (by looking for a specific table).
# Customize this table if necessary.
if ! python manage.py showmigrations | grep -q "[X]"; then
    echo "Migrations have not been run. Running them now..."
    python manage.py migrate
else
    echo "Migrations have already been run."
fi

# Create superuser if it doesn't exist (using environment variables)
if ! python manage.py changepassword admin &>/dev/null; then
    echo "Superuser 'admin' does not exist. Creating it..."
    python manage.py createsuperuser --noinput
else
    echo "Superuser 'admin' already exists."
fi

# Start the Django server.
python manage.py runserver 0.0.0.0:8000