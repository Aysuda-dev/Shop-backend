from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class ContactModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contact_module'
    verbose_name = _('ارتباط با ما')
