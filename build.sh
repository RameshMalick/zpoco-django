#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Convert static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate

# Load initial data
python manage.py loaddata initial_data.json
python manage.py loaddata users.json
