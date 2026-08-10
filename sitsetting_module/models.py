from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Sitsetting(models.Model):
    Sit_name = models.CharField(max_length=100, verbose_name=_('اسم سایت'))
    slogan = models.CharField(max_length=100, verbose_name=_('شعار'), null=True, blank=True)
    logo = models.ImageField(upload_to='sit_images/', null=True, blank=True, verbose_name=_('لوگو'))
    phone_number = models.CharField(max_length=11, null=True, blank=True, verbose_name=_('شماره تلفن'))
    fax = models.CharField(max_length=11, null=True, blank=True, verbose_name=_('فکس'))
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name=_('ایمیل'))
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name=_('آدرس'))
    about_us = models.TextField(null=True, blank=True, verbose_name=_('درباره ما'))
    copyright = models.TextField(null=True, blank=True, verbose_name=_('حق کپی رایت '))
    instagram = models.URLField(null=True, blank=True, verbose_name=_('آیدی اینستاگرام'))
    telegram = models.URLField(null=True, blank=True, verbose_name=_('آیدی تلگرام'))
    is_active = models.BooleanField(default=True, verbose_name=_('فعال/غیرفعال'))

    def __str__(self):
        return self.Sit_name

    class Meta:
        verbose_name = _('تنظیمات سایت')
        verbose_name_plural = _('تنظیمات سایت')


class Slider(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('عنوان'))
    url = models.URLField(max_length=100, verbose_name=_('لینک'), null=True, blank= True )
    image = models.ImageField(upload_to='slider/', verbose_name=_('تصویر اسلایدر'))
    is_active = models.BooleanField(default=True, verbose_name=_('فعال/ غیرفعال بودن'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('اسلایدر ')
        verbose_name_plural = _('اسلایدرها')


# class FooterLinkBox(models.Model):
#     title = models.CharField(max_length=100)
#
#
#     def __str__(self):
#         return self.title
#
#     class Meta:
#         verbose_name='لینک فوتر'
#         verbose_name_plural='لینک های فوتر '
#
#
#
#
# class FooterLink(models.Model):
#     title = models.CharField(max_length=100)
#

class Banners(models.Model):
    title = models.CharField(max_length=300, verbose_name=_('عنوان بنر'))
    url= models.URLField(max_length=400, null=True, blank=True, verbose_name=_('آدرس بنر '))
    image = models.ImageField(upload_to='sitebanner/', verbose_name=_('تصویر بنر '))
    is_active = models.BooleanField(default=True, verbose_name=_('فعال/غیرفعال'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('بنر تبلیغاتی')
        verbose_name_plural = _('بنرهای تبلیغاتی')
