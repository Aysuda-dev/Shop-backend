from idlelib.rpc import request_queue

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse, Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView , ListView
from account_module.models import User
from order_module.models import Order, OrderDetail
from .forms import EditProfileForm, ChangePasswordForm
from django.utils.decorators import method_decorator

# Create your views here.
@method_decorator(login_required, name='dispatch')
class UserPanel(TemplateView):
    template_name = 'profile_module/user_panel.html'



@method_decorator(login_required, name='dispatch')
class EditProfile(View):
    def get(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileForm(instance=current_user)

        cotext = {
            'form': edit_form,
            'current_user': current_user,
        }
        return render(request, 'profile_module/edit_profile.html', cotext)

    def post(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileForm(request.POST, request.FILES, instance=current_user)
        if edit_form.is_valid():
            edit_form.save(commit=True)
        cotext = {
            'form': edit_form,
            'current_user': current_user,
        }
        return render(request, 'profile_module/user_panel.html', cotext)


@method_decorator(login_required, name='dispatch')
class ChangePassword(View):
    def get(self, request: HttpRequest):
        context = {
            'form': ChangePasswordForm()
        }
        return render(request, 'profile_module/change_password.html', context)

    def post(self, request: HttpRequest):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            current_user = User.objects.filter(id=request.user.id).first()
            if current_user.check_password(form.cleaned_data.get('current_user')):
                current_user.set_password(form.cleaned_data.get('password'))
                current_user.save()
                logout(request)
                return redirect(reverse('login_page'))
            else:
                form.add_error('password', 'کلمه عبور وارد شده اشتباه میباشد.')

        context = {
            'form': form
        }
        return render(request, 'profile_module/change_password.html', context)



@method_decorator(login_required, name='dispatch')
class MyShopping(ListView):
    model = Order
    template_name = 'profile_module/user_shopping.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        request: HttpRequest = self.request
        queryset = queryset.filter(user_id=request.user.id, is_paid=True)
        return queryset


@login_required
def user_panel_menu_component(request: HttpRequest):
    return render(request, 'profile_module/components/menu_component.html')


@login_required
def user_basket(request: HttpRequest):
    current_order = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,                                                                           user_id=request.user.id)[0]
    total_amount = current_order.calculate_total_price()

    context = {
        'order': current_order,
        'sum': total_amount
    }
    return render(request, 'profile_module/user_basket.html', context)


@login_required
def remove_order_detail(request):
    detail_id = request.GET.get('detail_id')
    if detail_id is None:
        return JsonResponse({
            'status': 'not_found_detail_id'
        })

    deleted_count, deleted_dict = OrderDetail.objects.filter(id=detail_id, order__is_paid=False, order__user_id=request.user.id).delete()

    if deleted_count == 0:
        return JsonResponse({
            'status': 'detail_not_found'
        })

    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False, user_id=request.user.id)
    total_amount = current_order.calculate_total_price()

    context = {
        'order': current_order,
        'sum': total_amount
    }
    return JsonResponse({
        'status': 'success',
        'body': render_to_string('profile_module/user_basket_content.html', context)
    })


@login_required
def change_order_detail_count(request: HttpRequest):
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')
    if detail_id is None or state is None:
        return JsonResponse({
            'status': 'not_found_detail_or_state'
        })

    order_detail = OrderDetail.objects.filter(id=detail_id, order__user_id=request.user.id, order__is_paid=False).first()

    if order_detail is None:
        return JsonResponse({
            'status': 'detail_not_found'
        })

    if state == 'increase':
        order_detail.count += 1
        order_detail.save()
    elif state == 'decrease':
        if order_detail.count == 1:
            order_detail.delete()
        else:
            order_detail.count -= 1
            order_detail.save()
    else:
        return JsonResponse({
            'status': 'state_invalid'
        })

    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False, user_id=request.user.id)
    total_amount = current_order.calculate_total_price()

    context = {
        'order': current_order,
        'sum': total_amount
    }
    return JsonResponse({
        'status': 'success',
        'body': render_to_string('profile_module/user_basket_content.html', context)
    })


@login_required
def my_shopping_detail(request: HttpRequest, order_id):
    order = Order.objects.prefetch_related('orderdetail_set').filter(id=order_id, user_id=request.user.id).first()
    order_detail = OrderDetail.objects.filter(id=order_id, order__user_id=request.user.id, order__is_paid=True).first()
    if order is None:
        raise Http404('سبد خرید مورد نظر یافت نشد')

    return render(request, 'profile_module/user_shopping_detail.html', {
        'order': order,
        'detail':order_detail
    })





