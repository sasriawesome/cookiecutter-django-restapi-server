from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.shortcuts import reverse
from django.template.response import TemplateResponse

from restapi.admin.sites import admin_site
from admin_numeric_filter.admin import NumericFilterModelAdmin


class ModelAdmin(NumericFilterModelAdmin, admin.ModelAdmin):
    """ Add Inspect view feature to ModelAdmin """

    inspect_template = None
    inspect_enabled = False

    def get_urls(self):
        from django.urls import path
        info = self.model._meta.app_label, self.model._meta.model_name
        urls = super().get_urls()
        custom_urls = []
        if self.inspect_enabled:
            custom_urls.append(
                path('<path:object_id>/inspect/',
                     self.admin_site.admin_view(self.inspect_view),
                     name='%s_%s_inspect' % info
                     )
            )
        return custom_urls + urls

    def inspect_view(self, request, object_id, extra_context=None):
        obj = self.get_object(request, object_id)
        if not self.has_view_or_change_permission(request, obj):
            return PermissionError("You don't have any permissions")
        context = {
            **self.admin_site.each_context(request),
            'self': self,
            'opts': self.opts,
            'instance': obj,
            **(extra_context or {})
        }

        return TemplateResponse(request, self.inspect_template or [
            'admin/%s_%s_inspect.html' % (self.opts.app_label, self.opts.model_name),
            'admin/%s_inspect.html' % self.opts.app_label,
            'admin/inspect.html'
        ], context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        if not self.has_view_or_change_permission(request, obj):
            raise PermissionError(_("You don't have any permission!"))
        if self.has_change_permission(request, obj):
            return self.changeform_view(request, object_id, form_url, extra_context)
        return self.inspect_view(request, object_id, extra_context)

    def _get_url_name(self, obj, action):
        return 'custom_admin:%s_%s_%s' % (
            self.opts.app_label,
            self.opts.model_name,
            action
        )

    def get_list_display(self, request):
        list_display = self.list_display.copy()
        if self.has_change_permission(request):
            list_display.append('edit_link')
        if self.has_delete_permission(request):
            list_display.append('delete_link')
        if self.has_view_or_change_permission(request):
            list_display.append('view_link')
        return list_display

    def edit_link(self, obj):
        template = "<a class='changelink' href='%s' title='%s'></a>"
        url = reverse(self._get_url_name(obj, 'change'), args=(obj.id,))
        return format_html(template % (url, _('edit').title()))

    def delete_link(self, obj):
        template = "<a class='deletelink' href='%s' title='%s'></a>"
        url = reverse(self._get_url_name(obj, 'delete'), args=(obj.id,))
        return format_html(template % (url, _('delete').title()))

    def view_link(self, obj):
        template = "<a class='viewlink' href='%s' title='%s'></a>"
        url = reverse(self._get_url_name(obj, 'inspect'), args=(obj.id,))
        return format_html(template % (url, _('inspect').title()))

    edit_link.short_description=''
    delete_link.short_description=''
    view_link.short_description=''