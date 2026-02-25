#!/usr/bin/env bash
set -o errexit
# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

apt-get update
apt-get install -y gdal-bin libgdal-dev
