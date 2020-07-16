from constance import config
from django.conf import settings as app_settings

def settings(request):
    return {
        'constance': config,
        'debug_mode': app_settings.DEBUG,
        'project_name': getattr(app_settings, 'PROJECT_NAME', '{{cookiecutter.project_title}}'),
        'project_version': getattr(app_settings, 'PROJECT_VERSION', 'Cloud Version'),
    }