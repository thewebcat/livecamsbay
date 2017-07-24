# coding=utf-8
from django.db.models import Q

from articles.models import Article
from common.decorators import render_to
from materials.models import Material
from products.models import Product


@render_to("tags/tags.html")
def tags(request):
    """
    поиск информации по тегам(давно не обновлялось)
    """
    get_filter = request.GET.get('filter', None)
    if get_filter:
        return {
            'materials': Material.objects.filter(Q(tags__title=get_filter)),
            'products': Product.objects.filter(Q(tags__title=get_filter)),
            'articles': Article.objects.filter(Q(tags__title=get_filter)),
        }
    return {}
