# -*- coding: UTF-8 -*-
from django.conf.urls import url

from news import views


urlpatterns = [
    url(r'^$', views.listnews, name='listnews'),
    url(r'^(?P<slug>[-\w]+)/$', views.news, name='news_view'),
]
