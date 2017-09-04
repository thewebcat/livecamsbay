# -*- coding: UTF-8 -*-
from django.http import Http404
from django.shortcuts import render
from django.template.response import TemplateResponse
from .models import Page

def cms_page(request, slug):
    """
    Страница
    """
    try:
        page = Page.objects.get(slug=slug)
    except Page.DoesNotExist:
        raise Http404

    context = {
        'page': page
    }
    return TemplateResponse(request, "cms/page.html", context)