from http.client import HTTPResponse
from sitsetting_module.models import Banners
from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article , ArticleCategory , ArticleComment
from jalali_date import datetime2jalali, date2jalali
# Create your views here.


class ArticlesListView(ListView):
    model =Article
    paginate_by = 2
    ordering = ["-create_date"]
    template_name = 'article_module/article_page.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ArticlesListView, self).get_context_data(*args, **kwargs)
        context['banners'] = Banners.objects.filter(is_active=True)

        return context

    def get_queryset(self):
        queryset = super(ArticlesListView, self).get_queryset()
        queryset=queryset.filter(is_active=True)
        category_name = self.kwargs.get('category')
        if category_name:
            queryset = queryset.filter(category__url_title__iexact=category_name).order_by('-create_date')
        return queryset


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_module/article_detail.html'

    def get_queryset(self):
        query = super(ArticleDetailView, self).get_queryset()
        query = query.filter(is_active=True)
        return query

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data()
        article: Article = kwargs.get('object')
        context['comments'] = ArticleComment.objects.filter(article_id=article.id, parent=None).order_by('-creat_date').prefetch_related('articlecomment_set')
        context['comments_count'] = ArticleComment.objects.filter(article_id=article.id).count()
        return context


def article_categories_component(request: HttpRequest):
    article_main_categories = ArticleCategory.objects.prefetch_related('articlecategory_set').filter(is_active=True, parent_id=None)

    context = {
        'main_categories': article_main_categories
    }
    return render(request, 'article_module/component/article_categories_component.html', context)


def add_article_comment(request: HttpRequest):
    if request.user.is_authenticated:
        article_id = request.GET.get('article_id')
        article_comment = request.GET.get('article_comment')
        parent_id = request.GET.get('parent_id')
        print(article_id, article_comment, parent_id)
        new_comment = ArticleComment(article_id=article_id, text=article_comment, user_id=request.user.id, parent_id=parent_id)
        new_comment.save()
        context = {
            'comments': ArticleComment.objects.filter(article_id=article_id, parent=None).order_by('-creat_date').prefetch_related('articlecomment_set'),
            'comments_count': ArticleComment.objects.filter(article_id=article_id).count()
        }

        return render(request, 'article_module/includes/article_comments_partial.html', context)

    return HTTPResponse('response')



