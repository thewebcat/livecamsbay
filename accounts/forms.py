# -*- coding: UTF-8 -*-

import warnings

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm
from django.shortcuts import get_object_or_404
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _
from accounts.models import Profile, ProfilePhone, ProfileEmail, ProfileUrl
from cities_light.models import City
from main.fields import SplitPhoneField
from main.fields import SplitPhoneWidget
# from common.mixin import MixinForm
# from common.models import Currency
# from common.uploadform import UploadAvatarFormBase
#
from main.models import User
# from geo.models import City
# from orders.models import Order, OfferToOrder
#
from nocaptcha_recaptcha.fields import NoReCaptchaField
from ckeditor.widgets import CKEditorWidget
#
# from products.models import ProductCatalog
# from works.models import WorkCatalog


class NoReCaptchaFieldRu(NoReCaptchaField):
    default_error_messages = {
        'captcha_invalid': _('Попробуйте еще раз.')
    }


class MixinCaptchaForm(object):
    captcha_label = u'Captcha'
    captcha = NoReCaptchaFieldRu(label=captcha_label)


class BaseProfileForm(forms.ModelForm):

    name_label = u'ФИО'
    city_label = u'Город'

    name = forms.RegexField(label=name_label, max_length=255, regex=r'^[\w\d\s_\'\"\.-]+$',
                            widget=forms.TextInput(attrs={'placeholder': name_label, 'required': True}))
    city = forms.ModelChoiceField(queryset=City.objects.none(), label=city_label, required=True, empty_label=city_label,
                                  widget=forms.Select({'required': True}))

    def __init__(self, *args, **kwargs):
        super(BaseProfileForm, self).__init__(*args, **kwargs)

        if self.data and self.data['city']:
            self.fields['city'].queryset = City.objects.filter(id=self.data['city'])
        else:
            self.fields['city'].queryset = City.objects.none()

    class Meta:
        model = Profile
        fields = ('name', 'city')


class ProfileForm(MixinCaptchaForm, BaseProfileForm):
    pass


class MasterProfileForm(MixinCaptchaForm, BaseProfileForm):
    pass


class CompanyProfileForm(MixinCaptchaForm, BaseProfileForm):
    """
    Форма регистрации компании
    """
    name_label = u'Название компании'
    provider_label = u'Поставщик'
    stoneworker_label = u'Камнеобработчик'
    name = forms.RegexField(label=name_label, max_length=255, regex=r'^[\w\d\s_\'\"\.-]+$',
                            widget=forms.TextInput(attrs={'placeholder': name_label}))
    provider = forms.BooleanField(label=provider_label, required=False)
    stoneworker = forms.BooleanField(label=stoneworker_label, required=False)

    class Meta:
        model = Profile
        fields = ('name', 'city', 'provider', 'stoneworker')

    def clean(self):
        super(CompanyProfileForm, self).clean()
        provider_value = self.cleaned_data.get('provider')
        stoneworker_value = self.cleaned_data.get('stoneworker')
        if not provider_value and not stoneworker_value:
            from django.core.exceptions import ValidationError
            raise ValidationError("Необходимо указать род деятельности (Поставщик, Камнеобработчик)")


class PasswordChangeForm(DjangoPasswordChangeForm):
    error_messages = {
        'password_mismatch': u"Пароли не совпадают",
        'password_incorrect': u"Неверно указан старый пароль. "
                              u"Попробуйте еще раз."
    }

    old_password_label = u'Старый пароль'
    new_password1_label = u'Новый пароль'
    new_password2_label = u'Повторите пароль'

    old_password = forms.CharField(label=old_password_label,
                                   widget=forms.PasswordInput(attrs={'placeholder': old_password_label}))
    new_password1 = forms.CharField(label=new_password1_label,
                                    widget=forms.PasswordInput(attrs={'placeholder': new_password1_label}))
    new_password2 = forms.CharField(label=new_password2_label,
                                    widget=forms.PasswordInput(attrs={'placeholder': new_password2_label}))

    field_order = ['old_password', 'new_password1', 'new_password2']


class ProfileAccountForm(forms.ModelForm):

    name_label = u'ФИО'
    city_label = u'Город'
    zip_label = u'Индекс'
    address_label = u'Фактический адрес'
    avatar_label = u'Аватар'
    description_label = u'Описание, деятельность'

    name = forms.RegexField(label=name_label, max_length=255, regex=r'^[\w\d\s_\'\"\.-]+$',
                            widget=forms.TextInput(attrs={'placeholder': name_label}))
    city = forms.ModelChoiceField(label=city_label, queryset=City.objects.none(), required=True, empty_label=city_label,
                                  widget=forms.Select(attrs={'placeholder': city_label}))
    zip = forms.CharField(label=zip_label, required=False,
                          widget=forms.TextInput(attrs={'placeholder': zip_label}))
    address = forms.CharField(label=address_label, required=False,
                              widget=forms.TextInput(attrs={'placeholder': address_label}))
    description = forms.CharField(label=description_label, required=False,
                                  widget=forms.Textarea(attrs={'placeholder': description_label}))

    def __init__(self, *args, **kwargs):
        super(ProfileAccountForm, self).__init__(*args, **kwargs)

        if self.data:
            self.fields['city'].queryset = City.objects.all()
        else:
            if self.instance.city:
                self.fields['city'].queryset = City.objects.filter(id=self.instance.city.id)
            else:
                self.fields['city'].queryset = City.objects.none()

    class Meta:
        model = Profile
        fields = ('name', 'city', 'zip', 'address', 'avatar', 'description')


class ProfileCompanyForm(forms.ModelForm):
    """
    Форма редактирования компании
    """
    name_label = u'Название компании'
    city_label = u'Город'
    zip_label = u'Индекс'
    address_label = u'Фактический адрес'
    legal_address_label = u'Юридический адрес'
    avatar_label = u'Логотип компании'
    short_description_label = u'Короткое описание'
    description_label = u'Описание, детельность'
    provider_label = u'Поставщик'
    stoneworker_label = u'Камнеобработчик'

    name = forms.RegexField(label=name_label, max_length=255, regex=r'^[\w\d\s_\'\"\.-]+$',
                            widget=forms.TextInput(attrs={'placeholder': name_label}))
    city = forms.ModelChoiceField(label=city_label, queryset=City.objects.all(), required=True, empty_label=city_label,
                                  widget=forms.Select(attrs={'placeholder': city_label}))
    zip = forms.CharField(label=zip_label, required=False,
                          widget=forms.TextInput(attrs={'placeholder': zip_label}))
    address = forms.CharField(label=address_label, required=False,
                              widget=forms.TextInput(attrs={'placeholder': address_label}))
    legal_address = forms.CharField(label=legal_address_label, required=False,
                                    widget=forms.TextInput(attrs={'placeholder': legal_address_label}))
    short_description = forms.CharField(label=short_description_label, required=False,
                                        widget=forms.TextInput(attrs={'placeholder': short_description_label}))
    description = forms.CharField(label=description_label, required=False,
                                  widget=CKEditorWidget(attrs={'placeholder': description_label}))
    provider = forms.BooleanField(label=provider_label, required=False)
    stoneworker = forms.BooleanField(label=stoneworker_label, required=False)

    class Meta:
        model = Profile
        fields = ('name', 'city', 'zip', 'address', 'legal_address', 'avatar', 'short_description', 'description',
                  'provider', 'stoneworker')

    def clean(self):
        super(ProfileCompanyForm, self).clean()
        provider_value = self.cleaned_data.get('provider')
        stoneworker_value = self.cleaned_data.get('stoneworker')
        if not provider_value and not stoneworker_value:
            from django.core.exceptions import ValidationError
            raise ValidationError("Необходимо указать род деятельности (Поставщик, Камнеобработчик)")


class ProfileMasterForm(forms.ModelForm):

    name_label = u'ФИО'
    city_label = u'Город'
    zip_label = u'Индекс'
    address_label = u'Фактический адрес'
    avatar_label = u'Аватар'
    short_description_label = u'Короткое описание'
    description_label = u'Описание, деятельность'

    name = forms.RegexField(label=name_label, max_length=255, regex=r'^[\w\d\s_\'\"\.-]+$',
                            widget=forms.TextInput(attrs={'placeholder': name_label}))
    city = forms.ModelChoiceField(label=city_label, queryset=City.objects.all(), required=True, empty_label=city_label,
                                  widget=forms.Select(attrs={'placeholder': city_label}))
    zip = forms.CharField(label=zip_label, required=False,
                          widget=forms.TextInput(attrs={'placeholder': zip_label}))
    address = forms.CharField(label=address_label, required=False,
                              widget=forms.TextInput(attrs={'placeholder': address_label}))
    short_description = forms.CharField(label=short_description_label, required=False,
                                        widget=forms.TextInput(attrs={'placeholder': short_description_label}))
    description = forms.CharField(label=description_label, required=False,
                                  widget=forms.Textarea(attrs={'placeholder': description_label}))

    class Meta:
        model = Profile
        fields = ('name', 'city', 'zip', 'address', 'avatar', 'short_description', 'description')


class ProfilePhoneForm(forms.ModelForm):

    phone_label = u'Номер телефона'

    phone = SplitPhoneField(label=phone_label, required=True,
                            widget=SplitPhoneWidget(attrs={'placeholder': phone_label, 'required': True}))

    class Meta:
        model = ProfilePhone
        fields = ('phone',)


class ProfileEmailForm(forms.ModelForm):

    email_label = u'E-mail'

    email = forms.CharField(label=email_label, required=False,
                            widget=forms.TextInput(attrs={'placeholder': email_label}))

    class Meta:
        model = ProfileEmail
        fields = ('email',)


class ProfileUrlForm(forms.ModelForm):

    url_label = u'Адрес сайта'

    url = forms.CharField(label=url_label, required=False,
                          widget=forms.TextInput(attrs={'placeholder': url_label}))

    class Meta:
        model = ProfileUrl
        fields = ('url',)


# class OrderAddOrEditForm(forms.ModelForm):
#
#     name_label = u'ФИО'
#     email_label = u'E-mail'
#     phone_label = u'Номер телефона'
#     title_label = u'Название заказа'
#     description_label = u'Описание заказа'
#     city_label = u'Город'
#     product_catalog_label = u'Каталог изделия'
#
#     name = forms.CharField(label=name_label,
#                            widget=forms.TextInput(attrs={'placeholder': name_label, 'required': True}))
#     email = forms.EmailField(label=email_label,
#                              widget=forms.EmailInput(attrs={'placeholder': email_label, 'required': True}))
#     # phone = forms.CharField(label=phone_label,
#     #                         widget=forms.TextInput(attrs={'placeholder': phone_label, 'required': True}))
#     city = forms.ModelChoiceField(label=city_label, queryset=City.objects.all(), required=True, empty_label=city_label,
#                                   widget=forms.Select(attrs={'placeholder': city_label}))
#     product_catalog = forms.ModelChoiceField(
#         label=product_catalog_label,
#         queryset=WorkCatalog.objects.filter(state=WorkCatalog.STATE_PUBLISH, level=0),
#         required=True,
#         empty_label=product_catalog_label,
#         widget=forms.Select(attrs={'placeholder': product_catalog_label})
#     )
#     phone = SplitPhoneField(label=phone_label, required=True,
#                             widget=SplitPhoneWidget(attrs={'placeholder': phone_label, 'required': True}))
#     title = forms.CharField(label=title_label,
#                             widget=forms.TextInput(attrs={'placeholder': title_label, 'required': True}))
#     description = forms.CharField(label=description_label,
#                                   widget=CKEditorWidget(attrs={'placeholder': description_label, 'required': True}))
#
#     class Meta:
#         model = Order
#         fields = ("name", "email", "phone", "title", "description", "city", "product_catalog")
#
#     def save(self, user, commit=True):
#         order = super(OrderAddOrEditForm, self).save(commit=False)
#         order.customer = user.profile
#         if commit:
#             order.save()
#         return order


# class AddOfferToOrderForm(forms.ModelForm):
#     action_text = "add_offer"
#     offer_label = u'Ответ'
#     price_label = u'Цена'
#     currency_label = u'Валюта'
#
#     action = forms.CharField(max_length=255, widget=forms.HiddenInput)
#     offer = forms.CharField(label=offer_label,
#                             widget=forms.Textarea(attrs={'placeholder': offer_label, 'required': True}))
#     price = forms.IntegerField(label=price_label,
#                                widget=forms.TextInput(attrs={'placeholder': price_label, 'required': True}))
#     currency = forms.ModelChoiceField(label=currency_label, queryset=Currency.objects.filter(is_currency=True), empty_label=None,
#                                       widget=forms.Select(attrs={'placeholder': currency_label, 'required': True}))
#
#     class Meta:
#         model = OfferToOrder
#         fields = ("offer", "price", "currency")
#
#     def __init__(self, *args, **kwargs):
#         super(AddOfferToOrderForm, self).__init__(*args, **kwargs)
#
#         self.initial['action'] = self.action_text
#
#     def save(self, request, order_id, commit=True):
#         self.performer = request.user.profile
#         self.order_id = order_id
#         offer = super(AddOfferToOrderForm, self).save(commit=False)
#         offer.performer = self.performer
#         offer.order = get_object_or_404(Order, id=self.order_id)
#         if commit:
#             offer.save()
#         return offer


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("email",)


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """
    error_messages = {
        'duplicate_email': _("Пользователь с такой почтой уже зарегистрирован."),
        'password_mismatch': _("Пароли не совпадают."),
    }

    email_label = u'E-mail'
    password_label1 = u'Пароль'
    password_label2 = u'Повторите пароль'

    email = forms.EmailField(label=email_label, error_messages={},
                             widget=forms.TextInput(attrs={'placeholder': email_label, 'required': True}))
    password1 = forms.CharField(label=password_label1,
                                widget=forms.PasswordInput(attrs={'placeholder': password_label1, 'required': True}))
    password2 = forms.CharField(label=password_label2,
                                widget=forms.PasswordInput(attrs={'placeholder': password_label2, 'required': True}))

    class Meta:
        model = User
        fields = ("email",)

    def clean_email(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def get_password(self):
        return self.cleaned_data.get("password1")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """

    email_label = u'E-mail'
    password_label = u'Пароль'

    email = forms.EmailField(
        label=email_label, error_messages={},
        widget=forms.EmailInput(attrs={'placeholder': email_label, 'required': True}))
    password = forms.Field(
        label=password_label,
        widget=forms.PasswordInput(attrs={'placeholder': password_label, 'required': True}))

    error_messages = {
        'invalid_login': _(u"Совпадений %s/%s не найдено. "
                           u"Проверьте введенные данные и повторите снова." % (email_label, password_label)),
        'inactive': _(u"Аккаунт не активирован."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        # Set the label for the "username" field.
        UserModel = get_user_model()
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if self.fields['email'].label is None:
            self.fields['email'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(username=email,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    # params={'email': self.email_label},
                )
            elif not self.user_cache.is_active:
                raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )
        return self.cleaned_data

    def check_for_test_cookie(self):
        warnings.warn(
            "check_for_test_cookie is deprecated; ensure your login "
            "view is CSRF-protected.", DeprecationWarning)

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache
