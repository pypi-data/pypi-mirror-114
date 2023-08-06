import os

# from django.conf import settings
from django.utils.translation import gettext_lazy as _

from gdaps.api import PluginConfig, require_app
# from gdaps.frontend.conf import frontend_settings
from . import __version__


class MeduxPrescriptionsPluginMeta:
    """ This configuration is the introspection data for plugins."""

    # the plugin machine "name" is taken from the AppConfig, so no name here
    verbose_name = _("Prescriptions plugin")
    author = "Christian González"
    author_email = "christian.gonzalez@nerdocs.at"
    vendor = "Nerdocs"
    description = _("A plugin for prescribing medication.")
    category = _("Base")
    visible = True
    version = __version__
    # compatibility = "medux.core>=2.3.0"


class MeduxPrescriptionsConfig(PluginConfig):
    """A GDAPS Django app plugin.

    It needs a special parameter named ``PluginMeta``. It is the key for GDAPS
    to recognize this app as a GDAPS plugin.
    ``PluginMeta`` must point to a class that implements certain attributes
    and methods.
    """

    # Dotted Python path to the app
    # FIXME: plugin_namespace could be wrong here.
    name = "medux.plugins.medux_prescriptions"
    label = "medux_medux_prescriptions"

    # This is the most important attribute of a GDAPS plugin app.
    PluginMeta = MeduxPrescriptionsPluginMeta

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

        require_app(self, "medux")
