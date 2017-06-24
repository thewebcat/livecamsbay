# coding=utf-8
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def set_meta(meta):
    """
    Тег для формирования мета-тегов на странице
    """
    html = []
    if hasattr(meta, 'title'):
        html.append('<title>%s</title>' % meta.title)
    if hasattr(meta, 'description'):
        html.append('<meta name="description" content="%s"/>' % meta.description)
    if hasattr(meta, 'keywords'):
        html.append('<meta name="keywords" content="%s"/>' % meta.keywords)
    if hasattr(meta, 'modified'):
        html.append('<meta http-equiv="Last-Modified" content="%s"/>' % meta.modified)
    return mark_safe('\n'.join(html))
