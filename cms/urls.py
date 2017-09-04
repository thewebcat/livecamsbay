# -*- coding: UTF-8 -*-
from django.conf.urls import url

from cms import views


urlpatterns = [
    url(r'^(?P<slug>[-\w]+)/$', views.cms_page, name='cms_page'),
]