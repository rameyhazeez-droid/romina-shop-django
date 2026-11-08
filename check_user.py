import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ourawsomecart.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

print("--- EXPORTING ALL REGISTERED BACKEND USERNAMES ---")
for user in User.objects.all():
    print(f"FOUND USERNAME: {user.username}")
print("-------------------------------------------------")
