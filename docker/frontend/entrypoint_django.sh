#!/bin/bash

# Check if database exists.
if ! mysql -u"$DB_USER" -p"$DB_PASSWORD" -h"$DB_HOST" -e "USE $DB_DATABASE"; then
  echo "Database does not exist. Creating it..."
  mysql -u"$DB_USER" -p"$DB_PASSWORD" -h"$DB_HOST" -e "CREATE DATABASE $DB_DATABASE"
fi

# Check if migrations have been run (by looking for a specific table).
# Customize this table if necessary.
if ! python manage.py showmigrations | grep -q "[X]"; then
    echo "Migrations have not been run. Running them now..."
    python manage.py migrate
else
    echo "Migrations have already been run."
fi

# Start the Django server.
python manage.py runserver 0.0.0.0:8000
