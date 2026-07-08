import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_restaurant.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

USERNAME = "admin"
EMAIL = "admin@example.com"
PASSWORD = "Leena@2026"

if not User.objects.filter(username=USERNAME).exists():
    User.objects.create_superuser(
        username=USERNAME,
        email=EMAIL,
        password=PASSWORD
    )
    print("✅ Superuser created successfully!")
else:
    print("✅ Superuser already exists.")