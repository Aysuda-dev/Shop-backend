from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class ArticleModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'article_module'
    verbose_name = _(' مقالات')
