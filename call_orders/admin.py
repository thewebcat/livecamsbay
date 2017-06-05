# -*- coding: UTF-8 -*-
#from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from django.db import models
from call_orders.models import CallOrder


class CallOrderAdmin(admin.ModelAdmin):
    list_display = 'name', 'status', 'creation_date'
#    formfield_overrides = {models.TextField: {'widget': CKEditorWidget()}}


admin.site.register(CallOrder, CallOrderAdmin)
