from django.urls import path
from . import views

urlpatterns=[
    path('register', views.RegisterView.as_view(), name="register_page"),
    path('login', views.LoginView.as_view(), name="login_page"),
    path('logout', views.LogoutView.as_view(), name="logout_page"),
    path('forget-pass', views.ForgotPasswordView.as_view(), name="forget-password"),
    path('reset-pass/<active_code>', views.ResetPasswordView.as_view(), name="reset-password"),
    path('activate/<email_active_code>', views.ActivateAccountView.as_view(), name='activate_account'),

]