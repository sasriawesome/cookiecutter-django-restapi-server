from django.contrib import admin
from .models import Work


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'is_done']
    list_filter = ['created_at']