# -*- coding: UTF-8 -*-
from PIL import Image
from main.models import AbstractStatus
from django.forms import RadioSelect
from django.utils.translation import ugettext_lazy as _

from django import forms

from livecamsbay import settings
from main.mixin import MixinForm
from main.widgets import ImageInput


class RecoverPasswordForm(MixinForm, forms.Form):
    """
    Форма для ввода email при восстановления пароля
    """

    action_text = "recover_password"
    email_label = u'E-mail'

    action = forms.CharField(max_length=255, widget=forms.HiddenInput)
    email = forms.EmailField(label=email_label,
                             widget=forms.TextInput(attrs={'placeholder': email_label, 'required': True}))

    def clean_email(self):
        from main.models import User
        email = self.cleaned_data.get('email')

        try:
            self.user_cache = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError(
                u'Пользователь с такой почтой не найден.',
                code='invalid_email',
            )

        return self.cleaned_data.get('email')

    def __init__(self, *args, **kwargs):
        self.user_cache = None
        super(RecoverPasswordForm, self).__init__(*args, **kwargs)
        self.initial['action'] = self.action_text

    def get_user(self):
        return self.user_cache


class RecoverPasswordKeyForm(MixinForm, forms.Form):
    """
    Форма для ввода ключа из письма для восстановления пароля.
    используется если пользователь не перешел по ссылке, а скопировал ключ
    """

    action_text = "recover_password_code"
    key_label = u'Введите код'

    action = forms.CharField(max_length=255, widget=forms.HiddenInput)
    key = forms.CharField(label=key_label, widget=forms.TextInput(attrs={'placeholder': key_label, 'required': True}))

    def __init__(self, *args, **kwargs):
        super(RecoverPasswordKeyForm, self).__init__(*args, **kwargs)
        self.initial['action'] = self.action_text


class ChangePasswordForm(MixinForm, forms.Form):
    """
    Форма смены пароля
    """

    error_messages = {
        'password_mismatch': _("Введенные пароли не совпадают."),
    }
    password1_label = u'Придумайте новый пароль'
    password2_label = u'Повторите'

    password1 = forms.CharField(label=password1_label,
                                widget=forms.PasswordInput(attrs={'placeholder': password1_label, 'required': True}))
    password2 = forms.CharField(label=password2_label,
                                widget=forms.PasswordInput(attrs={'placeholder': password2_label, 'required': True}))

    def clean(self):
        super(ChangePasswordForm, self).clean()
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )

    def get_password(self):
        return self.cleaned_data.get("password1")


class ImageForm(forms.ModelForm):
    """
    Устаревшее
    """
    image = forms.ImageField(widget=ImageInput)

    def clean(self):
        cleaned_data = self.cleaned_data.get('image')
        try:
            img = Image.open(cleaned_data)
            w, h = img.size
            max_w, max_h = settings.IMG_SIZE['L']
            if w < max_w or h < max_h:
                raise forms.ValidationError(
                    'Проверте размеры картинки, должна быть не меньше 250x250',
                    code='bad size',
                )
        except AttributeError:
            raise forms.ValidationError(
                'Подходящие форматы: jpg, png, gif',
                code='bad format',
            )


class AbsUserContentForm(MixinForm, forms.ModelForm):
    """
    Максин для форм добавлений контента пользователем
    в форме отображаются две кнопки "в черновик"/"опубликовать"
    """
    state = forms.ChoiceField(widget=RadioSelect(),
                              choices=(st for st in AbstractStatus.STATES if st[0] in (AbstractStatus.STATE_TO_PUBLISH,
                                                                                       AbstractStatus.STATE_DRAFT)))
