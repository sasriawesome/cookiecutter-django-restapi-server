from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _

class AppConfig(BaseAppConfig):
    name = 'restapi.api'
    label = 'restapi_api'
    verbose_name = _('Restapi API')