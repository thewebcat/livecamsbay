# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.db import models

from ckeditor.widgets import CKEditorWidget

from .models import Page


class PageAdmin(admin.ModelAdmin):
    list_display = 'title', 'slug'
    #formfield_overrides = {models.TextField: {'widget': CKEditorWidget()}}


admin.site.register(Page, PageAdmin)
