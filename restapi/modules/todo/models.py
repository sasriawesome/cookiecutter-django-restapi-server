from django.db import models
from restapi.core.models import BaseModel


class Work(BaseModel):

    class Meta:
        verbose_name = 'Todo'
        verbose_name_plural = 'Todo'
    
    title = models.CharField(max_length=250)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.title