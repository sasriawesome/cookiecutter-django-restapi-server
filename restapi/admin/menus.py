from restapi.core.menus import MenuItem, Menu, MenuDropdown
from django.utils.functional import lazy
from django.shortcuts import reverse

class ModelAdminMenuItem(MenuItem):
    """
    A sub-class of MenuItem, include modeladmin on init"""

    def __init__(self, modeladmin, order):
        self.modeladmin = modeladmin
        self.icon = modeladmin.get_menu_icon()
        url_name = modeladmin.get_url_name('changelist')
        super().__init__(
            label=modeladmin.get_menu_label(), url=reverse(url_name),
            icon=self.icon, order=order
        )

    def is_shown(self, request):
        return self.modeladmin.has_any_permission(request)


class ModelAdminDropdownMenuItem(MenuItem):
    template = 'sites/shared/navbar_menu_dropdown_item.html'

    def __init__(self, modeladmin, order):
        self.modeladmin = modeladmin
        self.icon = modeladmin.get_menu_icon()
        url = modeladmin.url_helper.get_url('index', False)
        super().__init__(
            label=modeladmin.get_menu_label(), url=url,
            icon=self.icon, order=order
        )

    def is_shown(self, request):
        return self.modeladmin.has_any_permission(request)


class ModelAdminGroupMenuItem(MenuDropdown):
    """
    A sub-class of SubmenuMenuItem, used by ModelAdminGroup to add a
    link to the main menu with its own submenu, linking to various listing
    pages
    """

    def __init__(self, modeladmin_group, order, menu):
        self.icon = modeladmin_group.get_menu_icon()
        super().__init__(
            label=modeladmin_group.get_menu_label(), menu=menu,
            icon=self.icon, order=order, )

    def is_shown(self, request):
        """
        If there aren't any visible items in the submenu, don't bother to show
        this menu item
        """
        # for menuitem in self.menu._registered_menu_items:
        #     if menuitem.is_shown(request):
        #         return True
        return True


class SubMenu(Menu):
    """
    A sub-class of Admin Menu, used by AppModelAdmin. We just want to
    override __init__, so that we can specify the items to include on
    initialisation
    """

    def __init__(self, menuitem_list):
        self._registered_menu_items = menuitem_list


admin_menu = Menu()