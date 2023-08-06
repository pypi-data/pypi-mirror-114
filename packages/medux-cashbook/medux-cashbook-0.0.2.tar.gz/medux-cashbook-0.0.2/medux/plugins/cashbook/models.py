from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from medux.core.api import CreatedUpdatedMixin

User = get_user_model()


class Balance(CreatedUpdatedMixin):
    """Represents an account balance at a certain timestamp.

    Do NOT create a Balance yourself, this model is automatically created when
    adding an AccountActivity."""

    timestamp = models.DateTimeField()
    amount = MoneyField(max_digits=19, decimal_places=2, default_currency="EUR")

    class Meta:
        verbose_name = _("Balance")
        verbose_name_plural = _("Balances")

    def __str__(self):
        return str(self.amount)


class AccountActivity(CreatedUpdatedMixin):
    timestamp = models.DateTimeField()
    amount = MoneyField(max_digits=19, decimal_places=2, default_currency="EUR")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.ForeignKey(Balance, on_delete=models.PROTECT, editable=False)
    comment = models.CharField(max_length=255, blank=True, null=True)
    # payment = models.ForeignKey()

    class Meta:
        verbose_name = _("Account activity")
        verbose_name_plural = _("Account activities")

    def save(self, *args, **kwargs):
        last = Balance.objects.last()
        if last:
            last_amount = last.amount
        else:
            last_amount = 0.0

        # create new balance entry
        balance = Balance(timestamp=self.timestamp)
        balance.amount = last_amount + self.amount
        balance.save()
        self.balance = balance
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.amount)
