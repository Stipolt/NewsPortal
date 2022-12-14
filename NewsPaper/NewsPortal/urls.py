from django.urls import path
from .views import (NewsList, NewsDetail, NewsSearch, NewsCreate, NewsUpdate, NewsDelete, ArticleCreate,
                    ArticleDelete, ArticleUpdate, upgrade_me, CategoryView, subscribe_cat)
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('',  cache_page(60)(NewsList.as_view()), name='news'),
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('search/', NewsSearch.as_view()),
    path('categories/', CategoryView.as_view(), name='categories'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('article/create/', ArticleCreate.as_view(), name='article_create'),
    path('article/<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('categories/<int:category_id>/subscribe/', subscribe_cat, name='subscribes'),
    # path('categories/<int:pk>/unsubscribes/', unsubscribe_category, name='unsubscribes')
]