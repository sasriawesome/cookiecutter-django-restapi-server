from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.shortcuts import reverse
from django.template.response import TemplateResponse
from django.urls import path

from admin_numeric_filter.admin import NumericFilterModelAdmin

from {{cookiecutter.project_label}}.admin.views import PDFPrintDetailView
from {{cookiecutter.project_label}}.admin.sites import admin_site
from {{cookiecutter.project_label}}.admin.menus import (
    admin_menu, 
    SubMenu,
    ModelAdminMenuItem,
    ModelAdminGroupMenuItem,
    MenuItem
)


class ModelAdminPDFPrintMixin(admin.ModelAdmin):

    print_view_class = PDFPrintDetailView
    print_template = 'admin/print/content.html'
    document_title = None
    document_show_cover = False
    document_show_header = True
    document_show_footer = True
    
    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.model_name
        urls = super().get_urls()
        custom_urls = []
        custom_urls.append(
            path('<path:object_id>/print/',
                    self.admin_site.admin_view(self.print_view),
                    name='%s_%s_print' % info
                    )
        )
        return custom_urls + urls

    def print_view(self, request, object_id, *args, **kwargs):
        kwargs.update(**{
            'modeladmin':self,
            'instance_pk':object_id
        })
        view_class = self.print_view_class
        return view_class.as_view(**kwargs)(request)

    def get_list_display(self, request):
        list_display = super().get_list_display(request).copy()
        if self.has_view_or_change_permission(request):
            list_display.append('print_link')
        return list_display
        
    def print_link(self, obj):
        template = "<a class='printlink' target='_blank' href='%s' title='%s'>" \
                   "<i class='mdi mdi-printer'></i></a>"
        url = reverse(self.get_url_name('print'), args=(obj.id,))
        return format_html(template % (url, _('print').title()))
    
    print_link.short_description=''


class ModelAdminMenuMixin(admin.ModelAdmin):

    menu_icon = None
    menu_label = None
    menu_order = None
    menu_class = ModelAdminMenuItem


    def get_menu_label(self):
        return self.menu_label or self.opts.verbose_name_plural.title()

    def get_menu_icon(self):
        return self.menu_icon

    def get_menu_order(self):
        return self.menu_order or 1000

    def get_menu_class(self):
        return self.menu_class

    def get_menu_item(self, order=None):
        
        def get_menu(request):
            return self.menu_class(self, order or self.get_menu_order())
        
        return get_menu


class ModelAdmin(NumericFilterModelAdmin, ModelAdminMenuMixin, admin.ModelAdmin):
    """ Add Inspect view feature to ModelAdmin """

    inspect_template = None
    inspect_enabled = False

    def has_any_permission(self, request, obj=None):
        return (
            self.has_add_permission(request)
            or self.has_view_or_change_permission(request)
        )

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

    def get_url_name(self, action):
        return '%s:%s_%s_%s' % (
            self.admin_site.name,
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
        url = reverse(self.get_url_name('change'), args=(obj.id,))
        return format_html(template % (url, _('edit').title()))
    
    def delete_link(self, obj):
        template = "<a class='deletelink' href='%s' title='%s'></a>"
        url = reverse(self.get_url_name('delete'), args=(obj.id,))
        return format_html(template % (url, _('delete').title()))

    def view_link(self, obj):
        template = "<a class='viewlink' href='%s' title='%s'></a>"
        url = reverse(self.get_url_name('inspect'), args=(obj.id,))
        return format_html(template % (url, _('inspect').title()))

    edit_link.short_description=''
    delete_link.short_description=''
    view_link.short_description=''


class ModelMenuGroup:
    menu_icon = None
    menu_label = None
    menu_order = None
    adminsite = None
    items = []

    def __init__(self):
        self.modeladmins = []
        self.get_modeladmin_instance()

    def get_items(self):
        return self.items

    def get_modeladmin_instance(self):
        if bool(self.items):
            for model, modeladmin in self.get_items():
                if model not in self.adminsite._registry:
                    continue
                self.modeladmins.append(
                    modeladmin(model, self.adminsite)
                )
            return self.modeladmins
        else:
            return []

    def get_menu_label(self):
            return self.menu_label

    def get_menu_icon(self):
        return self.menu_icon

    def get_menu_order(self):
        return self.menu_order or 1000

    def get_menu_item(self):
        if self.modeladmins:
            submenu = SubMenu(self.get_submenu_items())
            return ModelAdminGroupMenuItem(self, self.get_menu_order(), submenu)

    def get_submenu_items(self):
        menu_items = []
        item_order = 1
        for modeladmin in self.modeladmins:
            menu_items.append(modeladmin.get_menu_item(order=item_order))
            item_order += 1
        return menu_items

@admin_menu.register
def admin_home_menu(request):
    return MenuItem(
        'Home', reverse('admin:index'), 'home', 'home_menu', order=1
    )