# -*- coding: UTF-8 -*-
from functools import wraps
from django.http.response import HttpResponseBadRequest

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, Http404
import json
from decorator import decorator
from django.core import serializers
from django.db.models.query import QuerySet
# from influxdb import client as influxdb

# try:
#     INFLUXBD_LOGGING = settings.INFLUXBD_LOGGING
# except AttributeError:
#     INFLUXBD_LOGGING = False
#
#
# if INFLUXBD_LOGGING:
#     db = influxdb.InfluxDBClient(**settings.INFLUXBD)
#
#
# def influxdb_logger(name):
#
#     def renderer(function):
#
#         def logger(*args, **kw):
#             ts = time.time()
#             result = function(*args, **kw)
#             te = time.time()
#             json_body = [{
#                 "points": [[(te-ts)*1000]],
#                 "name": name,
#                 "columns": ["time diff"]
#             }]
#             if INFLUXBD_LOGGING:
#                 try:
#                     db.write_points(json_body)
#                 except:
#                     pass
#             return result
#
#         return logger
#
#     return renderer
#
#
# @influxdb_logger("func_render")
# def func_render(request, template, ret):
#     return render(request, template, ret)
from django.utils.decorators import available_attrs

# from common.models import ViewInstance
# from accounts.models import ViewInstance
from main.models import ViewInstance


def ajax_required(f):
    """
    AJAX request required decorator
    use it in your views:

    @ajax_required
    def my_view(request):
        ....

    """
    def wrap(request, *args, **kwargs):
            if not request.is_ajax():
                return HttpResponseBadRequest()
            return f(request, *args, **kwargs)
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


@decorator
def render_to_json(func, request, *args, **kw):
    """
    Декоратор, который возвращает json

    Usage:
    @render_to_json
    def my_view(request, param):
        if param == 'something':
            return {'data': 'some_data'}
        else:
            return {'data': 'some_other_data'}
    """
    output = func(request, *args, **kw)
    if isinstance(output, dict):
        return HttpResponse(json.dumps(output), content_type='application/json; charset=UTF-8')
    else:
        return output


@decorator
def render_to_json_or_tpl(func, request, *k, **kw):
    """
    Устаревшее
    """
    template = None
    ret = func(request, *k, **kw)

    # если ретурн тупо респонз то его и возвращаем
    if isinstance(ret, HttpResponse):
        return ret

    # если ретурн - tuple то разбиваем на объект и на шаблон
    if isinstance(ret, tuple):
        ret, template = ret

    if template:
        # TODD: вообще-то следующий кусок падает наверняка
        return func_render(request, template, ret)  # noqa

    # MSIE fix
    if 'MSIE' in request.META.get('HTTP_USER_AGENT'):
        content_type = 'text/plain; charset=UTF-8'
    else:
        content_type = 'application/json; charset=UTF-8'

    # если объект типа QuerySet
    if isinstance(ret, QuerySet):
        return HttpResponse(serializers.serialize('json', ret), content_type=content_type)

    # если объект типа dict
    return HttpResponse(json.dumps(ret), content_type=content_type)


def render_to(template):
    """
    Decorator for Django views that sends returned dict to render_to_response function
    with given template and RequestContext as context instance.

    If view doesn't return dict then decorator simply returns output.
    Additionally view can return two-tuple, which must contain dict as first
    element and string with template name as second. This string will
    override template name, given as parameter

    Parameters:

     - template: template name to use

    url snippet https://djangosnippets.org/snippets/821/

    Usage:
    @render_to('my/template.html')
    def my_view(request, param):
        if param == 'something':
            return {'data': 'some_data'}
        else:
            return {'data': 'some_other_data'}, 'another/template.html'
    """
    def renderer(func):
        @wraps(func)
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if isinstance(output, (list, tuple)):
                return render_to_response(output[1], output[0], RequestContext(request))
            elif isinstance(output, dict):
                return render_to_response(template, output, RequestContext(request))
            return output
        return wrapper
    return renderer


def has_edit(obj=None):
    """
    Проверка возможности редактирования материала пользователем
    """

    def wrapper(view_method):
        @wraps(view_method, assigned=available_attrs(view_method))
        def arguments_wrapper(request, *args, **kwargs):
            context = view_method(request, *args, **kwargs)

            if not obj or (obj in context and context[obj].profile != request.user.profile):
                raise Http404

            return context

        return arguments_wrapper

    return wrapper


def set_views(obj=None):
    """
    Счетчик посещений
    """
    def wrapper(view_method):
        @wraps(view_method, assigned=available_attrs(view_method))
        def arguments_wrapper(self, request, *args, **kwargs):
            context = view_method(self, request, *args, **kwargs)
            if hasattr(context, 'context_data'):
                # Увеличиваем инкремент (количество просмотров материала)
                context.context_data[obj].set_redis_key_incr()

                # используется при выводе количества новых/непросмотренных закзов
                new = ViewInstance.objects.get_or_create(content_object=context.context_data[obj])
                if hasattr(request.user, 'profile') and request.user.profile:
                    new.profiles.add(request.user.profile)

            return context

        return arguments_wrapper

    return wrapper
