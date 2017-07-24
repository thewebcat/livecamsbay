# -*- coding: UTF-8 -*-
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.db import models
from django.template.loader import render_to_string

from main.func import build_absolute_uri

from email.mime.text import MIMEText
from subprocess import Popen, PIPE
from livecamsbay import settings

from django.core.mail import send_mail as django_send_email


class EmailSender:
    """
    Класс отправки письма
    """

    def __init__(self):
        pass

    subject = ""
    content = ""
    html = None

    def create_message_from_template(self, template_name, data):
        """
        Формарование письма из шаблона и данных
        """

        current_site = get_current_site(None)

        data['site_url'] = build_absolute_uri()
        data['domain'] = current_site.domain
        data['site_name'] = current_site.name
        data['support_url'] = build_absolute_uri(reverse('feedback:feedback'))
        data['unsubscribe_url'] = build_absolute_uri(reverse('accounts:notifications'))

        template = u"%s" % render_to_string('emails/' + template_name + '.html', data)

        from main.simple_parser import SimpleParser
        sp = SimpleParser(template)

        self.subject = sp.get("SUBJECT")
        self.content = sp.get("CONTENT")
        self.html = sp.get("HTML")
        return self

    def send_to(self, email_addresses):
        """
        Отпрака письма
        """
        if not email_addresses:
            return

        if isinstance(email_addresses, basestring):
            email_addresses = [email_addresses]

        if settings.USE_DJANGO_SEND_MAIL:
            django_send_email(self.subject, self.content, settings.DEFAULT_FROM_EMAIL, tuple(email_addresses),
                              html_message=self.html)
        else:
            for email_address in email_addresses:
                EmailSender.send_mail(_from=settings.DEFAULT_FROM_EMAIL, _to=email_address, _subject=self.subject,
                                      _content=self.content)

    @staticmethod
    def send_mail(_from, _to, _subject, _content):
        """
        При настроенном почтовом сервере можно и ьтак отправлять
        """
        msg = MIMEText(_content.encode('utf-8'), 'html', 'utf-8')
        msg["From"] = _from
        msg["To"] = _to
        msg["Subject"] = _subject
        p = Popen(["/usr/sbin/sendmail", "-t"], stdin=PIPE)
        p.communicate(msg.as_string())


class EmailSetting(models.Model):
    """
    Система рассылок.
    """
    GROUPS = ((1, 'Заказ'),
              (2, 'Тикеты'),
              (3, 'Контент'),
              (4, 'Рейтинговая система'),
              (5, 'Рекламная система'),
              (6, 'Оплата аккаунта'),
              (7, 'События в календаре'),
              (8, 'Документооборот'))
    group = models.PositiveSmallIntegerField(choices=GROUPS)
    action = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, blank=True)
    profiles = models.ManyToManyField('accounts.Profile', related_name='email_settings')
    changeable = models.BooleanField(default=True)

    def __unicode__(self):
        return self.description or self.action

    @classmethod
    def group_name(cls, number):
        for g in cls.GROUPS:
            if number == g[0]:
                return g[1]


class EmailGroup(models.Model):
    """
    Доступ к рассылка в зависимости от пользователя.
    Компании и мастеру доступно больше подписок
    """
    COMPANY = 'co'
    PERSON = 'pe'
    TITLES = ((COMPANY, u'компании'),
              (PERSON, u'физическое лицо'))
    title = models.CharField(choices=TITLES, max_length=2)
    settings = models.ManyToManyField(EmailSetting, related_name='email_groups')

    def __unicode__(self):
        for n, v in self.TITLES:
            if n == self.title:
                return v
