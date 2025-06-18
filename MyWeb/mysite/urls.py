"""
Django 项目的 URL 声明，就像你网站的“目录”
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from debug_toolbar.toolbar import debug_toolbar_urls
# --------------------解决生产环境下static文件无法加载
from django.contrib.staticfiles.views import serve
from django.urls import re_path

def return_static(request,path,insecure=True,**kwargs):
    return serve(request,path,insecure,**kwargs)
# ----------------------------

urlpatterns = [
    path('markdownx/', include('markdownx.urls')),
    path("MyBlog/",include("MyBlog.urls")),

    path("admin/", admin.site.urls),
    
    re_path(r"^static/(?P<path>.*)$",return_static,name='static')#生产环境
] + debug_toolbar_urls()

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)