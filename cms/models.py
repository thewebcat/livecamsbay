# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models
from main.models import AbstractBaseClass
from ckeditor.fields import RichTextField


class Page(AbstractBaseClass):
    slug = models.SlugField(blank=True, unique=True, null=True, max_length=255)
    title = models.CharField(verbose_name="Заголовок", max_length=255)
    text = RichTextField("Текст страницы")

    def __unicode__(self):
        return u"%s" % self.title
