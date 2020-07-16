from django.forms import Media, MediaDefiningClass
from django.forms.utils import flatatt
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.text import slugify

_admin_menu_registry = []


def register_menu(func):
    _admin_menu_registry.append(func)


class MenuItem(metaclass=MediaDefiningClass):
    template = 'admin/sidenav_menu_item.html'

    def __init__(self, label, url, icon='', name=None, classnames='',
                 attrs=None, order=1000):
        self.label = label
        self.url = url
        self.classnames = classnames
        self.name = (name or slugify(str(label)))
        self.order = order
        self.icon = icon

        if attrs:
            self.attr_string = flatatt(attrs)
        else:
            self.attr_string = ""

    def is_shown(self, request):
        """
        Whether this menu item should be shown for the given request; permission
        checks etc should go here. By default, menu items are shown all the time
        """
        return True

    def is_active(self, request):
        return request.path == str(self.url)

    def get_context(self, request):
        """Defines context for the template, overridable to use more data"""
        return {
            'name': self.name,
            'url': self.url,
            'classnames': self.classnames,
            'attr_string': self.attr_string,
            'label': self.label,
            'active': self.is_active(request),
            'icon': self.icon
        }

    def render_html(self, request):
        context = self.get_context(request)
        return render_to_string(self.template, context, request=request)


class MenuDropdown(MenuItem):
    template = 'admin/sidenav_menu_dropdown.html'

    """A MenuItem which wraps an inner Menu object"""

    def __init__(self, label, menu, **kwargs):
        self.menu = menu
        super().__init__(label, '#', **kwargs)

    def is_shown(self, request):
        # show the submenu if one or more of its children is shown
        return bool(self.menu.menu_items_for_request(request))

    def is_active(self, request):
        return bool(self.menu.active_menu_items(request))

    def get_context(self, request):
        context = super().get_context(request)
        context['menu_html'] = self.menu.render_html(request)
        context['request'] = request
        return context


class AdminOnlyMenuItem(MenuItem):
    """A MenuItem which is only shown to superusers"""

    def is_shown(self, request):
        return request.user.is_superuser


class Menu:

    def __init__(self):
        self._registered_menu_items = []

    def register(self, func):
        self._registered_menu_items.append(func)
        

    @property
    def registered_menu_items(self):
        return self._registered_menu_items

    def menu_items_for_request(self, request):
        menu_items = [item(request) for item in self.registered_menu_items]
        return [ item for item in menu_items if item.is_shown(request)]

    def active_menu_items(self, request):
        return [item for item in self.menu_items_for_request(request) if
                item.is_active(request)]

    @property
    def media(self):
        media = Media()
        for item in self.registered_menu_items:
            media += item.media
        return media

    def render_html(self, request):
        menu_items = self.menu_items_for_request(request)

        # provide a hook for modifying the menu, if construct_hook_name has been set

        rendered_menu_items = []
        for item in sorted(menu_items, key=lambda i: i.order):
            rendered_menu_items.append(item.render_html(request))
        return mark_safe(''.join(rendered_menu_items))


website_menu = Menu()
