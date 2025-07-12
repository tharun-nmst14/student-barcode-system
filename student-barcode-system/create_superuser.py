import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crud.settings")
django.setup()

User = get_user_model()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@.com", "admin123")
    print("✅ Superuser created: admin / admin123")
else:
    print("ℹ️ Superuser already exists.")
