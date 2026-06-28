
from django.http import Http404, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views import View
from account_module.forms import RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from .models import User
from django.contrib.auth import login , logout
from utils.send_email import send_email
from django.contrib import messages


# Create your views here.


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }
        return  render(request,'account_module/register_page.html',context)

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = register_form.cleaned_data['email']
            user_password = register_form.cleaned_data['password']
            user = User.objects.filter(email__iexact=user_email).exists()
            if user:
                register_form.add_error('email','کاربری با این ایمیل ثبت نام کرده است.لطفا ایمیل جدیدی وارد نمایید')
            else:
                new_user=User(
                    email= user_email,
                    email_active_code=get_random_string(72),
                    is_active= False,
                    username= user_email,
                )
                new_user.set_password(user_password)
                new_user.save()
                send_email('فعال سازی حساب کاربری',new_user.email,{'user':new_user},'emails/activate_account.html')
                messages.success(request, 'برای فعال سازی حساب، ایمیلی به آدرس شما ارسال شد.')
                return redirect(reverse('login_page'))

        context = {
            'register_form': register_form
        }
        return render(request,'account_module/register_page.html',context)


class ActivateAccountView(View):
    def get(self, request, email_active_code):
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user :
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.save()
                messages.success(request,'حساب شما فعال شد')
                return redirect(reverse('login_page'))
            else:
                messages.success(request,'حساب شما قبلا فعال شده بود')
                pass

        raise Http404


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }
        return render(request,'account_module/login_page.html',context)

    def post(self,request:HttpRequest):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data['email']
            user_password = login_form.cleaned_data['password']
            user:User = User.objects.filter(email__iexact=user_email).first()
            if user :
                if not user.is_active:
                    login_form.add_error('email','حساب کاربری شما فعال نشده است')

                else:
                    is_password_correct = user.check_password(user_password)
                    if is_password_correct:
                        login(request, user)
                        return redirect(reverse('index_page'))
            else:
                login_form.add_error('email','کاربری با مشخصات وارد شده یافت نشد')
        context= {
            'login_form': login_form
        }
        return render(request,'account_module/login_page.html',context)



class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('login_page'))


class ForgotPasswordView(View):
    def get(self, request):
        forgot_password_form = ForgotPasswordForm()
        context = {
            'forgot_pass': forgot_password_form
        }
        return render(request,'account_module/forget_password.html',context)

    def post(self,request):
        forgot_password_form = ForgotPasswordForm(request.POST)
        if forgot_password_form.is_valid():
            user_email = forgot_password_form.cleaned_data['email']
            user :User = User.objects.filter(email__iexact=user_email).first()
            if user:
                send_email('بازیابی کلمه عبور', user.email, {'user': user}, 'emails/forgot_password.html')
                return redirect(reverse('index_page'))
            return redirect(reverse('index_page'))

        context = {
            'forgot_pass': forgot_password_form
        }
        return render(request,'account_module/forget_password.html',context)


class ResetPasswordView(View):
    def get(self, request , active_code):
        user:User = User.objects.filter(email_active_code__iexact=active_code).first()
        if user is None:
            return redirect(reverse('register_page'))

        reset_password_form = ResetPasswordForm()

        context = {
            'reset_pass': reset_password_form,
            'user': user
        }
        return render(request,'account_module/reset_page.html',context)


    def post(self,request , active_code):
        reset_password_form = ResetPasswordForm(request.POST)
        user : User = User.objects.filter(email_active_code__iexact=active_code).first()
        if reset_password_form.is_valid():
            new_pass= reset_password_form.cleaned_data['password']
            if user:
                user.set_password(new_pass)
                user.email_active_code = get_random_string(72)
                user.is_active = True
                user.save()
                return redirect(reverse('login_page'))
            else:
                return redirect(reverse('register_page'))
        context = {
            'reset_pass': reset_password_form,
            'user': user
        }
        return render(request,'account_module/reset_page.html',context)


