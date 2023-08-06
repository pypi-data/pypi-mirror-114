from django.contrib import admin

from .models import Balance, AccountActivity


class BalanceAdmin(admin.ModelAdmin):
    model = Balance


class AccountActivityAdmin(admin.ModelAdmin):
    model = AccountActivity


# admin.site.register(Balance, BalanceAdmin)
# admin.site.register(AccountActivity, AccountActivityAdmin)
