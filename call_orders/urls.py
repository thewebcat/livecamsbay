# -*- coding: UTF-8 -*-

from django.conf.urls import url
from call_orders import views


urlpatterns = [
    url(r'^send/$', views.call_order_send, name='send'),
]
