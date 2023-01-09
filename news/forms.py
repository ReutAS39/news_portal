from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Post

class PostForm(forms.ModelForm):
   article = forms.CharField(max_length=255, label='Заголовок:')
   class Meta:
       model = Post
       fields = [
           'author',
           'position',
           'category',
           'article',
           'text',
       ]

       labels = {
           'text': _('Текст'),
           'author': _('Автор:'),
           'category': _('Категории:'),
           'position': _('Статья/новость')
       }

   def clean(self):
       cleaned_data = super().clean()
       text = cleaned_data.get("text")
       if text is not None and len(text) < 20:
           raise ValidationError({
               "text": "Текст не может быть менее 20 символов."
           })

       return cleaned_data