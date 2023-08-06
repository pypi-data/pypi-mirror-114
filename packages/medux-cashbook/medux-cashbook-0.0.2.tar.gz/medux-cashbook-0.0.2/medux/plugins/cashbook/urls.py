from django.urls import path

from .views import CashbookIndexView

app_name = "cashbook"

urlpatterns = [
    path("", CashbookIndexView.as_view(), name="index"),
]
