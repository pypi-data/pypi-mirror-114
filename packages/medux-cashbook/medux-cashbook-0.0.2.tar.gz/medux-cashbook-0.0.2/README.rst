Cashbook Plugin
======================================

This is a newly created plugin for MedUX.
Please add some documentation here. 

General
-------

MedUX modules are living in the ``medux.plugins`` setuptools entrypoint group.
They are normal Django apps, but found and loaded dynamically during startup.
As Django apps, they can have everything a "static" app also has:

Medux Cashbook PluginConfig
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The app configuration is declared in the module's ``apps.py``. Set the plugin's metadata there in the PluginMeta class.


Install
^^^^^^^

You can install this plugin locally by invoking `pip install -e .` in this folder, assuming you have activated your main project's virtualenv.

Models
^^^^^^

Create your models as usual in ``models.py``, they will be included. Don't forget to run ``makemigrations`` and ``migrate`` afterwords.


After each change regarding version number etc., run `python manage.py syncplugins`. This ensures your database is in sync with the plugins on disk.

License
^^^^^^^

This plugin is licensed under the `GNU Affero General Public License v3 or later (AGPLv3+)`_


_`GNU Affero General Public License v3 or later (AGPLv3+)`: https://www.gnu.org/licenses/agpl-3.0.txt
