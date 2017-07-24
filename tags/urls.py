# -*- coding: UTF-8 -*-

from django.conf.urls import url
from tags import views


urlpatterns = [
    url(r'^$', views.tags, name='tags'),
]
