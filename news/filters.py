from django.forms import DateInput
from django_filters import FilterSet, DateFilter
from .models import Post

# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.


class PostFilter(FilterSet):
    # выводит виджет календаря при выборе даты за счёт атрибуты widget
    time_in = DateFilter(lookup_expr='gt', widget=DateInput(format='%d/%m/%Y', attrs={'type': 'date'}))

    class Meta:
        model = Post
        fields = {
           # поиск по названию
           'article': ['icontains'],
           # exact выбирает все объекты моделей, в которых свойство равно определенному значению.
           'author': ['exact'],
                  }

    def __init__(self, *args, **kwargs):
        super(PostFilter, self).__init__(*args, **kwargs)
        self.filters['article__icontains'].label = "Заголовок"  # не меняется
        self.filters['author'].label = "Автор"
        self.filters['time_in'].label = "Дата"
