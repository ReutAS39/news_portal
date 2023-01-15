from django.urls import path
# Импортируем созданное нами представление
from .views import PostsList, PostDetail, PostCreate, PostUpdate, PostDelete #UserDetail, UserUpdate
from .views import upgrade_me

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostsList.as_view(), name='news_list'),
   path('<int:pk>', PostDetail.as_view(), name='news'),
   #path('create/', PostCreate.as_view(), name='post_create'),
   path('news/create/', PostCreate.as_view(), name='news_create'),
   #path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('news/<int:pk>/edit', PostUpdate.as_view(), name='news_edit'),
   #path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('news/<int:pk>/delete', PostDelete.as_view(), name='news_delete'),
   path('articles/create/', PostCreate.as_view(), name='articles_create'),
   path('articles/<int:pk>/edit', PostUpdate.as_view(), name='articles_edit'),
   path('articles/<int:pk>/delete', PostDelete.as_view(), name='articles_delete'),
   # path('user/<int:pk>', UserDetail.as_view(), name='testprofile'),
   # path('user/<int:pk>/edit', UserUpdate.as_view(), name='testprofile_edit'),
   path('upgrade/', upgrade_me, name='upgrade')
]
