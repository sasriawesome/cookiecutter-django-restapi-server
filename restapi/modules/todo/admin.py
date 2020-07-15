from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from admin_numeric_filter.admin import (
    SingleNumericFilter,
    RangeNumericFilter,
    SliderNumericFilter
)

from restapi.admin.sites import admin_site
from restapi.admin.admin import ModelAdmin
from .models import Work, Note

# Custom Django Admin Filter Examples
class CustomSliderNumericFilter(SliderNumericFilter):
    MAX_DECIMALS = 2
    STEP = 2

class WorkAdmin(ModelAdmin):
    inspect_enabled = True
    list_per_page = 10
    list_display = ['title', 'created_at', 'score','is_done']
    search_fields = ['title']
    list_filter = [
        ('created_at', DateRangeFilter),
        ('score', SingleNumericFilter), # Single field search, __gte lookup
        ('score', RangeNumericFilter), # Range search, __gte and __lte lookup
        ('score', SliderNumericFilter), # Same as range above but with slider
        'is_done',
    ]


class NoteAdmin(ModelAdmin):
    inspect_enabled = True
    list_per_page = 10
    list_display = ['title']
    search_fields = ['title']
    list_filter = [
        ('created_at', DateRangeFilter)
    ]

admin_site.register(Note, NoteAdmin)
admin_site.register(Work, WorkAdmin)