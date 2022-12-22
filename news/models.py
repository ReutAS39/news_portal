from django.db import models
from django.contrib.auth.models import User



class Author(models.Model):
# Модель, содержащая объекты всех авторов.
    user = models.OneToOneField(User, on_delete=models.CASCADE)# cвязь «один к одному» с встроенной моделью пользователей User;
    rating = models.FloatField(default=0.0)# рейтинг пользователя. Ниже будет дано описание того, как этот рейтинг можно посчитать.

    def update_rating(self):
        pass

class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)

POSITION = (
    ('PO', 'Post'),
    ('NE', 'News')

class Post(models.Model):
# Эта модель должна содержать в себе статьи и новости, которые создают пользователи. Каждый объект может иметь одну или несколько категорий.
    author = models.ForeignKey(Author, on_delete=models.CASCADE) # связь «один ко многим» с моделью Author;
    position = models.CharField(choices=POSITION)# поле с выбором — «статья» или «новость»;
    time_in = models.DateTimeField(auto_now_add=True)# автоматически добавляемая дата и время создания;
    category = models.ManyToManyField(Category, through='PostCategory') # связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
    article = models.CharField(max_length=255)# заголовок статьи/новости;
    text = models.TextField() # текст статьи/новости;
    rating = models.FloatField(default=0.0)# рейтинг статьи/новости.

    def like(self):
        pass

    def dis_like(self):
        pass

    def preview(self):
        pass

class PostCategory(models.Model):
    pass
# Промежуточная модель для связи «многие ко многим»:
    post = models.ForeignKey(Post, on_delete=models.CASCADE)# связь «один ко многим» с моделью Post;
    category = models.ForeignKey(Category, on_delete=models.CASCADE)# связь «один ко многим» с моделью Category.

class Comment(models.Model):
# Под каждой новостью/статьёй можно оставлять комментарии, поэтому необходимо организовать их способ хранения тоже.

    post = models.ForeignKey(Post,on_delete=models.CASCADE)# связь «один ко многим» с моделью Post;
    user = models.ForeignKey(User, on_delete=models.CASCADE)# связь «один ко многим» со встроенной моделью User (комментарии может оставить любой пользователь, необязательно автор);
    text = models.CharField(max_length=255)# текст комментария;
    time_in = models.DateTimeField(auto_now_add=True)# дата и время создания комментария;
    rating = models.FloatField(default=0.0)# рейтинг комментария.

    def like(self):
        pass

    def dis_like(self):
        pass