# -*- coding: UTF-8 -*-

from django.conf.urls import url
import views


urlpatterns = [
    url(r'^$', views.GwView.as_view(), name='gw'),
]
