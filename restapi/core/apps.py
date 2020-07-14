from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _

class AppConfig(BaseAppConfig):
    name = 'restapi.core'
    label = 'restapi_core'
    verbose_name = _('Restapi Core')