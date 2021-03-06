# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from django_filters.views import FilterView
from main.views import Catalogue, CamServicesView, add_to_favourites
from main.views import ModelPage

from main.models import Model

urlpatterns = [
    url(r'^$', Catalogue.as_view(), name='index'),
    url(r'^catalogue/$', Catalogue.as_view(), name='catalogue'),
    url(r'^catalogue/(?P<cam_service>[-\w]+)/(?P<sex>[-\w]+)/$', Catalogue.as_view(), name='catalogue-filter'),
    url(r'^models/(?P<slug>[-\w]+)/$', ModelPage.as_view(), name='model-page'),

    url(r'^cam-services/$', CamServicesView.as_view(), name='cam-services'),
    url(r'^favourites/(?P<action>[-\w]+)/$', add_to_favourites, name='add-to-favorites'),

    # url(r'^tst/$', views.tst, name='tst'),
    # url(r'^price/$', views.price, name='price'),
    # url(r'^kontakty/$', views.kontakty, name='kontakty'),
    # url(r'^reviews/$', views.reviews, name='reviews'),
    # url(r'^works/$', views.works, name='works'),
    # url(r'^aktsii/$', views.aktsii, name='aktsii'),
    # url(r'^aktsii/(?P<pk>[0-9]+)/$', views.aktsii, name='aktsii'),
    # url(r'^kontakty/$', views.kontakty, name='kontakty'),
    # url(r'^kontakty/(?P<page>.+)/$', views.kontakty, name='kontakty'),
    # url(r'^kalkulator/(?P<page>.+)/$', views.kalkulator, name='kalkulator'),
    # url(r'^produktsiya/$', views.produktsiya, name='produktsiya'),
    # url(r'^produktsiya/(?P<page>.+)/$', views.produktsiya, name='produktsiya'),
    # url(r'^informatsiya/(?P<page>.+)/$', views.informatsiya, name='informatsiya'),

    # url(r'^search/$', views.search, name='search'),

    # url(r'^send_msg/$', views.send_msg, name='send_msg'),

    # url(r'^napechatat-knigu/$', views.napechatat_knigu, name='napechatat_knigu'),
    # url(r'^napechatat-zhurnal/$', views.napechatat_zhurnal, name='napechatat_zhurnal'),

    # url(r'^katalog_calc/$', views.katalog_calc, name='katalog_calc'),
    # asterisk cdr load
    # url(r'^main/sms/$', smssend, name='smssend'),
]
