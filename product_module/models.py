from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from unidecode import unidecode

from account_module.models import User


def generate_unique_slug(instance, value, slug_field_name="slug"):
    """
    Generate a unique slug for a model instance, supporting non-Latin characters.

    Parameters:
    - instance: The model instance.
    - value: The value to generate the slug from (e.g., name, title).
    - slug_field_name: The name of the slug field on the model (default is 'slug').

    Returns:
    - A unique slug as a string.
    """
    transliterated_value = unidecode(value)
    slug = slugify(transliterated_value)
    unique_slug = slug
    num = 1
    model_class = instance.__class__

    while model_class.objects.filter(**{slug_field_name: unique_slug}).exists():
        unique_slug = f"{slug}-{num}"
        num += 1

    return unique_slug


class Brand(models.Model):
    title = models.CharField(max_length=300, verbose_name=_('برند'))
    url_title = models.CharField(max_length=300, db_index=True, unique=True, null=False, verbose_name=_('عنوان در url'))
    is_active = models.BooleanField(default=True, verbose_name=_('فعال/غیرفعال'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('برند')
        verbose_name_plural = _('برندها')


class Category(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name=_('دسته بندی'))
    url_title = models.CharField(max_length=300, db_index=True, unique=True, verbose_name=_('عنوان در url'))
    is_active = models.BooleanField(default=True, verbose_name=_('فعال/غیرفعال'))
    is_deleted = models.BooleanField(default=False, verbose_name=_('حذف شده/نشده'))

    def __str__(self):
        return f"{self.title} _ {self.url_title}"

    class Meta:
        verbose_name = _('دسته بندی محصول')
        verbose_name_plural = _('دسته بندی ها')


class Products(models.Model):
    title = models.CharField(max_length=300, verbose_name=_('نام محصول'))
    price = models.IntegerField(verbose_name=_('قیمت'))
    category = models.ManyToManyField(Category, verbose_name=_('دسته بندی'), related_name='product_category', )
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True, related_name='product_brand', verbose_name=_('برند'))
    image = models.ImageField(upload_to='images/products', null=True, blank=True, verbose_name=_('تصویر'))
    short_description = models.CharField(max_length=500, db_index=True, null=True, blank=True, verbose_name=_('توضیحات کوتاه'))
    description = models.TextField(db_index=True, null=True, blank=True, verbose_name=_('توضیحات اصلی'))
    slug = models.SlugField(db_index=True, null=True, blank=True, unique=True, max_length=200, verbose_name=_('اسلاگ'))
    is_active = models.BooleanField(default=True, verbose_name=_('فعال/غیرفعال'))
    is_deleted = models.BooleanField(default=False, verbose_name=_('حذف شده/نشده'))

    def get_absolute_url(self):
        return reverse('product-detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} ({self.price})'

    class Meta:
        verbose_name = _('محصول')
        verbose_name_plural = _('محصولات')

class Size(models.Model):
    name = models.CharField(max_length=70, null=True, blank=True, verbose_name=_('سایز/حجم'))

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('سایز')
        verbose_name_plural = _('سایز ها')

class Color(models.Model):
    name= models.CharField(max_length=70, null=True, blank=True ,verbose_name=_('رنگ'))

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('رنگ')
        verbose_name_plural = _(' رنگ ها')

class ProductVariant(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name=_("محصول") ,related_name='variants')
    size= models.ForeignKey(Size, on_delete=models.CASCADE)
    color= models.ForeignKey(Color, on_delete=models.CASCADE)
    stock= models.PositiveIntegerField(default=0, verbose_name=_('موجودی'))
    price = models.IntegerField(null=True, blank=True ,verbose_name=_('قیمت'))
    image = models.ImageField(upload_to='images/product-variant', null=True, blank=True, verbose_name=_('تصویر'))

    def get_price(self) -> int:
        if self.price is not None:
            return self.price
        else:
            return self.product.price

        # return self.price if self.price is not None else self.product.price


    def __str__(self):
        return f'{self.size.name} -{self.color.name} '

    class Meta:
        unique_together = ('product', 'size', 'color')
        verbose_name = _('نوع محصول')
        verbose_name_plural = _('انواع محصول')


class ProductGallery(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name=_("محصول"))
    image = models.ImageField(upload_to='images/product-gallery', null=True, blank=True, verbose_name=_('تصویر'))
    def __str__(self):
        return f'{self.product.title}'

    class Meta:
        verbose_name = _('تصویر گالری')
        verbose_name_plural = _(' گالری تصاویر')

class ProductVisit(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name=_('محصول'))
    ip = models.CharField(max_length=30, verbose_name=_('آی پی کاربر'))
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name=_('کاربر'))

    def __str__(self):
        return f'{self.product.title} ({self.ip})'

    class Meta:
        verbose_name = _('بازدید محصول')
        verbose_name_plural = _('بازدیدهای محصول')

class ProductComment(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name=_('نام محصول'),related_name='comments' )
    user=models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('کاربر'))
    email = models.EmailField(max_length=300, verbose_name=_('ایمیل'))
    message = models.TextField(verbose_name=_('متن نظر'))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ ایجاد نظر'))
    is_approved = models.BooleanField(default=False, verbose_name=_('تایید توسط ادمین '))

    def __str__(self):
        return f'{self.product} - ({self.user.username})'

    class Meta:
        verbose_name = _('نظرات محصول ')
        verbose_name_plural = _('نظرات محصولات')
