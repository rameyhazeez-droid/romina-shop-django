import os
import django

# Setup django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ourawsomecart.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = 'admin'  # <-- Change this to your preferred username
email = 'support@rameycart.com'
password = 'hazeez7053951'  # <-- Change this to a secure password

if not User.objects.filter(username=username).exists():
    print(f"Creating superuser {username}...")
    User.objects.create_superuser(username, email, password)
    print("Superuser created successfully!")
else:
    print(f"Superuser {username} already exists.")
