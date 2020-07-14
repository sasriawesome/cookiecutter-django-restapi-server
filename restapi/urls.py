"""
{{cookiecutter.project_name}} URL Configuration

"""
from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path('api/', include('restapi.api.urls'))
]

if settings.DEBUG:
    from django.contrib import admin
    urlpatterns += [
        path('admin/', admin.site.urls),
    ]
