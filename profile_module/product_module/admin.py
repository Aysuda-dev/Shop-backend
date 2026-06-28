
from django.contrib import admin
from .models import Products, Category, Brand, ProductGallery, ProductVisit, ProductComment,Size,Color,ProductVariant


class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    can_delete = True


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'is_active']
    list_editable = ['price', 'is_active']
    inlines = [ProductGalleryInline,ProductVariantInline]


# :small_blue_diamond: بقیه مدل‌ها
admin.site.register(Products, ProductAdmin)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductVisit)
admin.site.register(ProductComment)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(ProductVariant)
