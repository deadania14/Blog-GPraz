"""gpraz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from blog import views
import gpraz.secrets as secret

admin.site.site_header = 'GPraz Administration'
admin.site.site_title = 'GPraz Admin'

urlpatterns = [
    url(secret.ADMIN_URL, admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^blog/(?P<year>[0-9]{4})/(?P<slug>[\w\-]+)/', views.blog, name='article'), # todo
    url(r'^archive/(?P<year>[0-9]{4})/', views.archive, name='archive'),
    url(r'^tag/(?P<tag_name>[\w]+)/', views.tag, name='tag'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)