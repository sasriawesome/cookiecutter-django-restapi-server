from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _

class AppConfig(BaseAppConfig):
    name = '{{cookiecutter.project_label}}.admin'
    label = '{{cookiecutter.project_label}}_admin'
    verbose_name = _('{{cookiecutter.project_title}} Admin')