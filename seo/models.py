# -*- coding: utf-8 -*-

from django.db import models
from django.core.validators import MaxLengthValidator

from annoying.functions import get_object_or_None

#from utils import get_first_object_or_None


__all__ = (
    'Rule',
)

def _get_queryset(model_or_queryset, *qs, **query):
    if hasattr(model_or_queryset, 'objects'):
        return model_or_queryset.objects.filter(*qs, **query)
    else:
        return model_or_queryset.filter(*qs, **query)

def get_first_object_or_None(model_or_queryset, *qs, **query):
    queryset = _get_queryset(model_or_queryset, *qs, **query)
    try:
        return queryset[0]
    except IndexError:
        return None

class Rule(models.Model):
    TYPE_MATCH = 0
    TYPE_STARTSWITH = 1
    TYPE_ENDSWITH = 2
    TYPE_CONTAINS = 3

    TYPE_CHOICES = (
        (TYPE_MATCH, u'совпадение'),
        (TYPE_STARTSWITH, u'начинается с'),
        (TYPE_ENDSWITH, u'заканчивается на'),
        (TYPE_CONTAINS, u'содержит'),
    )

    TITLE_MAX_LENGTH = 150
    KEYWORDS_MAX_LENGTH = 250
    DESCRIPTION_MAX_LENGTH = 200
    TITLE_HINT = str(TITLE_MAX_LENGTH)+u' символов максимум.'
    KEYWORDS_HINT = str(KEYWORDS_MAX_LENGTH)+u' символов максимум.'
    DESCRIPTION_HINT = str(DESCRIPTION_MAX_LENGTH)+u' символов максимум.'

    rtype = models.IntegerField(u'тип', choices=TYPE_CHOICES)
    pattern = models.TextField(u'паттерн')
    title = models.TextField(u'<title>', blank=True, validators=[MaxLengthValidator(TITLE_MAX_LENGTH)], help_text=TITLE_HINT)
    keywords = models.TextField(u'<meta name="keywords">', blank=True, validators=[MaxLengthValidator(KEYWORDS_MAX_LENGTH)], help_text=KEYWORDS_HINT)
    description = models.TextField(u'<meta name="description">', blank=True, validators=[MaxLengthValidator(DESCRIPTION_MAX_LENGTH)], help_text=DESCRIPTION_HINT)
    enabled = models.BooleanField(u'работает', default=True)

    def __unicode__(self):
        return self.pattern

    @classmethod
    def find(cls, request):
        for rtype in dict(cls.TYPE_CHOICES):
            if rtype == cls.TYPE_MATCH:
                rule = get_first_object_or_None(cls, rtype=cls.TYPE_MATCH, pattern=request.path, enabled=True)
                if rule: return rule
            else:
                guesses = (
                    (cls.TYPE_STARTSWITH, lambda pattern: request.path.startswith(pattern)),
                    (cls.TYPE_ENDSWITH, lambda pattern: request.path.endswith(pattern)),
                    (cls.TYPE_CONTAINS, lambda pattern: pattern in request.path),
                )
                for rtype, test in guesses:
                    candidates = cls.objects.filter(rtype=rtype, enabled=True)
                    for rule in candidates:
                        if test(rule.pattern): return rule

    class Meta:
        verbose_name = u'правило'
        verbose_name_plural = u'правила'


