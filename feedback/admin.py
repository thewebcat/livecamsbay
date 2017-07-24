# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.db import models

from ckeditor.widgets import CKEditorWidget

from feedback.models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = 'question', 'name', 'phone', 'email'
    formfield_overrides = {models.TextField: {'widget': CKEditorWidget()}}
    fieldsets = (
        (None, {'fields': (('name', 'phone', 'email',),)}),
        (None, {'fields': ('question', 'comment')}),
    )


admin.site.register(Feedback, FeedbackAdmin)
