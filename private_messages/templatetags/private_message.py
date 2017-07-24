# -*- coding: UTF-8 -*-

from django import template
from django.db.models import Q

register = template.Library()


@register.filter
def is_read(message, user):
    return message.message_recipient.filter(Q(profile=user.profile))[0].viewed
