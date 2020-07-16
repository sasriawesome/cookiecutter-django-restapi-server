from functools import update_wrapper
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import AdminSite
from django.conf import settings

site_title = getattr(settings, 'PROJECT_TITLE', '{{cookiecutter.project_title}}')
site_sub_title = getattr(settings, 'PROJECT_SUBTITLE', '{{cookiecutter.project_subtitle}}')
site_description = getattr(settings, 'PROJECT_DESCRIPTION', '{{cookiecutter.project_description}}')

class CustomAdminSite(AdminSite):
    """ 
        Custom Admin Site provide custom behaviour and Authentication
    """
    site_title = site_title
    site_header = site_title
    index_title = _('Site administration')
    
    site_url = '/'
    
    def each_context(self, request):
        context = super().each_context(request)
        context['site_sub_title'] = site_sub_title
        return context

    def has_permission(self, request):
        """
        Return True if the given HttpRequest has permission to view
        *at least one* page in the admin site.
        """
        return request.user.is_active and request.user.is_staff

admin_site = CustomAdminSite(name='custom_admin')