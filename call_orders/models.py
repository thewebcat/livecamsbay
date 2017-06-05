# coding=utf-8
from django.db import models
from main.models import User


class CallOrder(models.Model):
    """
    Обратный звонок
    """

    STATUS_CALL_LATER = "CL"
    STATUS_NOT_RESPONDING = "AW"
    STATUSES = (
        (STATUS_CALL_LATER, "Call later"),
        (STATUS_NOT_RESPONDING, "Not responding"),
    )

    name = models.CharField(u"User name", max_length=255)
    phone = models.CharField(u"Phone number", max_length=255)
    moderator = models.ForeignKey(User, blank=True, null=True)
    comment = models.TextField(u"Comment")
    status = models.CharField(u"Status", max_length=10, choices=STATUSES)
    creation_date = models.DateTimeField(u"Creation date", auto_now_add=True)
    processing_date = models.DateTimeField(u"Processing date", blank=True, null=True)
    finishing_date = models.DateTimeField(u"Finishing date", blank=True, null=True)

    @property
    def call_order_assign_form(self):
        """
        Получить форму, чтобы назначить себя исполнителем.
        """
        from call_orders.forms import CallOrderAssignForm
        return CallOrderAssignForm(instance=self)

    @property
    def call_order_status(self):
        """
        Текстовое отображение состояния обратного звонка
        """
        if self.finishing_date:
            return "Completed"
        for t in self.STATUSES:
            if t[0] == self.status:
                return t[1]
        return "Ops... call order status not found!"
