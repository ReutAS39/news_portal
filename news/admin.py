from django.contrib import admin
from .models import Category, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'position', 'article', 'text', 'time_in', 'author')
    list_filter = ('position', 'time_in', 'category__name')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('article', 'text')  # тут всё очень похоже на фильтры из запросов в базу


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
