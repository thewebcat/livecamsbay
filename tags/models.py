# -*- coding: UTF-8 -*-

from django.db import models


class TagCatalog(models.Model):
    """
    Деление тегов относящихся к Цвет камня, Наименование камня и Наименование изделия
    """
    FORM_KEY_CHOICES = (
        ('STONE_COLOR', 'Цвет камня'),
        ('NAME_STONE', 'Наименование камня'),
        ('PRODUCT_NAME', 'Наименование изделия')
    )
    form_key = models.CharField(u"Ключ для связи итемов каталога с тегами", max_length=255, unique=True, db_index=True,)
    title = models.CharField(u"Группа тегов", max_length=255)

    def __unicode__(self):
        return u'%s' % self.title


class Tag(models.Model):
    """
    Теги
    """
    tag_catalog = models.ForeignKey(TagCatalog, null=True, blank=True)
    title = models.CharField(u"Название тега", max_length=255)

    certified = models.BooleanField("Certified by the moderator", default=True)

    field_name = "tags"
    field_class = "tag_container"

    class Meta:
        unique_together = ('title', )

    def __unicode__(self):
        return u'%s' % self.title

    @staticmethod
    def instance_update(instance, objs):
        """
        Обновление тегов у переданного материала
        """
        objs = list(objs)
        removed_tags = instance.tags.exclude(id__in=[tag.id for tag in objs])
        instance.tags.remove(*removed_tags)
        instance.tags.add(*objs)

    @staticmethod
    def instance_update_tags(instance, dynamic_fields_list, cleaned_data):
        """
        Устаревшее
        Метод обрабатывает данные которые пришли из формы
        """
        tag_list = []
        for dynamic_field in dynamic_fields_list:
            key = dynamic_field.keys()[0]
            for tag_title in cleaned_data.get(key):
                tag_title = tag_title.lower()
                tag, created = Tag.objects.get_or_create(title=tag_title)
                tag_list.append(tag)
        if tag_list:
            removed_tags = instance.tags.exclude(id__in=[t.id for t in tag_list])
            instance.tags.remove(*removed_tags)
            instance.tags.add(*tag_list)

    @staticmethod
    def instance_append_tags(instance, tag_titles):
        """
        Метод добавляет теги из списка tag_titles
        """
        tag_list = []
        for tag_title in tag_titles:
            tag_title = tag_title.lower()
            try:
                tag = Tag.objects.get(title=tag_title)
            except Tag.DoesNotExist:
                tag = Tag(title=tag_title)
                tag.save()
            tag_list.append(tag)

        if tag_list:
            instance.tags.add(*tag_list)


class TagColor(models.Model):
    """
    Связь тега с цветом
    """
    tag = models.OneToOneField(Tag)
    color = models.CharField("Color", max_length=255)

    def __unicode__(self):
        return u'%s' % self.color
