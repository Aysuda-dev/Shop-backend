from django.db import models
from django.db.models import CASCADE
from django.urls import reverse
from django.utils.text import slugify

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
    title = models.CharField(max_length=300, verbose_name='برند')
    url_title = models.CharField(max_length=300, db_index=True, unique=True, null=False, verbose_name='عنوان در url')
    is_active = models.BooleanField(verbose_name='فعال/غیرفعال')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برندها'


class Category(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name='دسته بندی')
    url_title = models.CharField(max_length=300, db_index=True, unique=True, verbose_name='عنوان در url')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')
    is_deleted = models.BooleanField(default=False, verbose_name='حذف شده/نشده')

    def __str__(self):
        return f"{self.title} _ {self.url_title}"

    class Meta:
        verbose_name = 'دسته بندی محصول'
        verbose_name_plural = 'دسته بندی ها'


class Products(models.Model):
    title = models.CharField(max_length=300, verbose_name='نام محصول')
    code = models.CharField(max_length=10,null=True, blank=True, verbose_name='کد محصول')
    price = models.IntegerField(verbose_name='قیمت')
    category = models.ManyToManyField(Category, verbose_name='دسته بندی', related_name='product_category', )
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True, related_name='product_brand', verbose_name='برند')
    image = models.ImageField(upload_to='images/products', null=True, blank=True, verbose_name='تصویر')
    short_description = models.CharField(max_length=500, db_index=True, null=True, blank=True, verbose_name='توضیحات کوتاه')
    description = models.TextField(db_index=True, null=True, blank=True, verbose_name='توضیحات اصلی')
    slug = models.SlugField(db_index=True, null=True, blank=True, unique=True, max_length=200, verbose_name='اسلاگ')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')
    is_deleted = models.BooleanField(default=False, verbose_name='حذف شده/نشده')

    def get_absolute_url(self):
        return reverse('product-detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} ({self.price})'

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'


class Size(models.Model):
    name = models.CharField(max_length=70, null=True, blank=True, verbose_name='سایز/حجم')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'سایز'
        verbose_name_plural = 'سایز ها'

class Color(models.Model):
    name= models.CharField(max_length=70, null=True, blank=True ,verbose_name='رنگ')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'رنگ'
        verbose_name_plural = ' رنگ ها'

class ProductVariant(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='variants', verbose_name="محصول")
    size= models.ForeignKey(Size, on_delete=models.CASCADE)
    color= models.ForeignKey(Color, on_delete=models.CASCADE)
    stock= models.PositiveIntegerField(default=0, verbose_name='موجودی')
    price = models.IntegerField(null=True, blank=True ,verbose_name='قیمت')
    image = models.ImageField(upload_to='images/product-variant', null=True, blank=True, verbose_name='تصویر')

    def __str__(self):
        return f'{self.size.name} -{self.color.name} '

    class Meta:
        unique_together=('product','size','color')
        verbose_name = 'نوع محصول'
        verbose_name_plural = 'انوع محصول'


class ProductGallery(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name="محصول")
    image = models.ImageField(upload_to='images/product-gallery', null=True, blank=True, verbose_name='تصویر')
    def __str__(self):
        return f'{self.product.title}'

    class Meta:
        verbose_name = ' گالری تصویر'
        verbose_name_plural = ' گالری تصاویر'

class ProductVisit(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='محصول')
    ip = models.CharField(max_length=30, verbose_name='آی پی کاربر')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='کاربر')

    def __str__(self):
        return f'{self.product.title} ({self.ip})'

    class Meta:
        verbose_name = 'بازدید محصول'
        verbose_name_plural = 'بازدیدهای محصول'


class ProductComment(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='نام محصول',related_name='comments' )
    user=models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    email = models.EmailField(max_length=300, verbose_name='ایمیل')
    message = models.TextField(verbose_name='متن نظر')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد نظر')
    is_approved = models.BooleanField(default=False, verbose_name='تایید توسط ادمین ')

    def __str__(self):
        return f'{self.product} - ({self.user.username})'

    class Meta:
        verbose_name = 'نظرات محصول '
        verbose_name_plural = 'نظرات محصولات'
