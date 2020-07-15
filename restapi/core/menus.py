from django.forms import Media, MediaDefiningClass
from django.forms.utils import flatatt
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.text import slugify


class MenuItem(metaclass=MediaDefiningClass):
    template = 'sites/shared/navbar_menu_item.html'

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
        return request.path.startswith(str(self.url))

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
    template = 'sites/shared/navbar_menu_dropdown.html'

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


class Menu:

    def __init__(self):
        self._registered_menu_items = []

    def register(self, menu_item):
        if not isinstance(menu_item, MenuItem):
            raise ValueError('menu_item should be MenuItem subclass')
        self._registered_menu_items.append(menu_item)

    @property
    def registered_menu_items(self):
        return self._registered_menu_items

    def menu_items_for_request(self, request):
        return [item for item in self.registered_menu_items if
                item.is_shown(request)]

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


class AdminOnlyMenuItem(MenuItem):
    """A MenuItem which is only shown to superusers"""

    def is_shown(self, request):
        return request.user.is_superuser


class ModelSiteMenuItem(MenuItem):
    """
    A sub-class of MenuItem, include modelsite on init"""

    def __init__(self, modelsite, order):
        self.modelsite = modelsite
        self.icon = modelsite.get_menu_icon()
        url = modelsite.url_helper.get_url('index', False)
        super().__init__(
            label=modelsite.get_menu_label(), url=url,
            icon=self.icon, order=order
        )

    def is_shown(self, request):
        return self.modelsite.permission_helper.user_can_list(request.user)


class ModelSiteDropdownMenuItem(MenuItem):
    template = 'sites/shared/navbar_menu_dropdown_item.html'

    def __init__(self, modelsite, order):
        self.modelsite = modelsite
        self.icon = modelsite.get_menu_icon()
        url = modelsite.url_helper.get_url('index', False)
        super().__init__(
            label=modelsite.get_menu_label(), url=url,
            icon=self.icon, order=order
        )

    def is_shown(self, request):
        return self.modelsite.permission_helper.user_can_list(request.user)


class ModelSiteGroupMenuItem(MenuDropdown):
    """
    A sub-class of SubmenuMenuItem, used by ModelAdminGroup to add a
    link to the main menu with its own submenu, linking to various listing
    pages
    """

    def __init__(self, modelsitegroup, order, menu):
        self.icon = modelsitegroup.get_menu_icon()
        super().__init__(
            label=modelsitegroup.get_menu_label(), menu=menu,
            icon=self.icon, order=order, )

    def is_shown(self, request):
        """
        If there aren't any visible items in the submenu, don't bother to show
        this menu item
        """
        for menuitem in self.menu._registered_menu_items:
            if menuitem.is_shown(request):
                return True
        return False


class SubMenu(Menu):
    """
    A sub-class of wagtail's Menu, used by AppModelAdmin. We just want to
    override __init__, so that we can specify the items to include on
    initialisation
    """

    def __init__(self, menuitem_list):
        self._registered_menu_items = menuitem_list


website_menu = Menu()
admin_menu = Menu()
