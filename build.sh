#!/usr/bin/env bash
set -o errexit

echo "==> Installing system GIS packages (if needed)"
if ! command -v gdal-config >/dev/null 2>&1; then
  if command -v apt-get >/dev/null 2>&1; then
    apt-get update
    apt-get install -y --no-install-recommends \
      gdal-bin libgdal-dev libgeos-dev libproj-dev binutils gcc g++
  else
    echo "ERROR: apt-get and gdal-config both unavailable"
    exit 1
  fi
fi

echo "==> GDAL version: $(gdal-config --version)"
export CPLUS_INCLUDE_PATH="${CPLUS_INCLUDE_PATH}:/usr/include/gdal"
export C_INCLUDE_PATH="${C_INCLUDE_PATH}:/usr/include/gdal"

echo "==> Upgrading pip"
pip install --upgrade pip setuptools wheel

echo "==> Installing Python requirements"
pip install -r requirements.txt

echo "==> Installing Python GDAL bindings for system version"
pip install "gdal==$(gdal-config --version)"

echo "==> collectstatic"
python manage.py collectstatic --noinput

echo "==> migrate"
python manage.py migrate --noinput

echo "==> Build finished successfully"
