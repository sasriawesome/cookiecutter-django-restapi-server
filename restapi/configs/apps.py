from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _

class AppConfig(BaseAppConfig):
    name = 'restapi.configs'
    label = 'restapi_configs'
    verbose_name = _('Rest API Configs')