# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib import admin

from ckeditor.widgets import CKEditorWidget

from main.admin import MixinSaveModel
from news.models import News


class NewsAdmin(MixinSaveModel, admin.ModelAdmin):
    list_display = 'title',
    list_display_links = 'title',
    save_on_top = True
    fieldsets = (
        (None, {
            'fields': (
                'state',
                'title',
                'publish_date',
                'short_text',
                'text',
                ('public', 'profile',),
                'tags',
                'image'
            )}),
    )
    filter_horizontal = ('tags',)
    # readonly_fields = ('profile',)
    formfield_overrides = {models.TextField: {'widget': CKEditorWidget()}}

    list_filter = ('state',)

    def get_queryset(self, request):
        return self.model.live


admin.site.register(News, NewsAdmin)
