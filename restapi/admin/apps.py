from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _

class AppConfig(BaseAppConfig):
    name = 'restapi.admin'
    label = 'restapi_admin'
    verbose_name = _('Restapi Admin')