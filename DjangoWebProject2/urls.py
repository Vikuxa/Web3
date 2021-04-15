"""
Definition of urls for DjangoWebProject2.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin #для админ раздела
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.conf.urls import url
#from django.conf.urls import include #для админ раздела
admin.autodiscover() #для инициализации административного раздела

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings


urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('Links/', views.links, name='links'),
    
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Авторизация',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    url(r'^anketa$',views.anketa, name='anketa'),
    #url(r'^admin/', include(admin.site.urls)), # в задании написано, что это для входа в административный раздел, но это не работает, поскольку уже была добавлена строка для админ раздела выше
    url(r'^registration$', views.registration, name='registration'),
    url(r'^blog', views.blog, name='blog'),
    url(r'^(?P<parametr>\d+)/$', views.blogpost, name='blogpost'),
    url(r'^newpost$', views.newpost, name='newpost'),
    url(r'^videopost$', views.videopost, name='videopost')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#для загрузки файлов в папку media
urlpatterns += staticfiles_urlpatterns()