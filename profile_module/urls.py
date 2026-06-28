from django.urls import path
from . import views


urlpatterns=[
    path('', views.UserPanel.as_view(), name="user_panel_page"),
    path('change-pass', views.ChangePassword.as_view(), name="change_pass_page"),
    path('edit-profile', views.EditProfile.as_view(), name="edit_profile_page"),
    path('user-basket', views.user_basket, name="user_basket_page"),
    path('my-shopping', views.MyShopping.as_view(), name='user_shopping_page'),
    path('my-shopping-detail/<order_id>', views.my_shopping_detail, name='user_shopping_detail_page'),
    path('remove-order-detail', views.remove_order_detail, name='remove_order_detail_ajax'),
    path('change-order-detail', views.change_order_detail_count, name='change_order_detail_count_ajax'),

]