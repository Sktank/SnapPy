__author__ = 'spencertank'

from django.conf.urls import patterns, url

from django.conf.urls.defaults import *

from django.contrib.auth import views as auth_views

from front import views

user_re = '[\w\.-]+'

urlpatterns = patterns('',
    url(r'^$', views.front_index, name='index'),
    url(r'^about$', views.front_about, name='about'),
    url(r'^login$', views.front_login, name='login'),
    url(r'^register/$', views.front_register, name='register'),
)