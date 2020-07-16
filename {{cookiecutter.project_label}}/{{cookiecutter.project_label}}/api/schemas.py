from collections import OrderedDict
from rest_framework import serializers
from rest_framework import permissions

from drf_yasg import openapi
from drf_yasg.utils import no_body
from drf_yasg.views import get_schema_view
from drf_yasg.inspectors import SwaggerAutoSchema


class BlankMeta:
    pass


def serializer_factory(serializer_type, serializer):
    class CustomSerializer(serializer.__class__):

        class Meta(getattr(serializer.__class__, 'Meta', BlankMeta)):
            ref_name = serializer_type + serializer.__class__.__name__

        def get_fields(self):
            new_fields = OrderedDict()
            for fieldName, field in super().get_fields().items():
                if serializer_type == 'Write':
                    condition = field.read_only
                else:
                    condition = field.write_only
                # create new serializer for Read or Write
                if not condition:
                    if isinstance(field, serializers.ListSerializer):
                        # create new serializer for Array Item
                        new_fields[fieldName] = serializer_factory(
                            serializer_type, field.child
                        )
                    elif isinstance(field, serializers.Serializer):
                        new_fields[fieldName] = serializer_factory(
                            serializer_type, field
                        )
                    else:
                        new_fields[fieldName] = field
            return new_fields

    return CustomSerializer(data=serializer.data)


class ReadWriteAutoSchema(SwaggerAutoSchema):
    def get_view_serializer(self):
        return serializer_factory('Write', super().get_view_serializer())

    def get_default_response_serializer(self):
        body_override = self._get_request_body_override()
        if body_override and body_override is not no_body:
            return body_override

        return serializer_factory('Read', super().get_view_serializer())

SchemaView = get_schema_view(
    openapi.Info(
        title="REST API",
        default_version='v1',
        description="Restapi Description",
        terms_of_service="https://www.ahaastudio.com/policies/terms/",
        contact=openapi.Contact(email="contact@ahaastudio.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)