from django.test.signals import setting_changed
from gdaps.conf import PluginSettings

# This is a default conf file for a GDAPS plugin.
# You can use settings anywhere in your plugin using this syntax:
#
#     from .conf import cashbook_settings
#     # or:
#     # from /home/christian/Projekte/medux/medux/plugins.cashbook.conf import cashbook_settings
#
#     foo = cashbook_settings.FOO_SETTING
#
# This way you can use custom (plugin-default) settings, that can be overridden globally if needed.


# required parameter.
NAMESPACE = "CASHBOOK"

# Optional defaults. Leave empty if not needed.
DEFAULTS = {
    # 'MY_SETTING': 'somevalue',
    # 'FOO_PATH': '/home/christian/Projekte/medux/medux/plugins.cashbook.models.FooModel',
    # 'BAR': [
    #     'baz',
    #     'buh',
    # ],
}

# Optional list of settings keys that are allowed to be in 'string import' notation. Leave empty if not needed.
IMPORT_STRINGS = (
    # 'FOO_PATH',
)

# Optional list of settings that have been removed. Leave empty if not needed.
REMOVED_SETTINGS = ()


cashbook_settings = PluginSettings(
    namespace=NAMESPACE, defaults=DEFAULTS, import_strings=IMPORT_STRINGS
)


def reload_cashbook_settings(*args, **kwargs):
    setting = kwargs["setting"]
    if setting == "CASHBOOK":
        cashbook_settings.reload()


setting_changed.connect(reload_cashbook_settings)
