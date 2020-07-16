from django.db import models
from {{cookiecutter.project_label}}.core.models import BaseModel
from .workers import send_email

class Work(BaseModel):

    class Meta:
        verbose_name = 'Todo'
        verbose_name_plural = 'Todo'
    
    title = models.CharField(max_length=250)
    score = models.IntegerField(default=0)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @staticmethod
    def send_email(recipient, message):
        try:
            send_email(recipient, message)
            return True
        except Exception as err:
            print(err)
            return False


class Note(BaseModel):

    class Meta:
        verbose_name = 'Note'
        verbose_name_plural = 'Note'
    
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=False)

    def __str__(self):
        return self.title