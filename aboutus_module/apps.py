from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class AboutusModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aboutus_module'
    verbose_name = _('درباره ما')

