FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    gdal-bin libgdal-dev libgeos-dev libproj-dev binutils \
    gcc g++ \
    && rm -rf /var/lib/apt/lists/*

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel \
    && grep -v -iE '^gdal==|^#.*GDAL' requirements.txt > /tmp/requirements.nogdal.txt \
    && pip install -r /tmp/requirements.nogdal.txt \
    && pip install "gdal==$(gdal-config --version)"

COPY . .

RUN chmod +x ./build.sh

CMD gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120
