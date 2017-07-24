# coding=utf-8
from django.db import models

from main.models import User


class Feedback(models.Model):
    """
    Обратная связь
    """

    user = models.ForeignKey(User, blank=True, null=True)
    name = models.CharField(u"ФИО", max_length=255)
    phone = models.CharField(u"Телефон", max_length=255)
    email = models.EmailField(u"Email", max_length=255)
    company = models.CharField(u"Компания", max_length=255, blank=True, null=True)
    question = models.TextField(u"Вопрос")
    comment = models.TextField(u"Комментарий")
    creation_date = models.DateTimeField(u"Дата создания", auto_now_add=True)
    processing_date = models.DateTimeField(u"Дата обработки", blank=True, null=True)
    finishing_date = models.DateTimeField(u"Дата окончания", blank=True, null=True)

    @property
    def feedback_assign_form(self):
        """
        Для страницы модератора. Сейчас страница устарела
        """
        from feedback.forms import FeedbackAssignForm
        return FeedbackAssignForm(instance=self)

    @property
    def feedback_status(self):
        """
        Текстовый статус
        """
        if self.finishing_date:
            return u"Завершен"
        elif self.processing_date:
            return u"В работе"
        else:
            return u"Новый"

    class Meta:
        verbose_name = u'Обратная связь'
        verbose_name_plural = u'Обратная связь'

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
