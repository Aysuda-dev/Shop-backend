from django.db import models


# Create your models here.

class Sitsetting(models.Model):
    Sit_name = models.CharField(max_length=100, verbose_name='اسم سایت')
    slogan = models.CharField(max_length=100, verbose_name='شعار', null=True, blank=True)
    logo = models.ImageField(upload_to='sit_images/', null=True, blank=True, verbose_name='لوگو')
    phone_number = models.CharField(max_length=11, null=True, blank=True, verbose_name='شماره تلفن')
    fax = models.CharField(max_length=11, null=True, blank=True, verbose_name='فکس')
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name='ایمیل')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='آدرس')
    about_us = models.TextField(null=True, blank=True, verbose_name='درباره ما')
    copyright = models.TextField(null=True, blank=True, verbose_name='حق کپی رایت ')
    instagram = models.URLField(null=True, blank=True, verbose_name='آیدی اینستاگرام')
    telegram = models.URLField(null=True, blank=True, verbose_name='آیدی تلگرام')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')

    def __str__(self):
        return self.Sit_name

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات سایت'


class Slider(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    url = models.URLField(max_length=100, verbose_name='لینک', null=True, blank= True )
    image = models.ImageField(upload_to='slider/', verbose_name='تصویر اسلایدر')
    is_active = models.BooleanField(default=True, verbose_name='فعال/ غیرفعال بودن')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'اسلایدر '
        verbose_name_plural = 'اسلایدرها'


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
    title = models.CharField(max_length=300, verbose_name='عنوان بنر')
    url= models.URLField(max_length=400, null=True, blank=True, verbose_name='آدرس بنر ')
    image = models.ImageField(upload_to='sitebanner/', verbose_name='تصویر بنر ')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'بنر تبلیغاتی'
        verbose_name_plural = 'بنرهای تبلیغاتی'
