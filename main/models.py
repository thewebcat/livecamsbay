# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from sorl.thumbnail import ImageField

from django.template.loader import render_to_string
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from livecamsbay.redis_connection import redis_conn
from main.sendmail import send_mail

from .emails import model_recall

import datetime
import hashlib
import random


class Country(models.Model):
    name = models.CharField(u'Название', max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Страна'
        verbose_name_plural = u'Страны'


class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = (
        (1, u'Модель'),
        (2, u'Пользователь'),
    )

    email = models.EmailField(unique=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    country = models.ForeignKey(Country, verbose_name=u'Страна', null=True, blank=True)
    user_type = models.IntegerField(verbose_name=u'Тип пользователя', null=True, blank=True, choices=USER_TYPES)
    profile = models.ForeignKey('accounts.Profile', blank=True, null=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    recover_pass_key = models.CharField("Recovery password key", max_length=40, blank=True, null=True)
    recover_pass_active = models.BooleanField("recover pass active", default=False)

    access_key = models.CharField("Access key", max_length=40, blank=True, null=True)
    access_key_active = models.BooleanField("Access key active", default=False)

    ACCOUNT_ACTIVATION_DAYS = 5
    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def activation_key_expired(self):
        """
        Determine whether this ``User``'s activation
        key has expired, returning a boolean -- ``True`` if the key
        has expired.

        Key expiration is determined by a two-step process:

        1. If the user has already activated, the key will have been
           reset to the string constant ``ACTIVATED``. Re-activating
           is not permitted, and so this method returns ``True`` in
           this case.

        2. Otherwise, the date the user signed up is incremented by
           the number of days specified in the setting
           ``ACCOUNT_ACTIVATION_DAYS`` (which should be the number of
           days after signup during which a user is allowed to
           activate their account); if the result is less than or
           equal to the current date, the key has expired and this
           method returns ``True``.

        """
        expiration_date = datetime.timedelta(days=self.ACCOUNT_ACTIVATION_DAYS)
        return self.activation_key == self.ACTIVATED or (
            self.user.date_joined + expiration_date <= datetime.datetime.now())
    activation_key_expired.boolean = True

    def send_mail(self, action, dictionary=None):
        """
        Формирование и отправка письма
        @param action - наименование директории с шаблоном письма (templates/auth/)
            registration - шаблон письма с ключом активации после регистрации пользователя
            activation   - шаблон письма с данными пользователя после активации
            recover      - шаблон письма после запроса на восстановление пароля
            recover_pass - шаблон письма с подтверждением смены пароля
        @param dictionary - словарь с данными, которые нужны в шаблоне письма

        """
        ctx_dict = {
            'user': self,
            'company': settings.COMPANY,
            'domain': settings.DOMAIN
        }
        if dictionary is not None:
            ctx_dict.update(dictionary)

        subject = render_to_string('auth/' + action + '/email_subject.txt', ctx_dict)
        subject = ''.join(subject.splitlines())

        message = render_to_string('auth/' + action + '/email_content.txt', ctx_dict)
        # print u"%s" % message
        # print "%s %s %s %s" % (settings.DEFAULT_FROM_EMAIL, self.email, subject, message, )
        send_mail(settings.DEFAULT_FROM_EMAIL, self.email, subject, message, )

    def recover_pass_activate(self):
        """
        Устанавливается метка в значение True, указывающая на то, что пользователь
        воспользовался функцией восстановления пароля.
        Генерируется ключ по которому будет опозноваться пользователь.
        """
        self.recover_pass_active = True
        self.recover_pass_key = self.generate_recover_pass_key()
        self.save()

        from django.core.urlresolvers import reverse
        from main.func import build_absolute_uri
        from email_sender.models import EmailSender
        e = EmailSender()
        data = {
            'site_url': build_absolute_uri(),
            'name': self.name,
            'password_key_url': build_absolute_uri("%s?key=%s" % (reverse('authorization:recover_password'), self.recover_pass_key)),
            'input_password_key_url': build_absolute_uri(reverse('authorization:forgot_password_enter_key')),
            'recover_pass_key': self.recover_pass_key
        }
        e.create_message_from_template(template_name='forgot_password', data=data)
        e.send_to(email_addresses=self.email)

    def recover_pass_deactivate(self):
        """
        Устанавливается метка в значение False, указывающая на то, что пользователь
        успешно сменил пароль.
        """
        self.recover_pass_active = False
        self.save()

        from main.func import build_absolute_uri
        from email_sender.models import EmailSender
        e = EmailSender()
        data = {
            'site_url': build_absolute_uri(),
            'name': self.name,
        }
        e.create_message_from_template(template_name='change_password', data=data)
        e.send_to(email_addresses=self.email)

    def generate_recover_pass_key(self):
        """
        Создание секретного ключа для восстановления пароля
        """
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        return hashlib.sha1(salt + self.email).hexdigest()

    def access_key_activate(self, commit=True):
        """
        Установка ключа для активации
        """
        self.access_key = self.generate_recover_pass_key()
        self.access_key_active = True
        if commit:
            self.save()

    def access_key_deactivate(self):
        """
        После успешной активации устанавливается флаг, чтобы нельзя было повторно пройти активацию
        """
        self.access_key_active = False
        self.save()
# Create your models here.


class CamService(models.Model):
    name = models.CharField(verbose_name=u'Наименование', max_length=100)
    image = ImageField(verbose_name='Иконка', upload_to='camservice')
    url = models.CharField(verbose_name=u'Ссылка', max_length=255)
    prefix = models.CharField(verbose_name=u'Префикс', max_length=100)
    api_url = models.CharField(verbose_name=u'Апи url', max_length=255)
    active = models.BooleanField(default=True)


class Sex(models.Model):
    name = models.CharField(verbose_name=u'Пол', max_length=100)
    code = models.CharField(verbose_name=u'Код', max_length=10, db_index=True, unique=True)

    def __unicode__(self):
        return self.name


class Race(models.Model):
    name = models.CharField(verbose_name=u'Расса', max_length=100)
    code = models.CharField(verbose_name=u'Код', max_length=10, db_index=True, unique=True)

    def __unicode__(self):
        return self.name


class HairColor(models.Model):
    name = models.CharField(verbose_name=u'Цвет волос', max_length=100)
    code = models.CharField(verbose_name=u'Код', max_length=10, db_index=True, unique=True)

    def __unicode__(self):
        return self.name


class BustSize(models.Model):
    name = models.CharField(verbose_name=u'Размер груди', max_length=100)
    code = models.CharField(verbose_name=u'Код', max_length=10, db_index=True, unique=True)

    def __unicode__(self):
        return self.name


class Figure(models.Model):
    name = models.CharField(verbose_name=u'Фигура', max_length=100)
    code = models.CharField(verbose_name=u'Код', max_length=10, db_index=True, unique=True)

    def __unicode__(self):
        return self.name


class SpeaksLanguage(models.Model):
    name = models.CharField(verbose_name=u'Язык', max_length=100)
    code = models.CharField(verbose_name=u'Код', max_length=10, db_index=True, unique=True)

    def __unicode__(self):
        return self.name


class PublicArea(models.Model):
    name = models.CharField(verbose_name=u'На показ', max_length=100)
    code = models.CharField(verbose_name=u'Код', max_length=10, db_index=True, unique=True)

    def __unicode__(self):
        return self.name


class Extra(models.Model):
    name = models.CharField(verbose_name=u'Особое', max_length=100)
    code = models.CharField(verbose_name=u'Код', max_length=10, db_index=True, unique=True)

    def __unicode__(self):
        return self.name


class AbstractStatus(models.Model):
    """
    Абстрактный класс. В нем указаные возможные состояния обектов (удален, опубликован ...)
    """
    STATE_TO_PUBLISH = 0
    STATE_PUBLISH = 1
    STATE_REMOVE = 2
    STATE_DRAFT = 3

    STATES = (
        (STATE_TO_PUBLISH, u"не опубликован"),
        (STATE_PUBLISH, u"опубликован"),
        (STATE_REMOVE, u"удален"),
        (STATE_DRAFT, u"перенесен в черновик"),
    )

    state = models.IntegerField(verbose_name=u"Статус", choices=STATES, default=STATE_DRAFT)

    def is_publish(self):
        """
        Проверка, что материал опубликован
        """
        return self.state == self.__class__.STATE_PUBLISH

    def is_to_publish(self):
        """
        Проверка, что материал отправлен на модерацию
        """
        return self.state == self.__class__.STATE_TO_PUBLISH

    def is_draft(self):
        """
        Проверка, что материал находится в черновиках
        """
        return self.state == self.__class__.STATE_DRAFT

    @classmethod
    def get_beauty_name(cls):
        """
        Возвращает человекопонятное название модели в единственном числе
        """
        return cls._meta.verbose_name

    @classmethod
    def get_beauty_name_plural(cls):
        """
        Возвращает человекопонятное название модели во множественном числе
        """
        return cls._meta.verbose_name_plural

    class Meta:  # noqa
        abstract = True


class AbstractBaseClass(AbstractStatus):
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def mark_as_removed(self, commit=False):
        """
        Пометить материал удаленным
        """
        self.state = self.STATE_REMOVE
        self.to_save(commit)

    def mark_as_published(self, commit=False):
        """
        Пометить материал опубликованным
        """
        self.state = self.STATE_PUBLISH
        self.to_save(commit)

    def mark_as_to_published(self, commit=False):
        """
        Пометить материал отправленным на модерацию
        """
        self.state = self.STATE_TO_PUBLISH
        self.to_save(commit)

    def mark_as_draft(self, commit=False):
        """
        Пометить материал как черновик
        """
        self.state = self.STATE_DRAFT
        self.to_save(commit)

    def to_save(self, commit):
        if commit:
            self.save()

    def get_actions_html(self):
        """
        Формирует html код для отбражения значков "редактировать/удалить" на материале в личном кабинете
        """
        if self.profile:
            return render_to_string(template_name='main/elements/actions_html.html', context={'instance': self})
        else:
            return ""

    def create_redis_key(self):
        '''
        -----------------------------------------------------
        Используеться в подсчете количества просмотров материала
        -----------------------------------------------------

        Формирует и возвращает имя, которое будет использоваться в качестве ключа для redis
        Имя состоит из "название приложения"_"название модели"_"id записи в таблице"
        '''
        return '{}_{}_{}'.format(self._meta.app_label, self._meta.model_name, self.id)

    def set_redis_key(self, value=None):
        '''
        Функция передает в redis по указанному ключу значение value.
        '''
        redis_conn.set(self.create_redis_key(), value)

    def set_redis_key_incr(self):
        '''
        -----------------------------------------------------
        Используеться в подсчете количества просмотров материала
        -----------------------------------------------------

        Функция использует имя в качестве ключа в redis,
        и устанавливает инкремент в качестве значения этого ключа.
        При каждом вызове метода инкремент будет увеличиваться.
        '''
        redis_conn.incr(self.create_redis_key())

    def get_redis_key(self):
        '''
        -----------------------------------------------------
        Используеться в подсчете количества просмотров материала
        -----------------------------------------------------

        Возвращает значение по ключу из redis
        '''
        return redis_conn.get(self.create_redis_key())

    @staticmethod
    def get_css_class_for_actions():
        return 'container_action_bar'

    @staticmethod
    def get_css_class_for_actions_visible():
        return 'container_action_bar_visible'


class Model(AbstractBaseClass):
    name = models.CharField(verbose_name=u'Ник', max_length=100, )
    display_name = models.CharField(verbose_name=u'Ник', max_length=100, )
    description = models.TextField(verbose_name=u'Описание', blank=True)
    profile_image = models.CharField(verbose_name=u'Картинка профиля', max_length=200, blank=True)
    profile_url = models.CharField(verbose_name=u'Ссылка на профиль', max_length=200, blank=True)
    chat_url = models.CharField(verbose_name=u'Ссылка на чат', max_length=200, blank=True)
    available = models.BooleanField(default=False)
    age = models.PositiveIntegerField(verbose_name=u'Возраст', default=0)
    sex = models.ForeignKey(Sex, verbose_name=u'Пол', null=True, blank=True)
    race = models.ForeignKey(Race, verbose_name=u'Расса', null=True, blank=True)
    hair_color = models.ForeignKey(HairColor, verbose_name=u'Цвет волос', null=True, blank=True)
    bust_size = models.ForeignKey(BustSize, verbose_name=u'Размер груди', null=True, blank=True)
    figure = models.ForeignKey(Figure, verbose_name=u'Фигура', null=True, blank=True)
    speaks_language = models.ManyToManyField(SpeaksLanguage, verbose_name=u'Язык', blank=True)
    public_area = models.ForeignKey(PublicArea, verbose_name=u'На показ', null=True, blank=True)
    extra = models.ManyToManyField(Extra, verbose_name=u'Особое', blank=True)
    online_time = models.PositiveIntegerField(verbose_name=u'Время онлайн', default=0)
    views_count = models.PositiveIntegerField(verbose_name=u'Просмотры', default=0)
    profile = models.ForeignKey('accounts.Profile', verbose_name=u'Пользователь', null=True, blank=True)
    cam_service = models.ForeignKey(CamService, verbose_name=u'Cam сервис')

    def __unicode__(self):
        return self.name

    def agetag(self):
        if self.age >= 18 and self.age < 21:
            return AgeTag.objects.get(pk=1).name
        elif self.age >= 21 and self.age < 30:
            return AgeTag.objects.get(pk=2).name
        elif self.age >= 30 and self.age < 55:
            return AgeTag.objects.get(pk=3).name
        elif self.age >= 55:
            return AgeTag.objects.get(pk=4).name

    class Meta:
        index_together = ["name", "available", "views_count"]

class CamSnapshot(AbstractBaseClass):
    model = models.ForeignKey(Model, verbose_name=u"Модель", null=True, blank=True)
    snapshot_url = models.CharField(verbose_name=u"Ссылка", max_length=255, blank=True)

    def __unicode__(self):
        return self.snapshot_url

    class Meta:
        ordering = ('-date_add',)


class AgeTag(models.Model):
    """docstring for AgeTag"""
    name = models.CharField(verbose_name=u'Название', max_length=100, )

    def __unicode__(self):
        return self.name


class ViewInstanceManager(models.Manager):
    def get_or_create(self, content_object):
        content_type = ContentType.objects.get_for_model(content_object)
        return super(ViewInstanceManager, self).get_or_create(content_type=content_type, object_id=content_object.id)[0]


class ViewInstance(models.Model):
    # уже не нужна, можно по позже удалить но проверить не используеться где либо еще
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    profiles = models.ManyToManyField('accounts.Profile')
    # counter = models.PositiveIntegerField(default=0)
    # unique_views = models.PositiveIntegerField(default=0)

    objects = ViewInstanceManager()

    class Meta:
        unique_together = ('content_type', 'object_id')


class ModelRecall(models.Model):
    """
    Отзыв о заказе/исполнителе
    Оставляется заказчиком
    """
    model = models.OneToOneField(Model)
    profile = models.ForeignKey('accounts.Profile')

    text = models.TextField(u'текст')
    RATES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )
    rate = models.PositiveSmallIntegerField(u'оценка', default=5)

    class Meta:
        verbose_name = u'отзыв'
        verbose_name_plural = u'отзывы'

    def __unicode__(self):
        return self.text[:20]

    def save(self, *args, **kwargs):
        """
        Переопределенный метод.
        Отправляется письмо модели, если у нее есть хозяин.
        """
        id = self.id
        super(ModelRecall, self).save(*args, **kwargs)
        if not id:
            model_recall(self)