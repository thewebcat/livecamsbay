# -*- coding: UTF-8 -*-
import datetime

from django import forms

from main.fields import SplitPhoneWidget, SplitPhoneField
from main.mixin import MixinForm

from feedback.models import Feedback


class FeedbackForm(MixinForm, forms.ModelForm):

    action_text = "add_feedback"
    messages = {
        'email_or_phone_required': u'Поле Почта или Телефон должно быть заполнено'
    }
    name_label = u'Контактное лицо'
    email_label = u'E-mail'
    phone_label = u'Телефон'
    question_label = u'Ваш вопрос'

    action = forms.CharField(max_length=255, widget=forms.HiddenInput)
    name = forms.CharField(label=name_label, widget=forms.TextInput(attrs={'placeholder': name_label, 'required': True}))
    email = forms.CharField(label=email_label, required=False,
                            widget=forms.TextInput(attrs={'placeholder': email_label}))
    # phone = forms.CharField(label=phone_label, required=False,
    #                         widget=forms.TextInput(attrs={'placeholder': phone_label}))
    phone = SplitPhoneField(label=phone_label, required=False,
                            widget=SplitPhoneWidget(attrs={'placeholder': phone_label, 'required': False}))
    question = forms.CharField(label=question_label, widget=forms.Textarea(attrs={'placeholder': question_label, 'required': True}))

    class Meta:
        model = Feedback
        fields = ('name', 'phone', 'email', 'question', )

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.initial['action'] = self.action_text

    def clean(self):
        cleaned_data = super(FeedbackForm, self).clean()
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone')

        if len(list(set(phone))) == 1 and phone[0] == '':
            if not email:
                self.add_error('email', self.messages['email_or_phone_required'])
                self.add_error('phone', self.messages['email_or_phone_required'])
        return cleaned_data


class FeedbackAssignForm(forms.ModelForm):
    # Форма для принятия в обработку

    action_text = "assigning_feedback"
    action = forms.CharField(max_length=255, widget=forms.HiddenInput)
    id = forms.CharField(max_length=255, widget=forms.HiddenInput)

    class Meta:
        model = Feedback
        fields = ('id', )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(FeedbackAssignForm, self).__init__(*args, **kwargs)

        self.initial['action'] = self.action_text

    def save(self, commit=True):
        feedback = super(FeedbackAssignForm, self).save(commit=False)
        feedback.moderator = self.user
        feedback.processing_date = datetime.datetime.now()
        if commit:
            feedback.save()
        return feedback


class FeedbackProcessingForm(forms.ModelForm):
    # Форма для работы с обратной связью

    action_text = "processing_feedback"
    action = forms.CharField(max_length=255, widget=forms.HiddenInput)

    finished = forms.BooleanField(required=False)

    class Meta:
        model = Feedback
        fields = ('comment',)

    def __init__(self, *args, **kwargs):
        super(FeedbackProcessingForm, self).__init__(*args, **kwargs)

        self.initial['action'] = self.action_text

    def save(self, commit=True):
        feedback = super(FeedbackProcessingForm, self).save(commit=False)
        if self.cleaned_data.get("finished"):
            feedback.finishing_date = datetime.datetime.now()
        if commit:
            feedback.save()
        return feedback
