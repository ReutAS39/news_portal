from random import choices

from django.forms import DateInput, TextInput
from django_filters import FilterSet, DateFilter, ChoiceFilter, CharFilter

from .models import Post, POSITION


# Создаем свой набор фильтров для модели Post.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.


class PostFilter(FilterSet):
    position = ChoiceFilter(choices=POSITION)
    # выводит виджет календаря при выборе даты за счёт атрибуты widget
    time_in = DateFilter(lookup_expr='gt', widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Post
        fields = {
           # поиск по названию
           'article': ['icontains'],
           # exact выбирает все объекты моделей, в которых свойство равно определенному значению.
           'author__user__username': ['icontains'],
        }



    def __init__(self, *args, **kwargs):
        super(PostFilter, self).__init__(*args, **kwargs)
        self.filters['position'].label = "Статья/новость"
        self.filters['article__icontains'].label = "Заголовок"
        self.filters['author__user__username__icontains'].label = "Автор"
        self.filters['time_in'].label = "За период с"

