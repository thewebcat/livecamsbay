# -*- coding: UTF-8 -*-
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar
from common.cms import CMSToolbarMix
from news.models import News


@toolbar_pool.register
class NewsToolbar(CMSToolbarMix, CMSToolbar):
    model = News
