from django import template
from restapi.admin.menus import admin_menu, MenuItem

register = template.Library()


@register.inclusion_tag('admin/sidenav_main.html', takes_context=True)
def admin_sidenav(context):
    request = context['request']
    return {
        'menu_html': admin_menu.render_html(request),
        'request': request,
    }