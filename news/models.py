from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    # Модель, содержащая объекты всех авторов.
    user = models.OneToOneField(User, on_delete=models.CASCADE)  #cвязь «один к одному» с встроенной моделью пользователей User;
    rating = models.FloatField(default=0.0) # рейтинг пользователя. Ниже будет дано описание того, как этот рейтинг можно посчитать.

    def update_rating(self): # Метод модели Author, который обновляет рейтинг пользователя, переданный в аргумент этого метода.
        self.rating = 0
        for comment in Comment.objects.filter(user=self.user): # суммарный рейтинг всех комментариев автора;
            self.rating += comment.rating

        for post in Post.objects.filter(author=Author.objects.get(user=self.user)):
            self.rating += post.rating * 3 # суммарный рейтинг каждой статьи автора умножается на 3;
            for post_comment in Comment.objects.filter(post=post):
                self.rating += post_comment.rating # суммарный рейтинг всех комментариев к статьям автора.
        self.save()


class Category(models.Model):
    # Категории новостей/статей — темы, которые они отражают (спорт, политика, образование и т. д.).
    name = models.CharField(max_length=255, unique=True) #название категории. Поле должно быть уникальным
    subscribers = models.ManyToManyField(User)

    def __str__(self):
        return self.name.title()

POSITION = (
    ('PO', 'Post'),
    ('NE', 'News')
)

class Post(models.Model):
    # Эта модель должна содержать в себе статьи и новости, которые создают пользователи.
    # Каждый объект может иметь одну или несколько категорий.
    author = models.ForeignKey(Author, on_delete=models.CASCADE) # связь «один ко многим» с моделью Author;
    position = models.CharField(max_length=255, choices=POSITION) # поле с выбором — «статья» или «новость»;
    time_in = models.DateTimeField(auto_now_add=True) # автоматически добавляемая дата и время создания;
    category = models.ManyToManyField(Category, through='PostCategory') # связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
    article = models.CharField(max_length=255)  # заголовок статьи/новости;
    text = models.TextField() # текст статьи/новости;
    rating = models.FloatField(default=0.0) # рейтинг статьи/новости.

    def like(self):
        self.rating += 1
        self.save()

    def dis_like(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[0:124]}...'

    def __str__(self):
        return f'{self.article.title()}: {self.time_in} : {self.text}'

    def get_absolute_url(self):
        return reverse('news', args=[str(self.id)])

class PostCategory(models.Model):
    # Промежуточная модель для связи «многие ко многим»:
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # связь «один ко многим» с моделью Post;
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # связь «один ко многим» с моделью Category.

class Comment(models.Model):
    # Под каждой новостью/статьёй можно оставлять комментарии, поэтому необходимо организовать их способ хранения тоже.

    post = models.ForeignKey(Post,on_delete=models.CASCADE) # связь «один ко многим» с моделью Post;
    user = models.ForeignKey(User, on_delete=models.CASCADE) # связь «один ко многим» со встроенной моделью User
# (комментарии может оставить любой пользователь, необязательно автор);
    text = models.CharField(max_length=255)# текст комментария;
    time_in = models.DateTimeField(auto_now_add=True)# дата и время создания комментария;
    rating = models.FloatField(default=0.0)# рейтинг комментария.

    def like(self):
        self.rating += 1
        self.save()

    def dis_like(self):
        self.rating -= 1
        self.save()
