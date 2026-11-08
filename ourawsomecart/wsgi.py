import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ourawsomecart.settings')
application = get_wsgi_application()

# --- AUTO ADMIN GENERATOR BLOCK ---
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    username = 'ramey_admin'  # <--- This is your new definitive username
    email = 'support@rameycart.com'
    password = 'SecurePassword786!'  # <--- This is your new secure password

    if not User.objects.filter(username=username).exists():
        print(f"WSGI Init: Creating superuser {username}...")
        User.objects.create_superuser(username, email, password)
        print("WSGI Init: Superuser created successfully!")
    else:
        print(f"WSGI Init: Superuser {username} already exists.")
except Exception as e:
    print(f"WSGI Init: Admin account generation failed -> {e}")
# ----------------------------------
