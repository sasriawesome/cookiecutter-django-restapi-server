"""
{{cookiecutter.project_name}} URL Configuration

"""
from django.conf import settings
from django.urls import path, include
from django.contrib import admin

from restapi.admin.sites import admin_site

urlpatterns = [
    path('api/', include('restapi.api.urls')),
    path('admin/', admin.site.urls)
]

if settings.DEBUG:
    urlpatterns += [
        path('admin/queues/', include('django_rq.urls'))
    ]
