# -*- coding: UTF-8 -*-
import datetime
from django import forms

from call_orders.models import CallOrder
from common.fields import SplitPhoneField
from common.fields import SplitPhoneWidget


class CallOrderForm(forms.ModelForm):

    action_text = "add_call_order"
    name_label = u'ФИО'
    phone_label = u'Номер телефона'

    action = forms.CharField(max_length=255, widget=forms.HiddenInput)
    name = forms.CharField(label=name_label, required=True,
                           widget=forms.TextInput(attrs={'placeholder': name_label, 'required': True}))
    # phone = forms.CharField(label=phone_label, required=True,
    #                         widget=forms.TextInput(attrs={'placeholder': phone_label, 'required': True}))
    phone = SplitPhoneField(label=phone_label, required=True,
                            widget=SplitPhoneWidget(attrs={'placeholder': phone_label, 'required': True}))

    class Meta:
        model = CallOrder
        fields = ('name', 'phone', )

    def __init__(self, *args, **kwargs):
        super(CallOrderForm, self).__init__(*args, **kwargs)

        self.initial['action'] = self.action_text


class CallOrderAssignForm(forms.ModelForm):
    # Форма для принятия в обработку

    action_text = "assigning_call_order"
    action = forms.CharField(max_length=255, widget=forms.HiddenInput)
    id = forms.CharField(max_length=255, widget=forms.HiddenInput)

    class Meta:
        model = CallOrder
        fields = ('id', )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(CallOrderAssignForm, self).__init__(*args, **kwargs)

        self.initial['action'] = self.action_text

    def save(self, commit=True):
        call_order = super(CallOrderAssignForm, self).save(commit=False)
        call_order.moderator = self.user
        call_order.processing_date = datetime.datetime.now()
        if commit:
            call_order.save()
        return call_order


class CallOrderProcessingForm(forms.ModelForm):
    # Форма для работы со звонком

    action_text = "processing_call_order"
    action = forms.CharField(max_length=255, widget=forms.HiddenInput)

    finished = forms.BooleanField(required=False)

    class Meta:
        model = CallOrder
        fields = ('comment', 'status')

    def __init__(self, *args, **kwargs):
        super(CallOrderProcessingForm, self).__init__(*args, **kwargs)

        self.initial['action'] = self.action_text

    def save(self, commit=True):
        call_order = super(CallOrderProcessingForm, self).save(commit=False)
        if self.cleaned_data.get("finished"):
            call_order.finishing_date = datetime.datetime.now()
        if commit:
            call_order.save()
        return call_order
