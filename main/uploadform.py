# coding=utf-8
import os

from django import forms
from django.conf import settings
from django.core.files import File

from main.func_image import get_thumb_url


class UploadBase(forms.ModelForm):

    @staticmethod
    def compare_files(old, new):
        if old:
            if new.replace(settings.MEDIA_URL, '').split('?')[0] == old.replace(settings.MEDIA_URL, '').split('?')[0]:
                return True
        return False


class UploadImageFormBase(UploadBase, forms.ModelForm):
    image_label = u'Изображение'

    image = forms.CharField(max_length=255, label=image_label, required=False)

    def __init__(self, *args, **kwargs):
        super(UploadImageFormBase, self).__init__(*args, **kwargs)
        if self.initial.get('image'):
            thumb_url = get_thumb_url(self.initial['image'].path)
            self.initial['image'] = str(self.initial.get('image')) + '?' + thumb_url
        self.file_path = None
        self.allowed_file_extensions = ','.join(settings.IMAGE_EXTENTION.keys())

    def clean_image(self):
        file_name = self.cleaned_data.get('image')
        if self.compare_files(self.initial.get('image'), file_name):
            return
        if file_name:
            self.file_path = os.path.join(settings.MEDIA_ROOT, file_name.split('?')[0].replace(settings.MEDIA_URL, ''))
            return File(open(self.file_path, 'r'))


class UploadAvatarFormBase(UploadBase, forms.ModelForm):
    avatar_label = u'Изображение'

    avatar = forms.CharField(max_length=255, label=avatar_label, required=False)

    def __init__(self, *args, **kwargs):
        super(UploadAvatarFormBase, self).__init__(*args, **kwargs)
        if self.initial.get('avatar'):
            thumb_url = get_thumb_url(self.initial['avatar'].path)
            self.initial['avatar'] = str(self.initial.get('avatar')) + '?' + thumb_url
        self.file_path = None
        self.allowed_file_extensions = ','.join(settings.IMAGE_EXTENTION.keys())

    def clean_avatar(self):
        file_name = self.cleaned_data.get('avatar')
        if self.compare_files(self.initial.get('avatar'), file_name):
            return
        if file_name:
            self.file_path = os.path.join(settings.MEDIA_ROOT, file_name.split('?')[0].replace(settings.MEDIA_URL, ''))
            return File(open(self.file_path, 'r'))


class UploadFileFormBase(UploadBase, forms.ModelForm):
    file_label = u'Файл'

    file = forms.CharField(max_length=255, label=file_label, )

    def __init__(self, *args, **kwargs):
        super(UploadFileFormBase, self).__init__(*args, **kwargs)
        if self.initial.get('file'):
            thumb_url = get_thumb_url(self.initial['file'].path)
            self.initial['file'] = str(self.initial.get('file')) + '?' + thumb_url
        self.file_path = None
        self.allowed_file_extensions = ','.join(settings.IMAGE_EXTENTION.keys() + settings.FILE_EXTENTION.keys())

    def clean_file(self):
        file_name = self.cleaned_data.get('file')
        if self.compare_files(self.initial.get('file'), file_name):
            return
        if file_name:
            self.file_path = os.path.join(settings.MEDIA_ROOT, file_name.split('?')[0].replace(settings.MEDIA_URL, ''))
            return File(open(self.file_path, 'r'))
