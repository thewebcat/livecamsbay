# -*- coding: utf-8 -*-

from django.contrib import admin

from seo.models import Rule

@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ('pattern', 'rtype', 'enabled')

    class Media:
        js = ('/static/admin/js/seo.rule.js',)