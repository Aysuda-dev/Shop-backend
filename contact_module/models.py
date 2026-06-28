from django.db import models


class ContactUs(models.Model):
    title = models.CharField(max_length=300, verbose_name= 'موضوع نظر ' , )
    email = models.EmailField(max_length=300, verbose_name='ایمیل')
    full_name = models.CharField(max_length=300, verbose_name='نام و نام خانوادگی')
    message = models.TextField(verbose_name='متن نظر', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد نظر')
    is_read_by_admin = models.BooleanField(default=False, verbose_name='خوانده شده توسط ادمین ')

    def __str__(self):
        return f'{self.title} - ({self.full_name})'

    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'لیست تماس با ما'