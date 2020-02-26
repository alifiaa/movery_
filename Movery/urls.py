"""Movery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.shortcuts import render
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^movie/', include('movie.urls')),
    url(r'^user/', include('user.urls')),
    url(r'^$', views.index, name='index'),
    #url(r'.*', lambda request: render(request, '404.html'), name='404'),
]

admin.site.site_title = 'Movie Discovery Site Admin'
admin.site.site_header = 'Welcome to Movie Discovery Site Admin'
admin.site.index_title = 'Dashboard'

#admin.site.site_header = 'Log In | Movie Discovery Site Admin'
#admin.site.site_title = 'Log In Movie Discovery Site Admin'
#admin.site.index_title = 'Welcome to Movie Discovery Site Admin'
