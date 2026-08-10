from django.urls import path
from . import views

urlpatterns = [
    path('', views.indx_page.as_view() , name='index_page'),
]
