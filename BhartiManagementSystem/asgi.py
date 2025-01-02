"""
ASGI config for BhartiManagementSystem project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from dotenv import load_dotenv


from django.core.asgi import get_asgi_application


load_dotenv()
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    os.getenv('DJANGO_SETTINGS_MODUE', 'BhartiManagementSystem.settings.base'))

application = get_asgi_application()
