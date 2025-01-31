#!/bin/bash

set -e



echo "Running migrations..."
./venv/bin/python3 manage.py migrate

echo "Loading data for users..."
./venv/bin/python3 manage.py loaddata data/users.json

echo "Loading data for polls..."
./venv/bin/python3 manage.py loaddata data/polls.json

echo "Loading data for votes..."
./venv/bin/python3 manage.py loaddata data/vote.json

echo "Starting Django development server..."
./venv/bin/python3 manage.py runserver 0.0.0.0:8000 --insecure