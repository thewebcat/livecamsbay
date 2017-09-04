"""livecamsbay URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render_to_response
from django.template import RequestContext

from newsletter_email.views import email_subscribe


def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


urlpatterns = [
                  url(r'^', include('main.urls')),
                  url(r'^admin_tools/', include('admin_tools.urls')),
                  url(r'^admin/', admin.site.urls),

                  url(r'^auth/', include('authorization.urls', namespace="authorization")),
                  url(r'^accounts/', include('accounts.urls', namespace="accounts")),

                  # subscribe
                  url(r'^subscribe', email_subscribe, name='email_subscribe'),
                  # feedback
                  url(r'^feedback/', include('feedback.urls', namespace="feedback")),
                  # news
                  url(r'^news/', include('news.urls', namespace="news")),

                  url(r'^zombaiogw/', include('zombaio.urls', namespace="zombaio")),

                  url(r'^update-api/', include('update_api.urls', namespace="update-api")),

                  url(r'^404/$', handler404, ),
                  url(r'^add_new_ticket/', include('tickets.urls', namespace='tickets')),
                  url(r'^', include('cms.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
