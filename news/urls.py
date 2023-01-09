from django.urls import path
# Импортируем созданное нами представление
from .views import PostsList, PostDetail, PostCreate, PostUpdate, PostDelete


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostsList.as_view(), name='post_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]

# path('news/create/', PostCreate.as_view(), name='news_create'),
# path('news/<int:pk>/update', PostUpdate.as_view(), name='news_update'),
# path('news/<int:pk>/delete', PostDelete.as_view(), name='news_delete'),
# path('article/create/', PostCreate.as_view(), name='article_create'),
# path('article/<int:pk>/update', PostUpdate.as_view(), name='article_update'),
# path('article/<int:pk>/delete', PostDelete.as_view(), name='article_delete'),
#
# /news/create/
# /news/<int:pk>/edit/
# /news/<int:pk>/delete/
# /articles/create/
# /articles/<int:pk>/edit/
# /articles/<int:pk>/delete/