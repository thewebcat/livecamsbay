# -*- coding: UTF-8 -*-

from django import template
from django.template.loader import render_to_string
from django.utils.encoding import force_unicode
from django.template.defaultfilters import stringfilter
import re
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def get_range(value):
    """
      Filter - returns a list containing range made from given value
      Usage (in template):

      <ul>{% for i in 3|get_range %}
        <li>{{ i }}. Do something</li>
      {% endfor %}</ul>

      Results with the HTML:
      <ul>
        <li>0. Do something</li>
        <li>1. Do something</li>
        <li>2. Do something</li>
      </ul>

      Instead of 3 one may use the variable set in the views
    """
    return range(value)


@register.filter
def divide(value, arg):
    """
    Тег для отображения деления одного значения на другое
    использование {{ my_var1|divide:my_var2 }}
    """
    return int(value) / int(arg)


@register.filter
def show_me(v):
    """
    Отладочный тег для просмотра переменной в шаблоне
    использование {{ my_var|show_me }}
    результат выводится в консоль
    """
    print dir(v)  # do not delete this 'print'
    return v

@register.filter
def type_of(v):
    """
    Отладочный тег для просмотра типа переменной в шаблоне
    использование {{ my_var|type_of }}
    результат выводится в консоль
    """
    print type(v)  # do not delete this 'print'
    return type(v)

@register.filter
def int_to_str(v):
    """
    Конвертор типа int в str.
    использование {{ my_var|show_me }}
    """
    return str(v)

@register.filter
def mod(v, num):
    """
    Остаток от деления на
    использование {{ my_var|mod:num }}
    """
    return v % num

@register.filter
def key_value(dic, key):
    """
    Тег для получения значения из словаря по ключу
    использование {{ my_dict|key_value:my_key }}
    """
    try:
        return dic[str(key)]
    except KeyError:
        return None


@register.filter
def in_queryset(obj, instance):
    """
    Устаревшее
    Наличие экземпляра класса в queryset
    """
    if obj.filter(id=instance.id):
        return True
    return False


@register.filter
def in_queryset2(obj, instance):
    """
    Уставервшее
    """
    if obj.filter(company=instance):
        return True
    return False


@register.filter('intspace')
def intspace(value):
    """
    Converts an integer to a string containing spaces every three digits.
    For example, 3000 becomes '3 000' and 45000 becomes '45 000'.
    See django.contrib.humanize app
    """
    orig = force_unicode(value)
    new = re.sub("^(-?\d+)(\d{3})", '\g<1> \g<2>', orig)
    if orig == new:
        return new
    else:
        return intspace(new)


def paragraphs(value):
    """
    Turns paragraphs delineated with newline characters into
    paragraphs wrapped in <p> and </p> HTML tags.
    """
    paras = re.split(r'[\r\n]+', value)
    paras = ['<p>%s</p>' % p.strip() for p in paras]
    return '\n'.join(paras)


paragraphs = stringfilter(paragraphs)

register.filter(paragraphs)


@register.filter
def tag_relations(obj):
    """
    Тег для отображения материалов по похожим тегам
    использование {{ my_instance|tag_relations  }}
    """
    from products.models import Product
    from materials.models import Material
    from articles.models import Article
    from news.models import News

    tags = obj.tags.all()
    where = {'tags__in': tags, 'state': Article.STATE_PUBLISH}
    products = Product.objects.filter(**where)
    articles = Article.objects.filter(**where)
    materials = Material.objects.filter(**where)
    news_list = News.objects.filter(**where)
    if isinstance(obj, Product):
        products = products.exclude(id=obj.id)
    if isinstance(obj, Article):
        articles = articles.exclude(id=obj.id)
    if isinstance(obj, Material):
        materials = materials.exclude(id=obj.id)
    if isinstance(obj, News):
        news_list = news_list.exclude(id=obj.id)
    context = {
        # 'materials': materials.distinct()[:2],
        # 'products': products.distinct()[:2],
        'articles': articles.distinct()[:2],
        'news_list': news_list.distinct()[:2],
    }
    return render_to_string('common/elements/tag_relations.html', context)


@register.simple_tag
def check_forms(*args):
    """
    use {% check_forms form0 formset form1 %}
    :param args: forms
    :return:
    """
    error_template = '<div class="control-container">Поля выделенные <span style="color: #f7931e">цветом</span> ' \
                     'обязательны к заполнению</div>'
    for form in args:
        if form and form.errors:
            return mark_safe(error_template)
    return ''


@register.simple_tag
def check_empty(value, default):
    """
    Тег вернет value если оно не путое, иначе default
    use {% check_empty value default %}
    :param args: value, default
    :return: value or default
    """
    return value if value else default


@register.filter
def queryset_filter(queryset, profile):
    """
    Тег для выборки из queryset только данные которые принадлежат
    пользователю, либо созданы модератором
    """
    return queryset.filter(profile__in=[None, profile])


# @register.filter
# def or_default_thumb(image):
#     """
#     Фильтр возвращает Thumbnailer от картинки по умолчанию,
#     если image (поле ThumbnailerImageFieldFile или Thumbnailer) отсутсвует,
#
#     Использование: {% thumbnail image|or_default_thumb size crop %}
#     """
#
#     from easy_thumbnails.files import get_thumbnailer
#     from amigostone import settings
#
#     default_image = get_thumbnailer(open(settings.DEFAULT_IMAGE), relative_name='default.png')
#
#     return default_image if not image else image
