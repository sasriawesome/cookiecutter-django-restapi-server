from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _

class AppConfig(BaseAppConfig):
    name = 'restapi.auth'
    label = 'restapi_auth'
    verbose_name = _('Restapi Auth')