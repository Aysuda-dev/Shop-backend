from django.shortcuts import render, redirect
from django.http import JsonResponse
from sitsetting_module.models import Banners
from .models import Products, Category, Brand, ProductVisit, ProductGallery, ProductComment, ProductVariant
from .forms import ProductCommentForm
from django.views.generic import ListView, DetailView
from django.http import HttpRequest
from django.db.models import Count
from utils.http_servis import get_client_ip
from utils.convertors import group_list


# Create your views here.


class ProductListView(ListView):
    template_name = 'product_module/productList.html'
    model = Products
    context_object_name = 'products'
    ordering = ['-id']
    paginate_by = 9

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        query = Products.objects.all()
        product: Products = query.order_by('-price').first()
        db_max_price = product.price if product is not None else 0
        context['db_max_price'] = db_max_price
        context['start_price'] = self.request.GET.get('start_price') or 0
        context['end_price'] = self.request.GET.get('end_price') or db_max_price
        context['banners'] = Banners.objects.filter(is_active=True,
                                                    position__iexact=Banners.SiteBannerPosition.product_list)
        return context

    def get_queryset(self):
        query = super(ProductListView, self).get_queryset()
        category_name = self.kwargs.get('cat')
        brand_name = self.kwargs.get('brand')
        request: HttpRequest = self.request
        start_price = request.GET.get('start_price')
        end_price = request.GET.get('end_price')
        if start_price is not None:
            query = query.filter(price__gte=start_price)

        if end_price is not None:
            query = query.filter(price__lte=end_price)

        if category_name:
            query = query.filter(category__url_title__iexact=category_name)

        if brand_name:
            query = query.filter(brand__url_title__iexact=brand_name)
        return query


class ProductDetailView(DetailView):
    template_name = 'product_module/productDetail.html'
    model = Products
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['banners'] = Banners.objects.filter(is_active=True,
                                                    position__iexact=Banners.SiteBannerPosition.product_detail)
        product = self.object

        context['sizes'] = product.variants.values(
            "size_id", "size__name"
        ).distinct()


        context['form'] = ProductCommentForm()
        context['comments'] = ProductComment.objects.filter(product_id=product.id, is_approved=True).select_related(
            'user').order_by('-created_date')
        context['comment_count'] = ProductComment.objects.filter(product_id=product.id, is_approved=True).count()
        galleries = list(ProductGallery.objects.filter(product_id=product.id).all())
        galleries.insert(0, product)
        context['product_galleries'] = group_list(galleries, 3)
        context['related_product'] = group_list(
            list(Products.objects.filter(brand_id=product.brand_id).exclude(pk=product.id).all()[:12]), 3)
        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
        has_been_visited = ProductVisit.objects.filter(ip__iexact=user_ip, product_id__exact=product.id).exists()
        if not has_been_visited:
            new_visit = ProductVisit(ip=user_ip, user_id=user_id, product_id=product.id)
            new_visit.save()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ProductCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = self.object
            comment.user = self.request.user
            comment.email = self.request.user.email
            comment.save()
            return redirect('product-detail', slug=self.object.slug)
        context = self.get_context_data(form=form)
        return self.render_to_response(context)



def get_colors_by_size(request, product_id):
    size_id = request.GET.get("size_id")

    colors = ProductVariant.objects.filter(
        product_id=product_id,
        size_id=size_id
    ).values(
        "color_id", "color__name"
    ).distinct()

    return JsonResponse({"colors": list(colors)})


def get_variant_detail(request, product_id):
    size_id = request.GET.get("size_id")
    color_id = request.GET.get("color_id")

    variant = ProductVariant.objects.filter(
        product_id=product_id,
        size_id=size_id,
        color_id=color_id
    ).first()

    if not variant:
        return JsonResponse({"error": "not found"})

    return JsonResponse({
        "price": variant.price,
        "stock": variant.stock,
        "image": variant.image.url,
    })



def product_category_component(request: HttpRequest):
    product_category = Category.objects.filter(is_active=True, is_deleted=False)
    context = {
        'categories': product_category
    }
    return render(request, 'product_module/components/product_category_component.html', context)


def product_brand_component(request: HttpRequest):
    product_brand = Brand.objects.annotate(product_count=Count('product_brand')).filter(is_active=True)
    context = {
        'brands': product_brand
    }
    return render(request, 'product_module/components/product_brand_component.html', context)

