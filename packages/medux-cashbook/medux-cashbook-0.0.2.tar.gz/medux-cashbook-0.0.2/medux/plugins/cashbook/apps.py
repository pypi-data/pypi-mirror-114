import os

# from django.conf import settings
from django.utils.translation import gettext_lazy as _

from gdaps.api import PluginConfig

# from gdaps.frontend.conf import frontend_settings
from . import __version__


class CashbookPluginMeta:
    """This configuration is the introspection data for plugins."""

    # the plugin machine "name" is taken from the AppConfig, so no name here
    verbose_name = _("Cashbook")
    author = "Christian González"
    author_email = "christian.gonzalez@nerdocs.at"
    vendor = "nerdocs"
    description = _("A simple Cashbook plugin")
    category = _("Base")
    visible = True
    version = __version__
    # compatibility = "medux.core>=2.3.0"


class CashbookConfig(PluginConfig):
    """A GDAPS Django app plugin.

    It needs a special parameter named ``PluginMeta``. It is the key for GDAPS
    to recognize this app as a GDAPS plugin.
    ``PluginMeta`` must point to a class that implements certain attributes
    and methods.
    """

    # Dotted Python path to the application, e.g. '/home/christian/Projekte/medux/medux/plugins.fooplugin'
    # It has to start with '/home/christian/Projekte/medux/medux/plugins' to be recognized as plugin.
    name = "medux.plugins.cashbook"

    # This is the most important attribute of a GDAPS plugin app.
    PluginMeta = CashbookPluginMeta

    def ready(self):
        # This function is called after the app and all models are loaded.
        #
        # You can do some initialization here, but beware: it should rather
        # return fast, as it is called at each Django start, even on
        # management commands (makemigrations/migrate etc.).
        #
        # Avoid interacting with the database especially 'save' operations,
        # if you don't *really* have to."""

        try:
            from . import signals
        except ImportError:
            pass

        # if os.path.exists(os.path.join(settings.BASE_DIR, frontend_settings.FRONTEND_DIR)):
        #
        #     settings.WEBPACK_LOADER.update({
        #         'cashbook': {
        #             'BUNDLE_DIR_NAME': '',
        #             'STATS_FILE': os.path.join(
        #                 os.path.abspath(os.path.dirname(__file__)),
        #                 "frontend",
        #                 "webpack-stats.json"
        #             ),
        #             # 'POLL_INTERVAL': 0.1,
        #             # 'TIMEOUT': None,
        #             # 'IGNORE': [r'.+\.hot-update.js', r'.+\.map']
        #         }
        #     })
