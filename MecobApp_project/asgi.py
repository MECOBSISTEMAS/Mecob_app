#A pasta MecobApp_project é a parte das configurações da aplicação, o arquivo asgi.py veio por default, ele cuida das requisições assincronas

"""
ASGI config for MecobApp_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MecobApp_project.settings')

application = get_asgi_application()
