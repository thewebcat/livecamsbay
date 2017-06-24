# -*- coding: UTF-8 -*-

from django import template

register = template.Library()


@register.assignment_tag
def check_owner(obj, user):
    """
    Устаревшее
    """
    return obj.check_owner(user.profile)
