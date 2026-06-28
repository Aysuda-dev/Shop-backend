from django.utils import timezone
import uuid
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from product_module.models import  ProductVariant
from order_module.models import Order, OrderDetail


def addProductToOrder(request: HttpRequest):
    variant_id = int(request.GET.get('variant_id'))
    count = int(request.GET.get('count'))
    if count < 1:
        return JsonResponse({
            'status': 'invalid_count',
            'text': 'مقدار وارد شده معتبر نمی باشد',
            'confirm_button_text': 'مرسی از شما',
            'icon': 'warning'
        })

    if request.user.is_authenticated:
        variant = ProductVariant.objects.filter(id=variant_id).first()
        if variant:
            if count > variant.stock:
                return JsonResponse({
                    'status': 'out_of_stock',
                    'text': f'تعداد مورد نظر ({count}) موجود نیست. موجودی: {variant.stock}',
                    'confirm_button_text': 'باشه',
                    'icon': 'warning'
                })

            current_order: Order = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)[0]
            current_order_detail = current_order.orderdetail_set.filter(variant_id=variant_id).first()
            if current_order_detail:
                new_count = current_order_detail.count + int(count)
                if new_count > variant.stock:
                    return JsonResponse({
                        'status': 'out_of_stock',
                        'text': f'تعداد مورد نظر ({count}) موجود نیست. موجودی: {variant.stock}',
                        'confirm_button_text': 'باشه',
                        'icon': 'warning'
                    })
                current_order_detail.count = new_count
                current_order_detail.save()
            else:
                new_detail = OrderDetail(order_id=current_order.id, variant_id=variant_id, count=count)
                new_detail.save()

            return JsonResponse({
                'status': 'success',
                'text': 'محصول مورد نظر با موفقیت به سبد خرید شما اضافه شد',
                'confirm_button_text': 'باشه ممنونم',
                'icon': 'success'
            })

        else:
            return JsonResponse({
                'status': 'not_found',
                'text': 'محصول مورد نظر یافت نشد',
                'confirm_button_text': 'مرسییییی',
                'icon': 'error'
            })

    else:
        return JsonResponse({
            'status': 'not_auth',
            'text': 'برای افزودن محصول به سبد خرید ابتدا می بایست وارد سایت شوید',
            'confirm_button_text': 'ورود به سایت',
            'icon': 'error'
        })


@login_required
def request_payment(request: HttpRequest):
    current_order: Order = Order.objects.get_or_create(
        is_paid=False,
        user_id=request.user.id
    )[0]

    # بررسی موجودی
    for detail in current_order.orderdetail_set.all():
        if detail.count > detail.variant.stock:
            return JsonResponse({
                'status': 'out_of_stock',
                'text': f'موجودی {detail.variant} کافی نیست',
                'icon': 'error'
            })

    total_price = current_order.calculate_total_price()
    if total_price == 0:
        return redirect(reverse('user_basket_page'))

    # انتقال به صفحه پرداخت مصنوعی
    return redirect(reverse('payment_page'))

@login_required
def payment_page(request: HttpRequest):
    current_order = Order.objects.filter(
        user=request.user,
        is_paid=False
    ).first()

    if not current_order:
        return redirect('user_basket_page')

    context = {
        'order': current_order,
        'total_price': current_order.calculate_total_price()
    }
    return render(request, 'order_module/payment_page.html', context)



@login_required
def verify_payment(request: HttpRequest):
    status = request.GET.get('status')  # success / failed
    current_order = Order.objects.filter(
        user=request.user,
        is_paid=False
    ).first()

    if not current_order:
        return JsonResponse({'status': False})

    if status == 'success':
        # ثبت قیمت نهایی و کاهش موجودی
        for detail in current_order.orderdetail_set.all():
            detail.final_price = detail.variant.get_price()
            detail.save()

            variant = detail.variant
            variant.stock -= detail.count
            variant.save()

        current_order.is_paid = True
        current_order.payment_date = timezone.now()
        current_order.ref_id = str(uuid.uuid4())[:8]
        current_order.save()

        return JsonResponse({
            'status': True,
            'ref_id': current_order.ref_id
        })

    return JsonResponse({
        'status': False,
        'message': 'پرداخت ناموفق بود'
    })