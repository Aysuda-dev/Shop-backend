from django.db import models
from django.utils.translation import gettext_lazy as _
from account_module.models import User


# Create your models here.

class ArticleCategory(models.Model):
    parent=models.ForeignKey('ArticleCategory',null=True,blank=True,on_delete=models.CASCADE,
                             verbose_name=_('دسته بندی والد'))
    title = models.CharField(max_length=300,verbose_name=_('عنوان دسته بندی '))
    url_title = models.CharField(max_length=300, unique=True,verbose_name= _('عنوان در url'))
    is_active = models.BooleanField(default=True, verbose_name=_(' فعال/غیرعال'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('دسته بندی مقاله')
        verbose_name_plural = _('دسته بندی های مقاله')


class Article(models.Model):

    title = models.CharField(max_length=300, verbose_name=_('عنوان مقاله '))
    slug=models.SlugField(max_length=400, db_index=True, allow_unicode=True,verbose_name=_('عنوان در url'))
    images= models.ImageField(upload_to='articles', verbose_name=_('تصویر مقاله'))
    short_description=models.TextField(verbose_name=_('توضیحات کوتاه'))
    text=models.TextField(verbose_name=_('متن مقاله'))
    category=models.ManyToManyField('ArticleCategory', verbose_name=_('دسته بندی ها'))
    is_active = models.BooleanField(default=True, verbose_name=_(' فعال/غیرعال'))
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('نویسنده'), null=True,editable=False)
    create_date= models.DateTimeField(auto_now_add=True,editable=False, verbose_name=_('تاریخ ثبت'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _(' مقاله')
        verbose_name_plural = _(' مقالات')


class ArticleComment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name=_('مقاله'))
    parent = models.ForeignKey('ArticleComment', null=True, blank=True, on_delete=models.CASCADE, verbose_name=_('والد'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('کاربر'))
    creat_date = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ ثبت'))
    text = models.TextField(verbose_name=_('متن نظر'))

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = _('نظر مقاله')
        verbose_name_plural = _('نظرات مقاله')
