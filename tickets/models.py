# -*- coding: UTF-8 -*-

from __future__ import unicode_literals

from accounts.models import Profile
from django.db import models


class Ticket(models.Model):
    """
    Тикет. Заголовоком тикета является первая запись из tickets.models.Message
    """
    profile = models.ForeignKey(Profile)
    is_active = models.BooleanField(u'активный', default=True)

    class Meta:
        verbose_name = u'тикет'
        verbose_name_plural = u'тикеты'
        ordering = ('-is_active',)

    def __unicode__(self):
        return unicode(self.profile) + '--' + str(self.pk)


class Message(models.Model):
    """
    Сообщения в тикете
    """
    date = models.DateTimeField(u'дата создания', auto_now_add=True)
    text = models.TextField(u'сообщение')
    profile = models.ForeignKey(Profile, null=True, blank=True, related_name='sender')
    ticket = models.ForeignKey(Ticket)
    file = models.FileField(upload_to='ticket', blank=True, null=True)

    class Meta:
        verbose_name = u'сообщение'
        verbose_name_plural = u'сообщения'
        ordering = ('ticket', 'date')

    # def __unicode__(self):
    #     return self.text[:15]
