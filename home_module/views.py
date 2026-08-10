from django.db.models.aggregates import Count
from django.shortcuts import render
from django.views.generic.base import TemplateView
from unicodedata import category

from product_module.models import Products, Category
from sitsetting_module.models import Sitsetting ,Slider
from utils.convertors import group_list

# Create your views here.


class indx_page(TemplateView):
    template_name = 'home_module/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sliders:Slider = Slider.objects.filter(is_active=True)
        context['sliders'] = sliders
        latest_products= Products.objects.filter(is_active=True , is_deleted=False).order_by('-id')[:12]
        context['latest_products'] = group_list(latest_products)
        most_visit_product = Products.objects.filter(is_active=True , is_deleted=False).annotate(visit_count= Count('productvisit'))[:12]
        context['most_visit_product'] = group_list(most_visit_product)

        categories = list(Category.objects.filter(is_active=True ,is_deleted=False)[:6])
        categories_products = []
        for category in categories:
            item = {
                'id': category.id,
                'title': category.title,
                'products' : list(category.product_category.all()[:4])
            }
            categories_products.append(item)
        context['categories_products'] = categories_products

        from django.db.models import Sum
        most_bought_products = Products.objects.filter(variants__orderdetail__order__is_paid=True).annotate(order_count=Sum(
            'variants__orderdetail__count'
        )).order_by('-order_count')[:12]

        context['most_bought_products'] = group_list(most_bought_products)
        return context



def site_header_component(request):
    return render(request,'shared/site_header_component.html')

def site_footer_component(request):

    return render(request,'shared/site_footer_component.html')