"""
WSGI config for smart_restaurant project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_restaurant.settings')

application = get_wsgi_application()

# Automatically create superuser on application startup
try:
    from create_superuser import create_admin
    create_admin()
except Exception as e:
    import sys
    print(f"Auto superuser creation failed: {e}", file=sys.stderr)
