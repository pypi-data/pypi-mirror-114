from django.views.generic import ListView

from medux.core.views import MeduxBaseMixin
from ..models import AccountActivity


class CashbookIndexView(MeduxBaseMixin, ListView):
    template_name = "cashbook/accountactivities.html"
    model = AccountActivity
    permission_required = ["cashbook.view_accountactivity"]
    extra_context = {"amount": "", "comment": ""}

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context["amount"] = None
    #     return context
