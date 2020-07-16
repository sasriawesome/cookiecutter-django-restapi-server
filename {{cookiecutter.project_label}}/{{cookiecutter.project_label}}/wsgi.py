"""
WSGI config for {{cookiecutter.project_title}} project.

"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{cookiecutter.project_label}}.settings')
application = get_wsgi_application()
