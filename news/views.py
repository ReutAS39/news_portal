from datetime import datetime
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.contrib import messages
from django.shortcuts import redirect, render, reverse, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст


from .models import Post, Category, Author
from .filters import PostFilter
from .forms import PostForm
# from .tasks import hello, printer, mass_sender


menu = [
        {'title': 'Добавить статью', 'url_name': 'articles_create'},
        {'title': 'Добавить новость', 'url_name': 'news_create'},
        ]


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
      #  Author.objects.create(user=User.objects.get(username=user)) # Добавление пользоаателя в Authors
    return redirect('/news')


def subscribe_me(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)
    category.subscribers.add(user)
#
#     message = "Вы подписались на рссылку новостей категории "
#     return render(request, 'subscribe.html', {'category': category, 'message': message})
    return redirect('/news')


class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-time_in'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news_list.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    # context_object_name = 'posts'
    context_object_name = 'news_list'
    paginate_by = 10  # вот так мы можем указать количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса, чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs
        # return Post.objects.filter(category=None)

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами, что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        context['news_count'] = f'Количество статей: {self.filterset.qs.count()}'
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_sale'] = None
        context['title'] = 'Главная страница'
        context['cat_selected'] = 0
        context['menu'] = menu
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context['auth'] = self.request.user.groups.filter(name='common').exists()
        return context


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — news.html
    template_name = 'news.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами, что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = f"{context['news'].article}"
        context['cat_subscriber'] = Category.objects.filter(subscribers__pk=self.request.user.id)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        context['cat_selected'] = context['news'].category.get()

        return context


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    # Указываем нашу разработанную форму
    form_class = PostForm
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Создание статьи'

        return context
# Добавляем представление для изменения товара.

    def form_valid(self, form):
        post = form.save(commit=False)
        path = self.request.path

        if path == '/news/articles/create/':
            post.position = 'PO'
        else:
            post.position = 'NE'

        # send_mail(
        #     subject=post.article,  # имя клиента и дата записи будут в теме для удобства
        #     message=post.text,  # сообщение с кратким описанием проблемы
        #     from_email='CamcoHKappacko@yandex.ru', # здесь указываете почту, с которой будете отправлять
        #     recipient_list=['chillyvilly@mailtest.html.ru']  # здесь список получателей.
        # )
        # получаем наш html
        # html_content = render_to_string(
        #     'mailtest.html',
        #     {
        #         'post': post,
        #     }
        # )
        #
        # # в конструкторе уже знакомые нам параметры, да? Называются правда немного по-другому, но суть та же.
        # msg = EmailMultiAlternatives(
        #     subject=f'{post.article}',
        #     body=post.text,  # это то же, что и message
        #     from_email='CamcoHKappacko@yandex.ru',
        #     to=['chillyvilly@mail.ru'],  # это то же, что и recipients_list
        # )
        # msg.attach_alternative(html_content, "text/html")  # добавляем html
        #
        # msg.send()  # отсылаем

#        mass_sender.delay(post.id)
        messages.success(self.request, 'Статья успешно добавлена.')
        return super().form_valid(form)

    permission_required = ('news.change_post',)


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    permission_required = ('news.add_post',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = f"Редактирование статьи {context['post'].article}"

        current_post = context['post']
        path = self.request.path
        if 'articles' in path:
            pos = 'PO'
        else:
            pos = 'NE'
        get_object_or_404(Post.objects.filter(position=pos), pk=current_post.pk)

        return context


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = f"Удаление статьи {context['post'].article}"

        current_post = context['post']
        path = self.request.path
        if 'articles' in path:
            pos = 'PO'
        else:
            pos = 'NE'
        get_object_or_404(Post.objects.filter(position=pos), pk=current_post.pk)

        return context


class CategoryList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    paginate_by = 5  # вот так мы можем указать количество записей на странице

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset.filter(category=self.kwargs['pk']))
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['title'] = 'Категория - ' + str(context['news_list'][0].category.get())
        context['menu'] = menu
        context['cat_selected'] = context['news_list'][0].category.get()
        context['news_count'] = f'Количество статей: {self.filterset.qs.count()}'
        context['cat_subscriber'] = Category.objects.filter(subscribers__pk=self.request.user.id)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context['auth'] = self.request.user.groups.filter(name='common').exists()
        return context
