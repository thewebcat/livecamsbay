# -*- coding: UTF-8 -*-
import re
from django import forms

from tags.models import TagCatalog, Tag


class TagCatalogForm(forms.ModelForm):

    action_text = "add_catalog"

    action = forms.CharField(max_length=255, widget=forms.HiddenInput)

    class Meta:
        model = TagCatalog
        fields = ('form_key', 'title', )

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        super(TagCatalogForm, self).__init__(instance=instance, *args, **kwargs)

        self.initial['action'] = self.action_text

    def clean_form_key(self):
        data = self.cleaned_data['form_key']
        if not re.match("^[A-Za-z_]+$", data):
            raise forms.ValidationError("Form key is to consist of [A-Za-z_]+!")

        return data


class TagForm(forms.ModelForm):

    action_text = "add_tag"

    action = forms.CharField(max_length=255, widget=forms.HiddenInput)

    class Meta:
        model = Tag
        fields = ('title', 'tag_catalog',)

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        super(TagForm, self).__init__(instance=instance, *args, **kwargs)

        self.initial['action'] = self.action_text


class MultipleChoiceTagForm(forms.Form):

    tags_label = u'Введите тег'
    tag_titles = []

    tags = forms.MultipleChoiceField(choices=lambda: ((tag.title, tag.title) for tag in Tag.objects.all()),
                                     widget=forms.SelectMultiple(
                                         attrs={
                                             'style': 'width: 100%;',
                                             'placeholder': tags_label
                                         }),
                                     required=False)

    def __init__(self, *args, **kwargs):
        "initial_object - instance with attr 'tags' manytomany"
        # self.fields['city'].choices = ((tag.title, tag.title) for tag in Tag.objects.all())
        if 'initial_object' in kwargs:
            initial_object = kwargs.pop('initial_object')
            if hasattr(initial_object, 'tags'):
                kwargs['initial'] = {'tags': (tag.title for tag in initial_object.tags.all())}
        super(MultipleChoiceTagForm, self).__init__(*args, **kwargs)
        if args and args[0]:
            self.tag_titles = args[0].getlist('tags') if args[0] else []

    def clean(self):
        cleaned_data = super(MultipleChoiceTagForm, self).clean()
        # Подавление ошибок, иначе нельзя добавить новые теги
        if 'tags' in self._errors:
            del self._errors['tags']
        return cleaned_data

    def save(self):
        for tag_title in self.tag_titles:
            tag_title = tag_title.lower()
            try:
                tag = Tag.objects.get(title=tag_title)
            except Tag.DoesNotExist:
                tag = Tag(title=tag_title)
                tag.save()

            yield tag
