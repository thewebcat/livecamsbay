# -*- coding: UTF-8 -*-

from django.conf.urls import url
from authorization import views


urlpatterns = [
    #url(r'^$', views.redirect_to_root, name='redirect_to_root'),

    url(r'^registration/(?P<role>.*)/', views.RegistrationAccount.as_view(), name="registration_account"),
    url(r'^registration/$', views.Registration.as_view(), name="registration"),
    # url(r'^login/', views.enter, name="enter"),
    # url(r'^quick_login/', views.quick_enter, name="quick_enter"),
    # url(r'^logout/', views.escape, name="escape"),
    # url(r'^activate/$', views.activate, name='activate'),
    # url(r'^password/forget/$', views.forgot_password, name='forgot_password'),
    # url(r'^password/forget/enter_key/$', views.forgot_password_enter_key, name='forgot_password_enter_key'),
    # url(r'^password/recover/$', views.recover_password, name='recover_password'),
    # url(r'^one_time/access/$', views.one_time_access, name='one_time_access'),
    # url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     views.activate, name='activate'),
]
