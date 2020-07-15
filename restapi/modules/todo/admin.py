from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from admin_numeric_filter.admin import (
    SingleNumericFilter,
    RangeNumericFilter,
    SliderNumericFilter
)

from restapi.admin.sites import admin_site
from restapi.admin.admin import ModelAdmin, ModelAdminPDFPrintMixin
from .models import Work, Note

# Custom Django Admin Filter Examples
class CustomSliderNumericFilter(SliderNumericFilter):
    MAX_DECIMALS = 2
    STEP = 2

class WorkAdmin(ModelAdminPDFPrintMixin, ModelAdmin):
    inspect_enabled = True
    menu_icon = 'briefcase-variant'
    menu_label = 'Pelanggan'
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
    menu_label = 'Permintaan Jasa'
    menu_icon = 'clipboard-outline'
    inspect_enabled = True
    list_per_page = 10
    list_display = ['title']
    search_fields = ['title']
    list_filter = [
        ('created_at', DateRangeFilter)
    ]

admin.site.register(Note, NoteAdmin)
admin.site.register(Work, WorkAdmin)

from restapi.admin.menus import admin_menu
from restapi.admin.admin import ModelMenuGroup

class TodoModelMenuGroup(ModelMenuGroup):
    adminsite = admin.site
    menu_icon = 'book'
    menu_label = 'Pelayanan Jasa Teknis'
    menu_order = 5
    items = [ (Note, NoteAdmin), (Work, WorkAdmin) ]

@admin_menu.register
def todo_admin_group(request):
    group = TodoModelMenuGroup()
    return group.get_menu_item()