from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _

class AppConfig(BaseAppConfig):
    name = '{{cookiecutter.project_label}}.auth'
    label = '{{cookiecutter.project_label}}_auth'
    verbose_name = _('{{cookiecutter.project_title}} Auth')