#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip

# Install Python deps without pinned GDAL first
grep -v -i '^gdal==' requirements.txt > /tmp/requirements.nogdal.txt
pip install -r /tmp/requirements.nogdal.txt

# Bind GDAL Python package to the system GDAL version from Aptfile
if command -v gdal-config >/dev/null 2>&1; then
  GDAL_VER="$(gdal-config --version)"
  pip install "gdal==${GDAL_VER}"
else
  echo "WARNING: gdal-config not found; GIS features may fail"
fi

python manage.py collectstatic --noinput
python manage.py migrate --noinput
