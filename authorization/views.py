# coding=utf-8
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.db import transaction
from django.forms import model_to_dict
from django.http import Http404
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.generic import View, TemplateView, ListView, DetailView, FormView

from accounts.forms import AuthenticationForm, UserCreationForm, ProfileForm, ProfilePhoneForm, CompanyProfileForm, \
     MasterProfileForm
# from accounts.models import Profile, ProfileHash
# from common.forms import ChangePasswordForm, RecoverPasswordKeyForm, RecoverPasswordForm
# from common.tokens import user_is_active_token_generator
# from custom_auth.models import User


class Registration(TemplateView):
    """
    Страница выбора профиля для регистрации.
    Клиент, Модель, Компания
    """
    template_name = 'main/registration.html'


class RegistrationAccount(TemplateView):

    def get_template_names(self):

        if self.get_role == 'account':
            #form_profile = ProfileForm(self.request.POST or None)
            return ['accounts/registration/registration_account.html']
        elif self.get_role == 'model':
            #form_profile = MasterProfileForm(self.request.POST or None)
            return ['accounts/registration/registration_master.html']
        else:  # role == 'company':
            #form_profile = CompanyProfileForm(self.request.POST or None)
            return ['accounts/registration/registration_company.html']

    def get_context_data(self, **kwargs):
        if self.get_role == 'account':
            form_profile = ProfileForm(self.request.POST or None)
        elif self.get_role == 'model':
            form_profile = MasterProfileForm(self.request.POST or None)
        else:  # role == 'company':
            form_profile = CompanyProfileForm(self.request.POST or None)

        form = UserCreationForm(self.request.POST or None)
        form_profile_phone = ProfilePhoneForm(self.request.POST or None)
        context = super(RegistrationAccount, self).get_context_data(**kwargs)
        context['form'] = form
        context['form_profile'] = form_profile
        context['form_profile_phone'] = form_profile_phone
        return context


    @property
    def get_role(self):
        roles = ['account', 'model', 'company']
        role = self.kwargs.get('role')
        if role not in roles:
            return redirect('registration')
        return role

# @transaction.atomic
# def registration_account(request, role=None):
#     """
#     Регистрация пользователя.
#     """
#
#     roles = ['account', 'master', 'company']
#     # roles = ['account', 'company']
#     if role not in roles:
#         return redirect('registration')
#
#     if role == 'account':
#         form_profile = ProfileForm(request.POST or None)
#         template = 'accounts/registration/registration_account.html'
#     elif role == 'master':
#         form_profile = MasterProfileForm(request.POST or None)
#         template = 'accounts/registration/registration_master.html'
#     else:  # role == 'company':
#         form_profile = CompanyProfileForm(request.POST or None)
#         template = 'accounts/registration/registration_company.html'
#
#     form = UserCreationForm(request.POST or None)
#     form_profile_phone = ProfilePhoneForm(request.POST or None)
#
#     if request.method == 'POST':
#         if form.is_valid() and form_profile.is_valid() and form_profile_phone.is_valid():
#             user = form.save(commit=False)
#             profile = form_profile.save(commit=False)
#             profile.state = profile.STATE_PUBLISH
#             if role == 'account':
#                 profile.role = Profile.ROLE_USER
#             elif role == 'master':
#                 profile.role = Profile.ROLE_MASTER
#             elif role == 'company':
#                 profile.role = Profile.ROLE_COMPANY
#             profile.save()
#             ProfileHash(profile=profile).save()
#             profile_phone = form_profile_phone.save(commit=False)
#             profile_phone.profile = profile
#             profile_phone.save()
#             if profile.role == Profile.ROLE_COMPANY:
#                 from accounts.models import ProfileDirector, ProfileBankDetails
#                 ProfileDirector(profile=profile).save()
#                 ProfileBankDetails(profile=profile).save()
#             user.profile = profile
#             user.is_active = False
#             user.save()
#
#             from authorization.tasks import sent_email
#             sent_email.delay(user)
#
#             # user = authenticate(username=user.email, password=form.get_password())
#             #
#             # login(request, user)
#             return TemplateResponse(request, 'common/registration_done.html')
#
#     context = {
#         'form': form,
#         'form_profile': form_profile,
#         'form_profile_phone': form_profile_phone,
#     }
#     return TemplateResponse(request, template, context)
#
#
# @take_meta()
# def enter(request):
#     """
#     Авторизация
#     """
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#
#             if 'remember_me' in request.POST:
#                 request.session.set_expiry(0)
#
#             login(request, form.get_user())
#
#             if form.get_user().profile and form.get_user().profile.city:
#                 request.session['geo'] = model_to_dict(form.get_user().profile.city)
#
#             from amigostone.redis_connection import redis_conn
#
#             hash_str = form.get_user().profile.profilehash.hash_str
#             if redis_conn.get(hash_str) is None:
#                 redis_conn.setex(request.session.session_key, hash_str, settings.SESSION_COOKIE_AGE)
#
#             next_url = request.GET.get('next', reverse('accounts:profile'))
#             return redirect(next_url)
#         else:
#             # if form errors
#             context = {'form': form}
#             return TemplateResponse(request, "common/enter.html", context)
#     else:
#         form = AuthenticationForm()
#         context = {'form': form}
#
#     return TemplateResponse(request, "common/enter.html", context)
#
#
# def quick_enter(request):
#     """
#     Функция быстрой авторизации. Работает при settings.DEBUG = True
#     """
#     if not settings.DEBUG:
#         raise Http404
#     email = request.GET.get('email')
#
#     user = User.objects.get(email=email)
#
#     user = authenticate(user=user)
#
#     login(request, user)
#     if user.profile and user.profile.city:
#         request.session['geo'] = model_to_dict(user.profile.city)
#
#     if user.is_admin:
#         return redirect('cp:index')
#
#     from amigostone.redis_connection import redis_conn
#
#     hash_str = user.profile.profilehash.hash_str
#     if redis_conn.get(hash_str) is None:
#         redis_conn.setex(request.session.session_key, hash_str, settings.SESSION_COOKIE_AGE)
#
#     return redirect('accounts:profile')
#
#
# def escape(request):
#     logout(request)
#     return redirect('/')
#
#
# @take_meta()
# def forgot_password(request):
#     """
#     Форма с полем для ввода email для восстановления пароля
#     """
#     if request.method == 'POST':
#         if request.POST.get('action') == RecoverPasswordForm.action_text:
#             form = RecoverPasswordForm(request.POST)
#             if form.is_valid():
#                 email = request.POST.get('email')
#                 p = form.get_user()
#                 p.recover_pass_activate()
#                 context = {'email': email, 'form': RecoverPasswordKeyForm()}
#                 return TemplateResponse(request, "common/forgot_password.html", context)
#             else:
#                 return TemplateResponse(request, "common/forgot_password.html", {'form': form})
#
#     form = RecoverPasswordForm()
#     return TemplateResponse(request, "common/forgot_password.html", {'form': form})
#
#
# @take_meta()
# def forgot_password_enter_key(request):
#     """
#     Форма с полем для ввода key для восстановления пароля
#     """
#     context = {'email': True, 'form': RecoverPasswordKeyForm()}
#     return TemplateResponse(request, "common/forgot_password.html", context)
#
#
# @take_meta()
# def recover_password(request):
#     """
#     Форма смены пароля
#     """
#     try:
#         user = User.objects.get(recover_pass_key=request.GET.get('key'), recover_pass_active=True)
#     except User.DoesNotExist:
#         return TemplateResponse(request, "common/change_password.html", {})
#
#     if request.method == 'POST':
#         form = ChangePasswordForm(request.POST)
#         if form.is_valid():
#             user.set_password(form.get_password())
#             user.recover_pass_deactivate()
#             user.save()
#             context = {'success': 1}
#             return TemplateResponse(request, "common/change_password.html", context)
#         else:
#             context = {'form': form}
#             return TemplateResponse(request, "common/change_password.html", context)
#     else:
#         form = ChangePasswordForm()
#         context = {'form': form}
#         return TemplateResponse(request, "common/change_password.html", context)
#
#
# def one_time_access(request):
#     """
#     Авторизация по ссылке из письма, которое отправляется при создании быстрого заказа.
#     """
#     email = request.GET.get('email')
#     access_key = request.GET.get('access_key')
#     next_url = request.GET.get('next')
#     # http://127.0.0.1:8000/one_time/access/?email=l2health@list.ru&access_key=38ce2179246b6388edacb2ba8c7036e241b4c1da&next=/accounts/orders/moderation/
#
#     user = authenticate(email=email, access_key=access_key)
#
#     if not user:
#         return redirect("/")
#
#     login(request, user)
#
#     if next_url:
#         return redirect(next_url)
#     return redirect('accounts:profile')
#
#
# def redirect_to_root(request):
#     """
#     Редирект на главную страницу
#     """
#     return redirect('/')
#
#
# def activate(request, uidb64=None, token=None,
#              token_generator=user_is_active_token_generator,
#              template_name="common/link_for_login.html"
#              ):
#     """
#     Активация нового пользователя
#     """
#     assert uidb64 is not None and token is not None  # checked by URLconf
#
#     try:
#         # urlsafe_base64_decode() decodes to bytestring on Python 3
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and user.is_active:
#         validlink = True
#     elif user is not None and token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         authenticate(user=user)
#         login(request, user)
#
#         return redirect('accounts:profile')
#     else:
#         validlink = False
#
#     context = {
#         'validlink': validlink,
#     }
#
#     return TemplateResponse(request, template_name, context)
