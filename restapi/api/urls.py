from django.urls import path, include

from .schemas import SchemaView
from .v1.routes import api_urls as v1_urls


urlpatterns = [
    path('v1/', include(v1_urls)),
    path('', SchemaView.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]