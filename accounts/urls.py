# -*- coding: UTF-8 -*-
from django.conf.urls import url

from accounts import views


urlpatterns = [

    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
    url(r'^profile/edit/$', views.profile_edit, name='profile_edit'),
    url(r'^profile/change_password/$', views.profile_change_password, name='profile_change_password'),
    url(r'^profile/change_password_success/$', views.profile_change_password_success, name='profile_change_password_success'),

    url(r'^favorite/list/$', views.favorite_list, name='favorite_list'),
    url(r'^favorite/add/$', views.favorite_add, name='favorite_add'),
    url(r'^favorite/(?P<object_id>[0-9]+)/edit/$', views.favorite_edit, name='favorite_edit'),
    # url(r'^orders/$', views.orders, name='order_list'),
    # url(r'^orders/(?P<t>.*)/(?P<f>.*)/$', views.orders, name='orders_type_filter'),
    # url(r'^orders/(?P<t>.*)/$', views.orders, name='orders_type'),
    # url(r'^order/add/$', views.order_add, name='order_add'),
    # url(r'^order/add/success/$', views.order_add_success, name='order_add_success'),
    # url(r'^order/(?P<object_id>[0-9]+)/edit/$', views.order_edit, name='order_edit'),
    # url(r'^order/(?P<object_id>[0-9]+)/recall/$', views.order_recall, name='order_recall'),
    # url(r'^order/(?P<object_id>[0-9]+)/$', views.order_view, name='order_view'),
    #
    # url(r'^note/list/$', views.note_list, name='note_list'),
    # url(r'^note/add/$', views.note_add, name='note_add'),
    # url(r'^note/(?P<object_id>[0-9]+)/edit/$', views.note_edit, name='note_edit'),
    #
    url(r'^message/list/$', views.message_list, name='message_list'),
    url(r'^message/(?P<object_id>[0-9]+)/$', views.message_view, name='message_view'),
    #
    # url(r'^documents/$', views.documents, name='documents'),
    #
    #
    # # only companies
    # url(r'^bonuses/$', views.bonus_list, name='bonus_list'),
    #
    # url(r'^articles/$', views.articles, name='articles'),
    # url(r'^article/add/$', views.article_add, name='article_add'),
    # url(r'^article/(?P<object_id>[0-9]+)/edit/', views.article_edit, name='article_edit'),
    # url(r'^article/(?P<object_id>[0-9]+)/', views.article_view, name='article_view'),
    #
    url(r'^news/$', views.news, name='news'),
    url(r'^news/add/$', views.news_add, name='news_add'),
    url(r'^news/(?P<object_id>[0-9]+)/edit/', views.news_edit, name='news_edit'),
    url(r'^news/(?P<object_id>[0-9]+)/', views.news_view, name='news_view'),
    #
    # url(r'^calendar/$', views.calendar, name='calendar'),
    # url(r'^calendarevent/list/$', views.calendar_event_list, name='calendar_event_list'),
    # url(r'^event/add/$', views.calendar_event_add, name='calendar_event_add'),
    # url(r'^event/(?P<object_id>[0-9]+)/$', views.calendar_event, name='event_view'),
    # url(r'^event/(?P<object_id>[0-9]+)/edit/$', views.calendar_event_edit, name='event_edit'),
    #
    # # CATALOGS
    # url(r'^workcatalog/add/$', views.work_catalog_add, name='workcatalog_add'),
    # url(r'^workcatalog/(?P<object_id>[0-9]+)/edit/', views.work_catalog_edit, name='workcatalog_edit'),
    # url(r'^workcatalog/(?P<object_id>[0-9]+)/$', views.catalog_works_child_catalog, name='workcatalog_view'),
    # url(r'^workcatalog/$', views.catalog_works_root_catalog, name='workcatalog_redirect'),
    # url(r'^works/$', views.catalog_works_new, name='works'),
    # url(r'^work/add/$', views.work_add, name='work_add'),
    # url(r'^work/(?P<object_id>[0-9]+)/edit/', views.work_edit, name='work_edit'),
    # url(r'^work/(?P<object_id>[0-9]+)/', views.catalog_work_view, name='work_view'),
    #
    # url(r'^services/$', views.services, name='services'),
    # url(r'^service/add/$', views.service_add, name='service_add'),
    # url(r'^service/(?P<object_id>[0-9]+)/edit/', views.service_edit, name='service_edit'),
    # url(r'^service/(?P<object_id>[0-9]+)/', views.service_view, name='service_view'),
    #
    # url(r'^productcatalog/add/$', views.product_catalog_add, name='productcatalog_add'),
    # url(r'^productcatalog/(?P<object_id>[0-9]+)/edit/', views.product_catalog_edit, name='productcatalog_edit'),
    # url(r'^productcatalog/$', views.catalog_products_root_catalog, name='productcatalog_redirect'),
    # url(r'^productcatalog/(?P<object_id>[0-9]+)/$', views.catalog_products_child_catalog, name='productcatalog_view'),
    # url(r'^products/$', views.catalog_products_new, name='products'),
    # url(r'^product/add/$', views.product_add, name='product_add'),
    # url(r'^product/(?P<object_id>[0-9]+)/$', views.catalog_product_view, name='product_view'),
    # url(r'^product/(?P<object_id>[0-9]+)/edit/', views.product_edit, name='product_edit'),
    #
    # url(r'^materials/$', views.catalog_materials_new, name='materials'),
    # url(r'^materialcatalog/add/$', views.material_catalog_add, name='materialcatalog_add'),
    # url(r'^materialcatalog/(?P<object_id>[0-9]+)/edit/', views.material_catalog_edit,
    #     name='materialcatalog_edit'),
    # url(r'^materialcatalog/$', views.catalog_materials_root_catalog, name='materialcatalog_redirect'),
    # url(r'^materialcatalog/(?P<object_id>[0-9]+)/$', views.catalog_materials_child_catalog, name='materialcatalog_view'),
    # # url(r'^material/add/$', views.material_add, name='material_add'),
    # url(r'^material/natural/add/$', views.material_natural_add, name='material_natural_add'),
    # url(r'^material/artificial/add/$', views.material_artificial_add, name='material_artificial_add'),
    # url(r'^material/(?P<object_id>[0-9]+)/$', views.material_view, name='material_view'),
    # url(r'^material/(?P<object_id>[0-9]+)/edit/$', views.material_edit, name='material_edit'),
    #
    # url(r'^offers/$', views.offers, name='offers'),
    # url(r'^offer/add/$', views.offer_add, name='offer_add'),
    # url(r'^offer/(?P<object_id>[0-9]+)/$', views.offer_view, name='offer_view'),
    # url(r'^offer/(?P<object_id>[0-9]+)/edit/$', views.offer_edit, name='offer_edit'),
    #
    url(r'^delete/(?P<data>.*)/$', views.delete, name='delete'),
    #
    url(r'tickets/$', views.tickets, name='tickets'),
    url(r'notifications/$', views.notifications_setting, name='notifications'),
    # /(?P<ticket_id>[0-9]+)
]
