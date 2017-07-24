# -*- coding: UTF-8 -*-
from django import forms
from django.core.exceptions import ValidationError

from main.uploadform import UploadFileFormBase
from tickets.models import Message, Ticket


class MessageForm(UploadFileFormBase, forms.ModelForm):

    def __init__(self, profile, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.profile = profile

    ticket = forms.IntegerField(required=False)
    file = forms.CharField(max_length=255, label=u'Файл', required=False)

    class Meta:
        model = Message
        fields = ('text', 'ticket', 'file', 'profile')

    def clean_ticket(self):
        self.ticket = self.cleaned_data.get('ticket')
        if self.ticket and not Ticket.objects.filter(profile=self.profile, id=self.ticket).exists():
            raise ValidationError(u'Нет такого тикета')
        elif not self.ticket:
            return Ticket.objects.create(profile=self.profile)
        else:
            return Ticket.objects.get(id=self.ticket)

    def clean_profile(self):
        return self.profile
