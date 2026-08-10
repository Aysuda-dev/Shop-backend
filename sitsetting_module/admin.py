from django.contrib import admin
from .models import Sitsetting ,Slider , Banners

# Register your models here.

class SitsettingAdmin(admin.ModelAdmin):
    list_display = ['Sit_name','is_active']
    list_editable= ['is_active']


class SliderAdmin(admin.ModelAdmin):
    list_display = ['title','is_active','url']
    list_editable= ['is_active', 'url']
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title','is_active']
    list_editable = ['is_active']
admin.site.register(Sitsetting,SitsettingAdmin)
admin.site.register(Slider,SliderAdmin)
admin.site.register(Banners,BannerAdmin)
