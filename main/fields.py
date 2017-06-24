# coding=utf-8
import re

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import _lazy_re_compile
from django.utils.deconstruct import deconstructible


@deconstructible
class PhoneValidator(object):
    message = u'Не верный формат номера телефона'
    code = 'invalid'
    code_city_regex = _lazy_re_compile(r'\d{3,5}')
    phone_number_regex = _lazy_re_compile(r'\d{5,7}')

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        if not self.code_city_regex.match(self.find_all_numbers(value[1])):
            raise ValidationError(self.message, code=self.code)

        if not self.phone_number_regex.match(self.find_all_numbers(value[2])):
            raise ValidationError(self.message, code=self.code)

    def __eq__(self, other):
        return (
            isinstance(other, PhoneValidator) and
            (self.message == other.message) and
            (self.code == other.code)
        )

    @staticmethod
    def find_all_numbers(value):
        return ''.join(re.findall('\d', value))


class SplitPhoneWidget(forms.widgets.MultiWidget):
    """
    Виджет разделяющий номер телефона на три <input type="text"> части.
    """
    supports_microseconds = False

    def __init__(self, attrs=None):
        _attrs = (
            {'placeholder': '+7', 'maxlength': 2, 'required': False},
            {'placeholder': 'Код', 'maxlength': 5},
            {'maxlength': 9}
        )
        for d in _attrs:
            for key in attrs.keys():
                if key not in d:
                    d[key] = attrs[key]

        widgets = (forms.TextInput(attrs=_attrs[0]),
                   forms.TextInput(attrs=_attrs[1]),
                   forms.TextInput(attrs=_attrs[2]))
        super(SplitPhoneWidget, self).__init__(widgets, {})

    def decompress(self, value):
        if value:
            matches = re.match('^(\+?\w{1,2}) \((\w{3,5})\) (\d{1,3}-\d{2}-\d{2})$', value)
            if matches:
                return matches.groups()
        return [None, None, None]

    def render(self, name, value, attrs=None):
        r = super(SplitPhoneWidget, self).render(name, value, attrs)
        return '<div style="display: flex" class="phone_split">%s</div>' % r


class SplitPhoneField(forms.fields.MultiValueField):
    """
    Поле для forms.
    Из трех значений (полученных в request.POST, при использовании SplitPhoneWidget)
    собирает одно, которое можно будет в forms валидировать с помощью clean_my_field_name
    и это же, собранное, значение записывается в бд
    """
    widget = SplitPhoneWidget
    # default_validators = [PhoneValidator()]

    def __init__(self, *args, **kwargs):
        required = kwargs.get('required')

        if required is None:
            required = True

        list_fields = [forms.fields.CharField(max_length=2, required=False),
                       forms.fields.CharField(max_length=5, required=required),
                       forms.fields.CharField(max_length=9, required=required)]
        # kwargs['required'] = False
        super(SplitPhoneField, self).__init__(list_fields, *args, **kwargs)

    def compress(self, values):
        if values:
            phone_format = '{0}{1} ({2}) {3}'
            plus = '+' if values[0].startswith('+') else ''
            country_code = ''.join(re.findall('\d', values[0]))
            country_code = '+7' if country_code == '' else country_code
            city_code = ''.join(re.findall('\d', values[1]))
            phone_number = ''.join(re.findall('\d', values[2]))
            phone_numbers_re = re.match('(\d{1,3})(\d{2})(\d{2})', phone_number)
            if phone_numbers_re:
                phone_number = '-'.join(re.match('(\d{1,3})(\d{2})(\d{2})', phone_number).groups())
            else:
                phone_number = ''
            return phone_format.format(plus, country_code, city_code, phone_number)

    def clean(self, value):
        self.validate(value)
        # todo Разобраться с валидацией через стандартный механизм
        if value[1] != '' or value[2] != '':
            PhoneValidator()(value)
        value = self.compress(value)
        return value

    def validate(self, value):
        if (value[1] in self.empty_values or value[2] in self.empty_values) and self.required:
            raise ValidationError(self.error_messages['required'], code='required')
