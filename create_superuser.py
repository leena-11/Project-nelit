import os
import django

def create_admin():
    # Setup Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_restaurant.settings')
    django.setup()

    from django.contrib.auth import get_user_model

    User = get_user_model()
    
    # Read environment variables with fallback defaults to ensure deployability without manual setup
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME') or os.environ.get('SUPERUSER_USERNAME') or 'admin'
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL') or os.environ.get('SUPERUSER_EMAIL') or 'admin@example.com'
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD') or os.environ.get('SUPERUSER_PASSWORD') or 'admin123'

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
