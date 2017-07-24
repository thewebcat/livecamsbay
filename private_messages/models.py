# -*- coding: UTF-8 -*-
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.template.loader import render_to_string
from accounts.models import Profile


class MessageRecipient(models.Model):
    """
    Связь автоматических уведомлений с пользователями и флагом просмотра сообщения
    """
    viewed = models.BooleanField("Viewed", default=False)
    profile = models.ForeignKey(Profile, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.profile


class BaseMessageAbstractModel(models.Model):
    """
    Фбстрактный класс
    Привязка уведомлений с конкретным материалом
    """
    content_type = models.ForeignKey(ContentType,
                                     verbose_name=_('content type'),
                                     related_name="content_type_set_for_%(class)s",
                                     blank=True, null=True)
    object_pk = models.IntegerField(_('object ID'), blank=True, null=True)
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_pk")

    class Meta:
        abstract = True

    def add_relation_object(self, obj):
        """
        Добавление материала к уведомлению
        """
        self.object_pk = str(obj._get_pk_val())
        self.content_type = ContentType.objects.get_for_model(obj)

    def get_relation_object(self):
        """
        Получение материала привязанного к уведомлению
        """
        if self.content_type and self.object_pk:
            return self.content_type.get_object_for_this_type(pk=self.object_pk)


class Message(BaseMessageAbstractModel):
    """
    Автоматические уведомления
    """
    subject = models.CharField(u"Заголовок", max_length=255)
    content = models.TextField(u"Сообщение")
    create_date = models.DateTimeField(u"Дата создания", auto_now_add=True)
    no_reply = models.BooleanField(u"No reply", default=False)
    deleted = models.BooleanField(u"Delete", default=False)
    message_recipient = models.ManyToManyField(MessageRecipient)

    class Meta:
        verbose_name = u"Сообщение"
        verbose_name_plural = u"Сообщения"
        ordering = ["create_date"]

    def __unicode__(self):
        return u'%s' % self.subject

    def create_message_from_template(self, template_name, data):
        """
        Создание уведомления из шаблона и данных
        """
        template = u"%s" % render_to_string('messages/' + template_name + '.txt', data)

        from common.simple_parser import SimpleParser
        sp = SimpleParser(template)

        self.subject = sp.get("SUBJECT")
        self.content = sp.get("CONTENT")

    def send_to_companies(self, companies):
        """
        Устаревшее
        """
        for company in companies:
            message_recipient = MessageRecipient(company=company)
            message_recipient.save()
            self.message_recipient.add(message_recipient)

    def send_to_accounts(self, accounts):
        """
        Устаревшее
        """
        for account in accounts:
            message_recipient = MessageRecipient(user=account)
            message_recipient.save()
            self.message_recipient.add(message_recipient)

    def send_to_profiles(self, profiles):
        """
        Привязка сообщения к пользователям
        """
        for profile in profiles:
            message_recipient = MessageRecipient(profile=profile)
            message_recipient.save()
            self.message_recipient.add(message_recipient)
