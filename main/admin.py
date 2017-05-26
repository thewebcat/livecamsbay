# -*- coding: utf-8 -*-
from django.contrib import admin

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
from .models import AgeTag


# Register your models here.

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


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_name', 'available', 'user', 'date_add')
    list_editable = ('available',)
    list_filter = ('available',)
    search_fields = ['display_name']


@admin.register(AgeTag)
class AgeTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    list_editable = ('name',)
