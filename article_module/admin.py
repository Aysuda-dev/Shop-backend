from django.contrib import admin
from .models import ArticleCategory , Article, ArticleComment
# Register your models here.


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['title','url_title' ,'parent','is_active']
    list_editable= ['is_active','parent','url_title']

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title','is_active','slug','author']
    list_editable= ['is_active']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        return super(ArticleAdmin, self).save_model(request, obj, form, change)

admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Article,ArticleAdmin)
admin.site.register(ArticleComment)

