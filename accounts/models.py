# -*- coding: UTF-8 -*-
from collections import namedtuple

from django.db.models.query_utils import Q
from django.db import models, IntegrityError
from django.db.transaction import atomic
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.conf import settings
from django.forms import inlineformset_factory

from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.files import get_thumbnailer

from main.models import AbstractBaseClass, AbstractStatus

from email_sender.models import EmailSetting, EmailGroup

from django.utils.translation import ugettext_lazy as _

from os import path


class ProfileQuerySet(models.QuerySet):
    def producers(self):
        return self.exclude(role=Profile.ROLE_USER).filter(state=Profile.STATE_PUBLISH)


class ProfileManager(models.Manager):
    def get_queryset(self):
        return ProfileQuerySet(self.model, using=self._db)

    def producers(self):
        return self.get_queryset().producers()


class Profile(AbstractBaseClass):
    """
    Модель профиля пользователя.
    Основная модель, она используется в создаваемых пользователем материалах.
    """
    objects = ProfileManager()

    ROLE_USER = 'u'
    ROLE_MODEL = 'm'
    ROLE_COMPANY = 'c'
    ROLE_DEAD_SOUL = 'd'

    ROLE_CHOICES = (
        (ROLE_USER, 'User'),
        (ROLE_MODEL, 'Model'),
        (ROLE_COMPANY, 'Company'),
        (ROLE_DEAD_SOUL, 'Dead soul'),
    )

    role = models.CharField(max_length=1, choices=ROLE_CHOICES)

    name = models.CharField("Profile name", max_length=255)
    city = models.ForeignKey('cities_light.City', null=True)
    short_description = models.CharField("Short description", max_length=255, default='', null=True, blank=True)
    description = models.TextField("Description", default='', null=True, blank=True)
    avatar = ThumbnailerImageField(u"Avatar", upload_to="profile_images", null=True, blank=True)
    # TODO: replace to state
    certified = models.BooleanField("Certified by the moderator", default=True)
    completed = models.BooleanField("Completed information", default=False)
    address = models.CharField("Address", max_length=255, null=True, blank=True)
    position = models.PositiveIntegerField(_('position'), null=True, default=None)
    point = models.PositiveSmallIntegerField(_(u'баллы'), default=0)

    def is_user(self):
        """
        Проверка, что пользователь является заказчиком
        """
        return self.role == self.ROLE_USER

    def is_company(self):
        """
        Проверка, что пользователь является компанией
        """
        return self.role == self.ROLE_COMPANY

    def is_producers(self):
        """
        Проверка, что пользователь имеет права исполнителя
        """
        return self.role in (self.ROLE_MASTER, self.ROLE_COMPANY)

    def phone(self):
        """
        Получение номера телефона. (Устаревшее)
        """
        phones = self.profilephone_set.all()
        return phones[0].phone if phones.count() else ''

    def email(self):
        """
        Получение адреса почты. (Устаревшее)
        """
        emails = self.profileemail_set.all()
        return emails[0].email if emails.count() else ''

    def get_avatar(self):
        """
        Получение аватара, если его нет или файл не найден, то дефолтная картинка
        """
        if self.avatar and path.exists(self.avatar.path):
            ava = self.avatar
        else:
            print settings.DEFAULT_IMAGE
            ava = get_thumbnailer(open(settings.DEFAULT_IMAGE), relative_name='default.png')
            print ava
        return ava

    # Foreign data

    def get_email(self):
        """
        Получение адреса электронной почты пользователя, с которой он регистрировался
        """
        # if self.role == Profile.ROLE_USER:
        #     return self.user_set.all()[0].email
        # emails = self.profileemail_set.all()
        # return emails[0].email if emails.count() else ''
        return self.user_set.all()[0].email

    def get_actual_emails(self):
        """
        Получение актуальных адресов электронной почты.
        Из базы выбираются, только адреса существующих людей.
        Исключены тестовые.
        """
        emails = list(
            user.email for user in self.user_set.filter(
                is_admin=False, is_staff=False, is_active=True
            ).exclude(Q(email__endswith='loc') | Q(email__endswith='amigostone.ru')))
        emails += list(profileemail.email for profileemail in self.profileemail_set.all()
                       .exclude(Q(email__endswith='loc') | Q(email__endswith='amigostone.ru')))
        return emails

    def get_phone(self):
        """
        Получение номера телефона
        """
        phones = self.profilephone_set.all()
        return phones[0].phone if phones.count() else ''

    def get_url(self):
        """
        Получение адреса сайта компании или мастера
        """
        urls = self.profileurl_set.all()
        return urls[0].url if urls.count() else ''

    # FORMS

    def get_profile_account_form(self):
        """
        В зависимости от роли пользователя, для редактирования профиля, ему дается определенная форма.
        Формы в основном отличаются названием полей.
        """
        from accounts.forms import ProfileAccountForm, ProfileMasterForm, ProfileCompanyForm
        if self.is_user():
            return ProfileAccountForm
        elif self.is_company():
            return ProfileCompanyForm
        else:
            return ProfileMasterForm

    def get_profile_account_formset(self):
        """
        Расширенные формы для заполнения профиля. Так же зависят от роли пользователя
        """
        if self.role == 'a':  # (Устаревшее) У обычного заказчика нет дополнительных форм
            return [Profile.get_profile_email_formset(), Profile.get_profile_email_formset()]
        elif self.role == 'c':  # Компания
            return [Profile.get_profile_email_formset(), Profile.get_profile_email_formset(),
                    Profile.get_profile_url_formset(), Profile.get_profile_contact_person_formset()]
        else:  # Мастер-
            return [Profile.get_profile_email_formset(), Profile.get_profile_email_formset()]

    @staticmethod
    def get_profile_phone_formset():
        """
        Форма для добавления номера телефона
        """
        from accounts.forms import ProfilePhoneForm
        return inlineformset_factory(Profile, ProfilePhone, ProfilePhoneForm, extra=1, min_num=1, max_num=1, can_delete=False)

    @staticmethod
    def get_profile_email_formset():
        """
        Форма для добавления электронного почтового адреса
        """
        from accounts.forms import ProfileEmailForm
        return inlineformset_factory(Profile, ProfileEmail, ProfileEmailForm, extra=1, min_num=1, max_num=1, can_delete=False)

    @staticmethod
    def get_profile_url_formset():
        """
        Форма для добавления электроного адреса компании
        """
        from accounts.forms import ProfileUrlForm
        return inlineformset_factory(Profile, ProfileUrl, ProfileUrlForm, extra=1, min_num=1, max_num=1, can_delete=False)

    @staticmethod
    def get_profile_director_form():
        """
        Форма для добавления Гендиректора
        """
        from accounts.forms import ProfileDirectorForm
        return ProfileDirectorForm
        # return inlineformset_factory(Profile, ProfileDirector, ProfileDirectorForm, extra=1, min_num=1, max_num=1,
        # can_delete=False)

    @staticmethod
    def get_profile_bank_details_form():
        """
        Форма для добавления банковских реквизитов
        """
        from accounts.forms import ProfileBankDetailsForm
        return ProfileBankDetailsForm
        # return inlineformset_factory(Profile, ProfileBankDetails, ProfileBankDetailsForm, extra=1, min_num=1,
        # max_num=1, can_delete=False)

    def __unicode__(self):
        return self.name

    def get_public_abs_url(self):
        """
        Ссылка на публичный профиль
        """
        return reverse('companies:profile_view', args=[self.slug])

    def get_email_settings(self):
        """
        Список доступных подписок на рассылки
        """
        if self.is_user():
            f = EmailGroup.PERSON
        else:
            f = EmailGroup.COMPANY
        return EmailSetting.objects.filter(email_groups__title=f)

    def get_email_subs(self, cached=False):
        """
        Формирование списка подписок на рассылки сгрупированного по темам
        """
        if cached:
            try:
                return self._get_email_subs
            except AttributeError:
                pass

        # p = EmailSetting.objects.raw('select es.id, es.group, es.action, es.description, esp.profile_id from email_sender_emailsetting as es '
        #                              'inner join email_sender_emailgroup_settings as egs on (es.id = egs.emailsetting_id) '
        #                              'inner join email_sender_emailgroup as eg on (egs.emailgroup_id = eg.id) '
        #                              'left join email_sender_emailsetting_profiles as esp on (es.id = esp.emailsetting_id and esp.profile_id=%s)'
        #                              'where eg.title="%s" and es.changeable=true' % (self.id, f))

        email_settings = self.get_email_settings().filter(changeable=True)
        accepts = {e.id for e in self.email_settings.all()}
        setting = namedtuple('ESetting', 'action description accept group')
        aggregate = sorted(
            (setting(
                s.action,
                s.description,
                True if s.id in accepts else False,
                EmailSetting.group_name(s.group))
                for s in email_settings
             ),
            key=lambda x: x.group)
        self._get_email_subs = aggregate
        return aggregate

    def update_email_subs(self, settings):
        """
        Обновление подписок на рассылки.
        Получает id-шники, сравнивает с теми которы в базе,
        после чего добавляет или удаляет.
        """
        new_accepts = set(settings)
        aggregate = self.get_email_subs(cached=True)
        all_settings = {s.action for s in aggregate}
        current_accepts = {s.action for s in aggregate if s.accept}
        assert new_accepts.issubset(all_settings)
        to_add = new_accepts - current_accepts
        to_remove = current_accepts - new_accepts
        if to_add:
            to_add = EmailSetting.objects.filter(action__in=to_add)
            self.email_settings.add(*to_add)
        if to_remove:
            to_remove = EmailSetting.objects.filter(action__in=to_remove)
            self.email_settings.remove(*to_remove)

    def get_rating(self):
        from common.models import PointSystem, PointAction
        rating = 0
        for item in self.pointaction_set.all():
            rating += item.content_type.pointsystem.point
        return rating

    # def get_seo_title(self):
    #     # try:
    #     #     if self.meta.title:
    #     #         return self.meta.title
    #     # except models.ObjectDoesNotExist:
    #     #     pass
    #     company_role = ''
    #     if self.provider and self.stoneworker:
    #         company_role = u'производство изделий из камня и поставки'
    #     elif self.provider:
    #         company_role = u'производитель изделий из камня'
    #     elif self.stoneworker:
    #         company_role = u'поставщик каменной отрасли'
    #
    #     try:
    #         if self.is_company():
    #             return u'Компания {0} {1} в городе {2}'.format(self.name, company_role, self.city)
    #         else:
    #             return ''
    #     except AttributeError:
    #         return ''
    #
    # def get_seo_description(self):
    #     # try:
    #     #     if self.seo.description:
    #     #         return self.seo.description
    #     # except models.ObjectDoesNotExist:
    #     #     pass
    #     company_role = ''
    #     if self.provider and self.stoneworker:
    #         company_role = u'производство изделий из камня и поставки'
    #     elif self.provider:
    #         company_role = u'производитель изделий из камня'
    #     elif self.stoneworker:
    #         company_role = u'поставщик каменной отрасли'
    #     try:
    #         if self.is_company():
    #             return u'Компания {0} {1} в городе {2} по самым выгодным ценам.'.format(self.name, company_role, self.city)
    #         else:
    #             return ''
    #     except AttributeError:
    #         return ''
    #
    # def get_seo_keywords(self):
    #     # try:
    #     #     if self.seo.keywords:
    #     #         return self.seo.keywords
    #     # except models.ObjectDoesNotExist:
    #     #     pass
    #     company_role = ''
    #     if self.provider and self.stoneworker:
    #         company_role = u'производство изделий из камня и поставки'
    #     elif self.provider:
    #         company_role = u'производитель изделий из камня'
    #     elif self.stoneworker:
    #         company_role = u'поставщик каменной отрасли'
    #
    #     try:
    #         if self.is_company():
    #             return u'компания {0}, {1}, {1} в {2}'.format(self.name, company_role, self.city)
    #         else:
    #             return ''
    #     except AttributeError:
    #         return ''


class ProfilePhone(models.Model):
    """
    Дополнительные номера телефонов.
    Используются у компании и мастера
    """

    profile = models.ForeignKey(Profile)
    phone = models.CharField("Phone number", max_length=255)

    class Meta:
        verbose_name = u"Телефон профиля"
        verbose_name_plural = u"Телефоны профиля"

    def __unicode__(self):
        return u'%s' % self.phone


class ProfileEmail(models.Model):
    """
    Дополнительные адреса электронных почт.
    Используются у компании и мастера
    """

    profile = models.ForeignKey(Profile)
    email = models.EmailField("Email", max_length=255)

    class Meta:
        verbose_name = u"Email профиля"
        verbose_name_plural = u"Email профиля"

    def __unicode__(self):
        return u'%s' % self.email


class ProfileUrl(models.Model):
    """
    Дополнительные электронные адреса.
    Используются у компании и мастера
    """

    profile = models.ForeignKey(Profile)
    url = models.CharField("Url", max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = u"Сайт профиля"
        verbose_name_plural = u"Сайты профиля"

    def __unicode__(self):
        return u'%s' % self.url


class ProfileHash(models.Model):
    """
    Вычисляется хэш для пользователя.
    Хэш используется для подключения "личного" вебсокета.
    """

    profile = models.OneToOneField(Profile)
    hash_str = models.CharField(max_length=255, unique=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.hash_str = self.generate_profile_hash()
        super(ProfileHash, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def generate_profile_hash(self):
        import hashlib
        import random

        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        return hashlib.sha1(salt + str(self.profile.id)).hexdigest()


class FavoriteModel(AbstractBaseClass):
    profile = models.ForeignKey(Profile)
    model = models.ForeignKey('main.Model')

# class ViewInstanceManager(models.Manager):
#     def get_or_create(self, content_object):
#         content_type = ContentType.objects.get_for_model(content_object)
#         return super(ViewInstanceManager, self).get_or_create(content_type=content_type, object_id=content_object.id)[0]
#
#
# class ViewInstance(models.Model):
#     # уже не нужна, можно по позже удалить но проверить не используеться где либо еще
#     content_type = models.ForeignKey(ContentType)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')
#     profiles = models.ManyToManyField(Profile)
#     # counter = models.PositiveIntegerField(default=0)
#     # unique_views = models.PositiveIntegerField(default=0)
#
#     objects = ViewInstanceManager()
#
#     class Meta:
#         unique_together = ('content_type', 'object_id')
