from django.views import View
from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from {{cookiecutter.project_label}}.modules.todo.models import Work
from .serializers import WorkSerializer

class RootView(View):
    def get(self, request):
        return JsonResponse(data={'message': 'Welcome to {{cookiecutter.project_title}} V1'})


class WorkViewSet(ModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer

    @action(methods=['get'], detail=False, url_path='notify')
    def notify(self, request):
        Work.send_email("{{cookiecutter.project_author}}", "Hello")
        return JsonResponse({'message': "{{cookiecutter.project_author}}"})