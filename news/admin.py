from django.contrib import admin
from .models import Category, Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'article', 'text', 'time_in')

admin.site.register(Category)
admin.site.register(Post, PostAdmin)
# Register your models here.
