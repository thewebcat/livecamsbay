# -*- coding: UTF-8 -*-

from django import forms

from ckeditor.widgets import CKEditorWidget

from main.forms import AbsUserContentForm
from main.uploadform import UploadImageFormBase

from news.models import News


class NewsForm(AbsUserContentForm, UploadImageFormBase):

    title_label = u'Название новости'
    image_label = u'Изображение к новости'
    short_text_label = u'Анонс - не более 150 слов'
    text_label = u'Текст новости'

    title = forms.CharField(label=title_label, widget=forms.TextInput(attrs={'placeholder': title_label}))
    short_text = forms.CharField(label=short_text_label,
                                 widget=CKEditorWidget(attrs={'placeholder': short_text_label}))
    text = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = News
        fields = ("title", "image", "short_text", "text", "state")

    def save(self, user=None, commit=True):
        news = super(NewsForm, self).save(commit=False)
        if user:
            news.profile = user.profile

        if commit:
            news.save()
        return news
