from django.db import models

from account_module.models import User
from product_module.models import Products ,ProductVariant



# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    is_paid = models.BooleanField(default=False,verbose_name='نهایی شده/نشده')
    payment_date = models.DateField(null=True, blank=True, verbose_name='تاریخ پرداخت')

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
        verbose_name = 'سبد خرید'
        verbose_name_plural = ' سبدهای خرید'


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سبد خرید')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, verbose_name='محصول')
    final_price = models.IntegerField(null=True, blank=True, verbose_name='قیمت نهایی')
    count = models.IntegerField(verbose_name='تعداد')

    def get_total_price(self):
        return self.variant.get_price() * self.count

    def __str__(self):
        return str(self.order)

    class Meta:
        verbose_name = 'جزئیات سبد خرید'
        verbose_name_plural = 'لیست جزئیات سبدهای خرید'
