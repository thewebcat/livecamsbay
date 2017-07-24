# -*- coding: UTF-8 -*-

from django.conf.urls import url
from tickets import views


urlpatterns = [
    url(r'^$', views.add_new_ticket, name='add_new_ticket'),
]
