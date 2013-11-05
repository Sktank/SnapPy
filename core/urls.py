from django.conf.urls import patterns, url

from django.conf.urls.defaults import *

from django.contrib.auth import views as auth_views

from core import views

urlpatterns = patterns('',
    url(r'^$', views.base, name='base'),
)