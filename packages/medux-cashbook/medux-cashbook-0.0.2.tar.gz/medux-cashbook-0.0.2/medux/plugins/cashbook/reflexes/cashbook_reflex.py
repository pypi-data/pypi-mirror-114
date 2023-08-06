from sockpuppet.reflex import Reflex
import logging

# from django.contrib import messages
from django.utils.timezone import now
from djmoney.money import Money

from medux.plugins.cashbook.models import AccountActivity

logger = logging.getLogger(__file__)


class Cashbook(Reflex):
    def add_amount(self):
        if self.request.user.has_perm("cashbook.add_accountactivity"):
            try:
                amount = Money(self.params["input-amount"], currency="EUR")
                activity = AccountActivity(timestamp=now(), amount=amount)
                activity.user = self.request.user
                if "input-comment" in self.params:
                    activity.comment = self.params["input-comment"]
                activity.save()
            except:
                # messages.warning(self.request, "You have to provide an amount.")
                pass

            self.amount = ""
            self.comment = ""
            self.object_list = AccountActivity.objects.all().order_by("-timestamp")
            # messages.success(self.request, "Saved amount.")

            # except ValueError as e:  # FIXME: catch errors and display in view

        else:
            # FIXME use Django messages system
            logger.warning("Non-authenticated user access blocked.")
