#!/usr/bin/env bash
# build.sh
echo "Aplicando migraciones..."
python manage.py migrate

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput
