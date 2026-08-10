from modeltranslation.translator import TranslationOptions, register
from .models import Products , Brand , Color , Size

@register(Products)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title','description','short_description')



@register(Brand)
class BrandTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Color)
class ColorTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Size)
class SizeTranslationOptions(TranslationOptions):
    fields = ('name',)