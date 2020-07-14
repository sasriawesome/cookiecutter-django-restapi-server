"""
{{cookiecutter.project_name}} URL Configuration

"""
from django.conf import settings
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('api/', include('restapi.api.urls'))
    path('admin/', admin.site.urls),
    
]

if settings.DEBUG:
    urlpatterns += [
        path('admin/queues/', include('django_rq.urls'))
    ]
