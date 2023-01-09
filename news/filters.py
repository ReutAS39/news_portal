from django.forms import DateInput
from django_filters import FilterSet, DateFilter
from .models import Post

# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
# выводит виджет календаря при выборе даты за счёт атрибуты widget
    time_in = DateFilter( lookup_expr='gt', widget=DateInput(format=('%d-%m-%Y'),attrs={'type': 'date'}))

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
                  }