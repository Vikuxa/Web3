"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.db import models
from .models import Comment
from .models import Blog

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))

class AnketaForm (forms.Form):
    name = forms.CharField(label='Ваше имя ', min_length=2,max_length=50)
    vozrast = forms.ChoiceField(label='Ваш возраст ',
                             choices = (('1','меньше 14'), ('2','от 14 до 18'), ('3','от 18 до 30'), 
                                        ('4','от 30 до 50'), ('5','больше 50')), initial=3)
    gender = forms.ChoiceField(label='Ваш пол ',
                            choices = [('1','муж'), ('2','жен')],widget=forms.RadioSelect , initial=1)
    nalichie_sobaki = forms.ChoiceField(label='Есть ли у вас собака? ',
                            choices = [('1','да'), ('2','нет'),('3','хочу завести питомца')],widget=forms.RadioSelect , initial=1)
    poroda = forms.ChoiceField(label='Какой породы ваша собака или какую породу хотели бы завести? ',
                             choices = (('1','Аляскинский маламут'), ('2','Бигль'), ('3','Двор-терьер'), 
                                        ('4','Питбуль'), ('5','Амстаф'), ('6','Бульдог'), ('7','Датский/немецкий дог'),
                                        ('8','Афганская борзая'),('9','Пудель королевский'),('10','Пудель карликовый')), initial=1)
    rassilka = forms.BooleanField(label='Хотели бы вы получать рассылку на e-mail? ',required = False)
    email = forms.EmailField(label='Ваш e-mail? ', min_length=7)
    pogelania = forms.CharField(label='Пожелания для нашего сайта ', widget=forms.Textarea(attrs={'rows':10,'cols':20}))

class CommentForm (forms.ModelForm):
    class Meta:
        model = Comment # используемая модель
        fields = ('text',) # требуется заполнить только поле text
        labels = {'text': "Комментарий"} # метка к полю формы text


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title','description','content','image')
        labels = {'title':"Заголовок",'description':"Краткое содержание",'content':"Полное содержание",'image':"Картинка"}