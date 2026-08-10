from modeltranslation.translator import TranslationOptions, register
from .models import Sitsetting

@register(Sitsetting)
class SitsettingTranslationOptions(TranslationOptions):
    fields = ('Sit_name','slogan', 'address' ,'about_us')