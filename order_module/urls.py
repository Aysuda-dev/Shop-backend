from django.urls import path
from . import  views
urlpatterns = [
    path('add-to-order', views.addProductToOrder , name='add-to-order'),
    path('request-payment/', views.request_payment , name='request_payment'),
    path('payment-page/', views.payment_page , name= 'payment_page'),
    path('verify-payment/', views.verify_payment , name='verify_payment'),
]
