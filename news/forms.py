from django import forms
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

from django.utils.translation import gettext_lazy as _

from .models import Post


class PostForm(forms.ModelForm):
    article = forms.CharField(max_length=255, label='Заголовок:')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].empty_label = 'Выберите автора'
        #self.fields['position'].initial = 'NE'

    class Meta:
        model = Post
        fields = [
           'author',
           'category',
           #'position',
           'article',
           'text',
        ]
        widgets = {
           'article': forms.TextInput(attrs={'class': 'form-input'}),
           'text': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }

        labels = {
           'text': _('Текст'),
           'author': _('Автор:'),
           'category': _('Категория:'),
           'position': _('Статья/Новость:'),
        }

    def clean_text(self):
        text = self.cleaned_data["text"]
        if text is not None and len(text) < 20:
            raise ValidationError("Текст не может быть менее 20 символов.")

        return text


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
