#!/usr/bin/env bash
# build.sh
echo "Aplicando migraciones..."
python manage.py migrate
python create_superuser.py

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput
