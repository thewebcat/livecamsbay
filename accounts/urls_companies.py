# -*- coding: UTF-8 -*-
from django.conf.urls import url

from accounts import views


urlpatterns = [
    url(r'^ajax/filter/$', views.companies_filter, name='companies_filter'),
    url(r'^ajax/filter/(?P<page>[0-9]+)/$', views.companies_filter, name='companies_filter_page'),


    url(r'^ajax/catalog_products/(?P<catalog_id>[0-9]+)/$', views.ajax_catalog_products, name='ajax_catalog_products'),
    url(r'^ajax/catalog_products/(?P<catalog_id>[0-9]+)/(?P<page>[0-9]+)/$', views.ajax_catalog_products,
        name='ajax_catalog_products_page'),
    url(r'^ajax/product/(?P<product_id>[0-9]+)/$', views.ajax_products, name='ajax_products'),

    url(r'^ajax/catalog_materias/$', views.ajax_catalog_materias, name='ajax_catalog_materias'),
    url(r'^ajax/catalog_materias/(?P<page>[0-9]+)/$', views.ajax_catalog_materias, name='ajax_catalog_materias_page'),
    url(r'^ajax/material/(?P<material_id>[0-9]+)/$', views.ajax_material, name='ajax_material'),

    url(r'^providers/$', views.companies_list, name='companies_providers'),
    url(r'^stoneworkers/$', views.companies_list, name='companies_stoneworkers'),
    url(r'^(?P<slug>.*)/$', views.profile_public, name='profile_view'),
]
