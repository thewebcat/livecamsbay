# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from main.models import Model
from update_api.views import BongaShowApi, BongaUpdateApi, ChaturShowApi, ChaturUpdateApi, JasminShowApi, \
    JasminUpdateApi, XcamsShowApi, XcamsUpdateApi

urlpatterns = [
    url(r'^bonga/show/$', BongaShowApi.as_view(), name='bonga-show-api'),
    url(r'^bonga/$', BongaUpdateApi.as_view(), name='bonga-update-api'),

    url(r'^chatur/show/$', ChaturShowApi.as_view(), name='chatur-show-api'),
    url(r'^chatur/$', ChaturUpdateApi.as_view(), name='chatur-update-api'),

    url(r'^jasmin/show/$', JasminShowApi.as_view(), name='jasmin-show-api'),
    url(r'^jasmin/$', JasminUpdateApi.as_view(), name='jasmin-update-api'),

    url(r'^xcams/show/$', XcamsShowApi.as_view(), name='xcams-show-api'),
    url(r'^xcams/$', XcamsUpdateApi.as_view(), name='xcams-update-api'),
]