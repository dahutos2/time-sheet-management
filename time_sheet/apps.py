from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BlogConfig(AppConfig):
    name = "time_sheet"
    verbose_name = verbose_name_plural = _("システム")
