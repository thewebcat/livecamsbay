# coding=utf-8
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from news.models import News


def listnews(request):
    """
    Список новостей
    """
    context = {
        'listnews': News.objects.filter(state=News.STATE_PUBLISH)
    }
    return TemplateResponse(request, "news/news.html", context)


def news(request, slug):
    """
    Отображение новости
    """
    news_instance = get_object_or_404(News, slug=slug)
    context = {
        'news': news_instance,
    }
    return TemplateResponse(request, "news/news_view.html", context)
