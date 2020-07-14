from django.views import View
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet

from restapi.modules.todo.models import Work
from .serializers import WorkSerializer

class RootView(View):
    def get(self, request):
        return JsonResponse(data={'message': 'Welcome to API V1'})


class WorkViewSet(ModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer