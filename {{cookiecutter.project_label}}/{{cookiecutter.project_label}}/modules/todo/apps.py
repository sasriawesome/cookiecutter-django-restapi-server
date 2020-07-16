from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _

class AppConfig(BaseAppConfig):
    name = '{{cookiecutter.project_label}}.modules.todo'
    label = '{{cookiecutter.project_label}}_todo'
    verbose_name = _('Work and Service')