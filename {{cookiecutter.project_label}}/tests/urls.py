"""
{{cookiecutter.project_title}} TEST URL Configuration

"""
from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path('api/', include('{{cookiecutter.project_label}}.api.urls'))
]

if settings.DEBUG:
    from django.contrib import admin
    urlpatterns += [
        path('admin/', admin.site.urls),
    ]