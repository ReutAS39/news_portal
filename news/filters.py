from django_filters import FilterSet
from .models import Post

# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
   class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       model = Post
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
       fields = {
           # поиск по названию
           'article': ['icontains'],
           # exact выбирает все объекты моделей, в которых свойство равно определенному значению.
           'author': ['exact'],
           'time_in': [
               'gt'  # дата должна быть больше или равна указанной
           ],
       }