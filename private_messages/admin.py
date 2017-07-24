# -*- coding: UTF-8 -*-

from django.contrib import admin
from private_messages.models import Message


class MessageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Message, MessageAdmin)
