# -*- coding: UTF-8 -*-
"""
Команда для импортирования камнеобработчиков из csv
Формат csv файла
"Город","Название компании или Камнеобработчик*","Контактное лицо**","Номер телефона","Email"
* Если мастер то в этом поле 'Камнеобработчик'
** Если мастер то значение из этого поля добавится вместо Название компании
"""
import csv
import io
import os
import re
import sys

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.core.validators import validate_email
from django.db import transaction

from accounts.forms import UserCreationForm, ProfilePhoneForm, BaseProfileForm
from accounts.models import ProfileHash, ProfileDirector, ProfileBankDetails, ProfileContactPerson
from geo.models import City

reload(sys)
sys.setdefaultencoding('utf8')


DEFAULT_PASSWORD = "Jg4kis32dFuf"


class Performer(dict):
    def __init__(self, *args):
        super(Performer, self).__init__()

        self.__setitem__('city', City.objects.get(title=args[0]).id)
        self.__setitem__('name', args[1])
        self.__setitem__('contactperson', args[2])
        self.__setitem__('phone', '{phone_0} ({phone_1}) {phone_2}'.format(**self.phone_to_number_dict(args[3])))
        self.update(self.phone_to_number_dict(args[3]))
        self.__setitem__('email', args[4])
        self.__setitem__('master', args[1] == u'Камнеобработчик')
        self.__setitem__('password1', DEFAULT_PASSWORD)
        self.__setitem__('password2', DEFAULT_PASSWORD)

    @staticmethod
    def phone_to_number_dict(value):
        """
        Номер телефона из строки в dict
        {'phone_0': '9', 'phone_1': '999', 'phone_2': '9999999'}
        для common.fields.SplitPhoneField
        """
        value = ''.join(re.findall('\d', value))
        return {
            'phone_0': '+7' if value[0] == '7' else value[0],
            'phone_1': value[1:4],
            'phone_2': value[4:]
        }


class FormValidationError(ValidationError):
    def __init__(self, form, performer):
        message = "For performer <{}> " \
                  "in form {} " \
                  "errors: {}".format(performer['email'], form.__class__, str(form.errors.as_json()))
        code = 'invalid'
        super(FormValidationError, self).__init__(message, code)


class Command(BaseCommand):

    csv_file = None
    performers = []

    def add_arguments(self, parser):
        parser.add_argument('file', help="Path to csv file")

    @transaction.atomic()
    def handle(self, *args, **options):
        self.csv_file = options['file']
        self.csv_to_list()
        self.remove_duplicates()
        self.validate_performers()
        self.save()
        self.save_cleaned_csv()

    def save_cleaned_csv(self):
        """
        Сохранение csv файла с валидными значениями исполнителей.
        """
        csv_file_cleaned = '.cleaned'.join(os.path.splitext(self.csv_file))
        with open(csv_file_cleaned, 'wb') as csvfile:
            spamwriter = csv.writer(csvfile)
            for performer in self.performers:
                spamwriter.writerow(
                    [
                        City.objects.get(id=performer['city']).title,
                        u'Камнеобработчик' if performer['master'] else performer['name'],
                        performer['contactperson'],
                        performer['phone'],
                        performer['email']
                    ]
                )

    def validate_performers(self):
        """
        Проверка валидности данных через django формы
        """
        for performer in self.performers:
            form = UserCreationForm(performer)
            form_profile = BaseProfileForm(performer)
            form_profile_phone = ProfilePhoneForm(performer)
            if not form.is_valid():
                raise FormValidationError(form, performer)
            if not form_profile.is_valid():
                raise FormValidationError(form, performer)
            if not form_profile_phone.is_valid():
                raise FormValidationError(form, performer)

    @transaction.atomic
    def save(self):
        """
        Сохранение через django формы
        """
        # Добавление исполнителя как и во вьюхе authorization.views.registration_account
        for performer in self.performers:
            if performer['master']:
                performer['name'] = performer['contactperson']
            form = UserCreationForm(performer)
            form_profile = BaseProfileForm(performer)
            form_profile_phone = ProfilePhoneForm(performer)
            if all([form.is_valid(), form_profile.is_valid(), form_profile_phone.is_valid()]):
                user = form.save(commit=False)
                profile = form_profile.save(commit=False)
                profile.role = profile.ROLE_MASTER if performer['master'] else profile.ROLE_COMPANY
                profile.save()
                ProfileHash(profile=profile).save()
                profile_phone = form_profile_phone.save(commit=False)
                profile_phone.profile = profile
                profile_phone.save()

                if profile.role == profile.ROLE_COMPANY:
                    ProfileDirector(profile=profile).save()
                    ProfileBankDetails(profile=profile).save()
                    ProfileContactPerson(profile=profile, contact_person=performer['contactperson']).save()
                user.profile = profile
                user.is_active = False
                user.save()

    def csv_to_list(self):
        """
        Чтение csv файла и запись его валидных данные в list
        """
        with io.open(self.csv_file, 'r', encoding='utf8') as csvfile:
            lines = csv.reader(csvfile, delimiter=',', quotechar='"')
            for line in lines:
                if self.is_email_valid(line[4]) and self.is_phone_valid(line[3]):
                    self.performers.append(Performer(*line))

    def remove_duplicates(self):
        """
        Удаляются дубликаты записей
        """
        new = []
        for performer in self.performers:
            if performer['phone'] not in [c['phone'] for c in new] and performer['email'] not in [c['email'] for c in new]:
                new.append(performer)
        self.performers = new

    @staticmethod
    def is_phone_valid(value):
        """
        Проверка на верный формат ввода номера телефона
        """
        return len(re.findall('\d', value)) == 11

    @staticmethod
    def is_email_valid(value):
        """
        Проверка на верный формат ввода Email
        """
        try:
            validate_email(value)
            return True
        except ValidationError:
            return False
