import os
import django

# Set DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_restaurant.settings')

# Call django.setup()
django.setup()

from django.contrib.auth import get_user_model

def create_admin():
    User = get_user_model()
    
    # Read credentials from environment variables with defaults
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

    # Create a superuser only if one does not already exist
    if not User.objects.filter(username=username).exists():
        print(f"Creating superuser '{username}'...")
        User.objects.create_superuser(username=username, email=email, password=password)
        print("Superuser created successfully.")
    else:
        print(f"Superuser '{username}' already exists.")

if __name__ == '__main__':
    try:
        create_admin()
    except Exception as e:
        import sys
        print(f"Error creating superuser: {e}", file=sys.stderr)
