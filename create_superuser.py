import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tu_proyecto.settings')  # cambia 'tu_proyecto'

django.setup()

User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    print("Superusuario creado.")
else:
    print("Ya existe el superusuario.")