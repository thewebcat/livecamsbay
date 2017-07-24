# -*- coding: UTF-8 -*-
from django.contrib import admin
from django import forms
from django.forms import TextInput

from tags.models import Tag, TagColor, TagCatalog


class TagCatalogAdmin(admin.ModelAdmin):
    pass


class TagColorForm(forms.ModelForm):
    class Meta:
        model = TagColor
        fields = ('color',)
        widgets = {'color': TextInput(attrs={'type': 'color'})}


class TagColorInline(admin.TabularInline):
    model = TagColor
    form = TagColorForm


class TagAdmin(admin.ModelAdmin):
    list_display = 'title', 'tag_catalog'
    list_editable = 'tag_catalog',
    save_on_top = True
    inlines = [
        TagColorInline,
    ]


admin.site.register(TagCatalog, TagCatalogAdmin)
admin.site.register(Tag, TagAdmin)
