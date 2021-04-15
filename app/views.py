"""
Definition of views.
"""
from django.contrib.auth.forms import UserCreationForm # для регистрации
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from .forms import AnketaForm 
from django.db import models
from .models import Blog
from .models import Comment # использование модели комментариев
from .forms import CommentForm # использование формы ввода комментария
from .forms import BlogForm

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def links(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/Links.html',
        {
            'title':'links',
            'message':'My page.',
            'year':datetime.now().year,
        }
    )



def anketa(request):
    assert isinstance(request, HttpRequest)
    data = None
    vozrast = {'1':'меньше 14','2':'от 14 до 18','3':'от 18 до 30','4':'от 30 до 50','5':'больше 50'}
    gender = {'1':'муж', '2':'жен'}
    nalichie_sobaki = {'1':'да', '2':'нет','3':'хочу завести питомца'}
    poroda = {'1':'Аляскинский маламут', '2':'Бигль', '3':'Двор-терьер','4':'Питбуль', '5':'Амстаф', '6':'Бульдог', '7':'Датский/немецкий дог',
    '8':'Афганская борзая','9':'Пудель королевский','10':'Пудель карликовый'}
    if request.method =='POST':
        form = AnketaForm(request.POST)
        if form.is_valid():
            data=dict()
            data['name'] = form.cleaned_data['name']
            data['vozrast'] = vozrast[form.cleaned_data['vozrast']]
            data['gender'] = gender[form.cleaned_data['gender']]
            data['nalichie_sobaki'] = nalichie_sobaki[form.cleaned_data['nalichie_sobaki']]
            data['poroda'] = poroda[form.cleaned_data['poroda']]
            if (form.cleaned_data['rassilka']==True): 
                data['rassilka']='Да'
            else:
                data['rassilka']='Нет'
            data['email'] = form.cleaned_data['email']
            data['pogelania'] = form.cleaned_data['pogelania']
            form = None
    else:
        form = AnketaForm()
    return render(
        request,
        'app/pool.html',
        {
            'form':form,
            'data':data
        }
    )

def registration(request): # контроллер регистрации
    """Renders the registration page."""
    if request.method == "POST": # после отправки формы
        regform = UserCreationForm (request.POST)
        if regform.is_valid(): #валидация полей формы
            reg_f = regform.save(commit=False) # не сохраняем автоматически данные формы
            reg_f.is_staff = False # запрещен вход в административный раздел
            reg_f.is_active = True # активный пользователь
            reg_f.is_superuser = False # не является суперпользователем
            reg_f.date_joined = datetime.now() # дата регистрации
            reg_f.last_login = datetime.now() # дата последней авторизации
            reg_f.save() # сохраняем изменения после добавления данных
        return redirect('home') # переадресация на главную страницу после регистрации
    else:
         regform = UserCreationForm() # создание объекта формы для ввода данных нового пользователя

    assert isinstance(request, HttpRequest)
    return render(
            request,
            'app/registration.html',
            {
                'regform': regform, # передача формы в шаблон веб-страницы
                'year':datetime.now().year,
            }
        )

def blog(request):
    """Renders the about page."""
    posts = Blog.objects.all()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blog.html',
        {
            'title':'Блог',
            'posts':posts,
            'year':datetime.now().year,
        }
    )

def blogpost(request, parametr):
    """Renders the about page."""
    post_1 = Blog.objects.get(id=parametr)
    comments = Comment.objects.filter(post=parametr)

    if request.method == "POST": # после отправки данных формы на сервер методом POST
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя
            comment_f.date = datetime.now() # добавляем в модель Комментария (Comment) текущую дату
            comment_f.post = Blog.objects.get(id=parametr) # добавляем в модель Комментария (Comment) статью, для которой данный комментарий
            comment_f.save() # сохраняем изменения после добавления полей
            return redirect('blogpost', parametr=post_1.id) # переадресация на ту же страницу статьи после отправки комментария
    else:
        form = CommentForm() # создание формы для ввода комментария

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blogpost.html',
        {
            'post_1':post_1,
            'comments': comments, # передача всех комментариев к данной статье в шаблон веб-страницы
            'form': form, # передача формы добавления комментария в шаблон веб-страницы
            'year':datetime.now().year,
        }
    )

def newpost(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)

    if request.method == "POST": # после отправки данных формы на сервер методом POST
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.autor = request.user
            blog_f.save() # сохраняем изменения после добавления полей

            return redirect('blog') # переадресация на ту же страницу статьи после отправки комментария
    else:
        blogform = BlogForm() # создание формы для ввода комментария

   
    return render(
        request,
        'app/newpost.html',
        {
            'blogform':blogform,
            'title': 'Добавить статью блога', 
            'year':datetime.now().year,
        }
    )


def videopost(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title':'Видео',
            'message':'Страница с видео',
            'year':datetime.now().year,
        }
    )