from django.db import models
from django.utils.translation import gettext_lazy as _
from account_module.models import User
from product_module.models import Products ,ProductVariant



# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('کاربر'))
    is_paid = models.BooleanField(default=False,verbose_name=_('نهایی شده/نشده'))
    payment_date = models.DateField(null=True, blank=True, verbose_name=_('تاریخ پرداخت'))

    def calculate_total_price(self):
        total_amount = 0
        if self.is_paid:
            for order_detail in self.orderdetail_set.all():
                total_amount += order_detail.final_price * order_detail.count
        else:
            for order_detail in self.orderdetail_set.all():
                total_amount += order_detail.variant.get_price() * order_detail.count
        return total_amount


    def __str__(self):
        return str(self.user)



    class Meta:
        verbose_name = _('سبد خرید')
        verbose_name_plural = _(' سبدهای خرید')


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_('سبد خرید'))
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, verbose_name=_('محصول'))
    final_price = models.IntegerField(null=True, blank=True, verbose_name=_('قیمت نهایی'))
    count = models.IntegerField(verbose_name=_('تعداد'))

    def get_total_price(self):
        return self.variant.get_price() * self.count

    def __str__(self):
        return str(self.order)

    class Meta:
        verbose_name = _('جزئیات سبد خرید')
        verbose_name_plural = _('لیست جزئیات سبدهای خرید')
