from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _

class AppConfig(BaseAppConfig):
    name = 'restapi.modules.todo'
    label = 'restapi_todo'
    verbose_name = _('Restapi ToDo')