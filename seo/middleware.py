# -*- coding: utf-8 -*-

from seo.models import Rule


class RuleMiddleware(object):
    def process_request(self, request):
        request.rule = Rule.find(request)


