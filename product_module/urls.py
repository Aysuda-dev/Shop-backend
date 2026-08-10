from django.urls import path
from . import views

from .views import get_colors_by_size, get_variant_detail, global_search

urlpatterns = [
    path('search/', global_search, name='global_search'),
    path('', views.ProductListView.as_view(), name='product-list'),
    path('cat/<cat>', views.ProductListView.as_view(), name='product-category-list'),
    path('brand/<brand>', views.ProductListView.as_view(), name='product-brand-list'),
    path('<slug:slug>', views.ProductDetailView.as_view(), name='product-detail'),
    path("colors/<int:product_id>/", get_colors_by_size, name="get_colors"),
    path("variant/<int:product_id>/", get_variant_detail, name="get_variant_detail"),

]
