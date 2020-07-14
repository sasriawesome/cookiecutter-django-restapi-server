from functools import update_wrapper
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import AdminSite

class CustomAdminSite(AdminSite):
    """ 
        Custom Admin Site provide custom behaviour and Authentication
    """
    # Text to put at the end of each page's <title>.
    site_title = _('Web Project')

    # Text to put in each page's <h1>.
    site_header = _('Web Project')

    # Text to put at the top of the admin index page.
    index_title = _('Site administration')

    # URL for the "View site" link at the top of each admin page.
    site_url = '/'
    

    def has_permission(self, request):
        """
        Return True if the given HttpRequest has permission to view
        *at least one* page in the admin site.
        """
        return request.user.is_active and request.user.is_staff

admin_site = CustomAdminSite(name='custom_admin')