from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.


class User(AbstractUser):
    avatar= models.ImageField(upload_to="images/profile", null=True, blank=True,verbose_name=_('عکس پروفایل'))
    email_active_code=models.CharField(max_length=100,verbose_name=_('ایمیل'))
    about_user=models.TextField(null=True, blank=True,verbose_name=_('درباره شخص'))
    address=models.TextField(null=True, blank=True,verbose_name=_('آدرس'))

    class Meta:
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')

    def __str__(self):
        if self.first_name  and self.last_name :
            return self.get_full_name()

        return self.email