# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from sorl.thumbnail import ImageField

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _

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
    country = models.ForeignKey(Country, verbose_name=u'Страна', null=True, blank=True)
    user_type = models.IntegerField(verbose_name=u'Тип пользователя', null=True, blank=True, choices=USER_TYPES)
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
    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

# Create your models here.

class CamService(models.Model):
    name = models.CharField(verbose_name=u'Наименование', max_length=100)
    image = ImageField(verbose_name='Иконка', upload_to='camservice')
    url = models.CharField(verbose_name=u'Ссылка', max_length=100)
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

class Model(models.Model):
    name = models.CharField(verbose_name=u'Ник', max_length=100, )
    display_name = models.CharField(verbose_name=u'Ник', max_length=100, )
    description = models.TextField(verbose_name=u'Описание', blank=True)
    profile_image = models.CharField(verbose_name=u'Картинка профиля', max_length=100, blank=True)
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
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    online_time = models.PositiveIntegerField(verbose_name=u'Время онлайн', default=0)
    views_count = models.PositiveIntegerField(verbose_name=u'Просмотры', default=0)
    user = models.ForeignKey(User, verbose_name=u'Пользователь', null=True, blank=True)
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

class AgeTag(models.Model):
    """docstring for AgeTag"""
    name = models.CharField(verbose_name=u'Название', max_length=100, )

    def __unicode__(self):
        return self.name