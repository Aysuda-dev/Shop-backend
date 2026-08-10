from modeltranslation.translator import TranslationOptions, register
from .models import ArticleCategory ,Article


@register(ArticleCategory)
class ArticleCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)



@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ('title','short_description', 'text')