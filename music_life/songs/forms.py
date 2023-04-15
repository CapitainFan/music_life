from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

from .models import *


class AddPostForm(forms.ModelForm):
    '''
    Форма для добавления поста
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].empty_label = "Исполнитель не выбран"
        self.fields['genre'].empty_label = "Жанр не выбран"
        self.fields['album'].empty_label = "Альбом не выбран"

    class Meta:
        model = Songs
        fields = ['title', 'slug', 'content', 'photo', 'author',
                  'genre', 'is_single','album', 'is_published',]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов')

        return title


class AddAuthorForm(forms.ModelForm):
    '''
    Форма для добавления исполнителя
    '''
    class Meta:
        model = Author
        fields = ['name', 'slug', 'content', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }


class AddAlbumForm(forms.ModelForm):
    '''
    Форма для добавления альбома
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].empty_label = "Исполнитель не выбран"

    class Meta:
        model = Album
        fields = ['name', 'slug', 'author', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
        }


class RegisterUserForm(UserCreationForm):
    '''
    Форма регистрации
    '''
    username = forms.CharField(
        label='Login',
        widget=forms.TextInput(attrs={'class': 'form-input'}),
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-input'}),
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
    )
    password2 = forms.CharField(
        label='Password again',
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    '''
    Форма авторизации
    '''
    username = forms.CharField(
        label='Login',
        widget=forms.TextInput(attrs={'class': 'form-input'}),
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
    )


class ContactForm(forms.Form):
    '''
    Контакт форма с капчей
    '''
    name = forms.CharField(
        label='Имя',
        max_length=225,
    )
    last_name = forms.CharField(
        label='Фамилия',
        max_length=225,
    )
    email = forms.EmailField(
        label='Почта',
    )
    content = forms.CharField(
        label='Текст',
        max_length=225,
        widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}),
    )
    captcha = CaptchaField()
