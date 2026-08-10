from django.db import models
from django.utils.translation import gettext_lazy as _


class ContactUs(models.Model):
    title = models.CharField(max_length=300, verbose_name= _('موضوع نظر ')  )
    email = models.EmailField(max_length=300, verbose_name=_('ایمیل'))
    full_name = models.CharField(max_length=300, verbose_name=_('نام و نام خانوادگی'))
    message = models.TextField(verbose_name=_('متن نظر'), null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ ایجاد نظر'))
    is_read_by_admin = models.BooleanField(default=False, verbose_name=_('خوانده شده توسط ادمین '))

    def __str__(self):
        return f'{self.title} - ({self.full_name})'

    class Meta:
        verbose_name = _('تماس با ما')
        verbose_name_plural = _('لیست تماس با ما')