from django.urls import path
from .views import PostsList, PostDetail, PostCreate, PostUpdate, PostDelete, CategoryList
from .views import upgrade_me, subscribe_me
from django.views.decorators.cache import cache_page

urlpatterns = [
   # path('', cache_page(60*1)(PostsList.as_view()), name='news_list'),
   path('', PostsList.as_view(), name='news_list'),
   path('<int:pk>', cache_page(60*5)(PostDetail.as_view()), name='news'),  # Раз в 5 минут будет записываться в кэш
   path('news/create/', PostCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit', PostUpdate.as_view(), name='news_edit'),
   path('news/<int:pk>/delete', PostDelete.as_view(), name='news_delete'),
   path('articles/create/', PostCreate.as_view(), name='articles_create'),
   path('articles/<int:pk>/edit', PostUpdate.as_view(), name='articles_edit'),
   path('articles/<int:pk>/delete', PostDelete.as_view(), name='articles_delete'),
   path('upgrade/', upgrade_me, name='upgrade'),
   path('subscribe/<int:pk>', subscribe_me, name='subscribe'),
   path('category/<int:pk>', CategoryList.as_view(), name='category'),
]
