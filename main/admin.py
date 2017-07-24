# -*- coding: utf-8 -*-
from django.contrib import admin
from main.emails import content_to_publish

from .models import User
from .models import Sex
from .models import Race
from .models import HairColor
from .models import BustSize
from .models import Figure
from .models import SpeaksLanguage
from .models import PublicArea
from .models import Extra
from .models import CamService
from .models import Model
from .models import CamSnapshot
from .models import AgeTag
from .models import ViewInstance


# Mixins
class MixinSaveModel(object):
    """
    Миксин для оповещения пользователя, что модератор исправил/изменил материал
    """

    @staticmethod
    def _send_private_message(template_name, data, to):
        """
        Формирование автоматического уведомления
        с указанием измененных полей
        """
        if len(data['changes']):
            if not isinstance(to, (list, set)):
                to = [to]
            if len(to) > 0:
                with transaction.atomic():
                    message = Message()
                    message.create_message_from_template(
                        template_name=template_name,
                        data=data)
                    message.save()
                    message.send_to_profiles(profiles=to)

    def save_model(self, request, obj, form, change):
        """
        Метод вызывается при сохранении материала из админки.
        При изменении полей формирует данные для автоматического уведомления
        При публикации оповещает пользователя письмом
        """
        not_notify_fields = {'state', 'tags'}
        form_fields_changed = set(form.changed_data) - not_notify_fields
        super(MixinSaveModel, self).save_model(request, obj, form, change)
        # todo change on first_attr
        profile = getattr(obj, 'profile', None) or getattr(obj, 'customer', None)
        if profile and form_fields_changed:
            self._send_private_message(
                template_name='change_user_content_by_moderator',
                data={
                    'changes': map(lambda x: obj._meta.get_field(x).verbose_name,
                                   filter(lambda x: x not in not_notify_fields, form_fields_changed)),
                    'obj': obj._meta.verbose_name,
                    'url': obj.private_url
                },
                to=profile
            )
        if 'state' in form.changed_data and obj.is_publish() and obj.profile:
            content_to_publish(obj)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_superuser', 'is_staff', 'is_active')
    list_editable = ('is_active',)


@admin.register(Sex)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    list_editable = ('code',)


@admin.register(Race)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    list_editable = ('code',)


@admin.register(HairColor)
class HairColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    list_editable = ('code',)


@admin.register(BustSize)
class BustSizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    list_editable = ('code',)


@admin.register(Figure)
class FigureAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    list_editable = ('code',)


@admin.register(SpeaksLanguage)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    list_editable = ('code',)


@admin.register(PublicArea)
class PublicAreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    list_editable = ('code',)


@admin.register(Extra)
class ExtraAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    list_editable = ('code',)


@admin.register(CamService)
class CamServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'api_url', 'active')
    list_editable = ('api_url',)


class CamSnapshotInline(admin.TabularInline):
    model = CamSnapshot
    extra = 0

@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_name', 'race', 'hair_color', 'available', 'profile', 'date_add')
    list_editable = ('available',)
    list_filter = ('available',)
    search_fields = ['display_name']
    inlines = (CamSnapshotInline,)


@admin.register(AgeTag)
class AgeTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    list_editable = ('name',)

@admin.register(CamSnapshot)
class CamSnapshotAdmin(admin.ModelAdmin):
    list_display = ('snapshot_url', 'model')


@admin.register(ViewInstance)
class ViewInstanceAdmin(admin.ModelAdmin):
    #list_display = ('snapshot_url', 'model')
    pass

