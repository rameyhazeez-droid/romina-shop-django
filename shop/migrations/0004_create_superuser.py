from django.db import migrations
from django.contrib.auth.models import User

def create_superuser(apps, schema_editor):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@rameycart.com',
            password='MySecretPassword123'  # <-- CHANGE THIS TO YOUR SECRET PASSWORD
        )

class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0003_alter_product_desc_productimage'), # Links to your image migration file
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
