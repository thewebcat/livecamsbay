# -*- coding: UTF-8 -*-

from django.conf.urls import url
from feedback import views


urlpatterns = [
    url(r'^$', views.feedback, name='feedback'),
]
