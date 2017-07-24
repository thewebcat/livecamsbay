# -*- coding: UTF-8 -*-
from django.db import models

from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.files import get_thumbnailer
import os

from accounts.models import Profile
from livecamsbay import settings
from main.models import AbstractBaseClass
from tags.models import Tag


class News(AbstractBaseClass):
    """
    Модель новости
    """
    title = models.CharField(u"Заголовок", max_length=255)
    short_text = models.TextField(u"Анонс")
    text = models.TextField(u"Текст")
    image = ThumbnailerImageField(u"Изображение", upload_to="news_images", null=True, blank=True)
    # create_date = models.DateTimeField(u"Create date", auto_now_add=True)
    public = models.BooleanField(u"Is public news?", default=False)
    profile = models.ForeignKey(Profile, null=True, blank=True)

    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        verbose_name = u"Новость"
        verbose_name_plural = u"Новости"
        ordering = ["-date_add"]

    def __unicode__(self):
        return u'%s' % self.title

    def get_image(self):
        """
        Получение главной картинки для новости
        """
        if self.image and os.path.exists(self.image.path):
            return self.image
        else:
            return get_thumbnailer(open(settings.DEFAULT_IMAGE), relative_name='default.png')

    @models.permalink
    def get_absolute_url(self):
        """
        Устаревшее
        """
        return 'news:news_view', (), {'news_id': self.id}

    @models.permalink
    def private_edit_url(self):
        """
        Устаревшее
        """
        return 'accounts:news_edit', (), {'object_id': self.id}

    def get_seo_title(self):
        # try:
        #     if self.meta.title:
        #         return self.meta.title
        # except models.ObjectDoesNotExist:
        #     pass

        try:
            if self.profile:
                return u'{0} | компания {1} | Amigostone'.format(self.title, self.profile.name)
            else:
                return u'{0} | Amigostone'.format(self.title)
        except AttributeError:
            return ''

    def get_seo_keywords(self):
        # try:
        #     if self.seo.keywords:
        #         return self.seo.keywords
        # except models.ObjectDoesNotExist:
        #     pass
        # if self.provider and self.stoneworker:
        #     company_role = u'производство изделий из камня и поставки'
        # elif self.provider:
        #     company_role = u'производитель изделий из камня'
        # elif self.stoneworker:
        #     company_role = u'поставщик каменной отрасли'

        try:
            if self.profile:
                return u'{0}, компания {1}, Amigostone онлайн биржа'.format(self.title, self.profile.name)
            else:
                return u'{0}, Amigostone онлайн биржа'.format(self.title)
        except AttributeError:
            return ''

    def get_seo_description(self):
        # try:
        #     if self.seo.description:
        #         return self.seo.description
        # except models.ObjectDoesNotExist:
        #     pass
        # if self.provider and self.stoneworker:
        #     company_role = u'производство изделий из камня и поставки'
        # elif self.provider:
        #     company_role = u'производитель изделий из камня'
        # elif self.stoneworker:
        #     company_role = u'поставщик каменной отрасли'

        try:
            if self.profile:
                return u'{0} | компания {1} | Amigostone'.format(self.title, self.profile.name)
            else:
                return u'{0} | Amigostone'.format(self.title)
        except AttributeError:
            return ''