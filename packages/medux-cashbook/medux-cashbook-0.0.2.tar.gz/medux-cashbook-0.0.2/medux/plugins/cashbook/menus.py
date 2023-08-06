from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# from menu import Menu

from medux.core.api import IViewMode

# from medux.core.api.menus import MenuItem

# Menu.add_item("main_menu", MenuItem(title=_("Cashbook"), url=reverse("cashbook:index")))


class CashbookViewMode(IViewMode):
    title = _("Cashbook")
    icon = "bi-wallet"
    url = reverse("cashbook:index")
    weight = 20
