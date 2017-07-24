# -*- coding: UTF-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class NewsApphook(CMSApp):
    name = _(u"Новости")
    urls = ["news.urls"]
    app_name = "news"


apphook_pool.register(NewsApphook)
