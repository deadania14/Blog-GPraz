from django.conf.urls import url
from blog import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^blog/(?P<year>[0-9]{4})/(?P<slug>[\w\-]+)/', views.blog, name='article'),
    url(r'^archive/(?P<year>[0-9]{4})/', views.archive, name='archive'),
    url(r'^tag/(?P<tag_name>[\w]+)/', views.tag, name='tag'),
]
