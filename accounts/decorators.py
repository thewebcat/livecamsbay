# -*- coding: UTF-8 -*-
from functools import wraps

from django.core.urlresolvers import reverse

from django.shortcuts import redirect
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import available_attrs
#
#             path = request.build_absolute_uri()
#             resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
#             # If the login url is the same scheme and net location then just
#             # use the path as the "next" url.
#             login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
#             current_scheme, current_netloc = urlparse(path)[:2]
#             if ((not login_scheme or login_scheme == current_scheme) and
#                     (not login_netloc or login_netloc == current_netloc)):
#                 path = request.get_full_path()
#             from django.contrib.auth.views import redirect_to_login
#             return redirect_to_login(
#                 path, resolved_login_url, redirect_field_name)
#


def profile_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Декоратор для блокирования доступа к личному кабинету кабинету пользователей у которых нет Profile
    Такими пользователями являются Администраторы и Модераторы
    """
    actual_decorator = user_passes_test(
        lambda u: u.profile,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def validate_access(function=None, access_profiles=None, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Декоратор дающий доступ для авторизированных пользователей с имеющимися правами
    """
    def decorator(view_func):

        @wraps(view_func, assigned=available_attrs(view_func))
        @login_required(login_url=login_url)
        @profile_required(login_url=login_url)
        def wrapper(request, *args, **kw):
            if not access_profiles or request.user.profile.role in access_profiles:
                return view_func(request, *args, **kw)
            else:
                return redirect(reverse('accounts:profile'))
        return wrapper
    return decorator
