import django_filters

from .models import Model
from .models import Race
from .models import HairColor
from .models import BustSize

class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass

class ModelsFilter(django_filters.FilterSet):
    #name = django_filters.CharFilter(lookup_expr='iexact')
    min_age = django_filters.NumberFilter(name="age", lookup_expr='gte')
    max_age = django_filters.NumberFilter(name="age", lookup_expr='lte')
    race = django_filters.ModelMultipleChoiceFilter(name='race__code', to_field_name='code',
                                                    queryset=Race.objects.all())
    hair_color = django_filters.ModelMultipleChoiceFilter(name='hair_color__code', to_field_name='code',
                                                    queryset=HairColor.objects.all())
    bust_size = django_filters.ModelMultipleChoiceFilter(name='bust_size__code', to_field_name='code',
                                                          queryset=BustSize.objects.all())
    #speaks_language = django_filters.ModelChoiceFilter(name=

    class Meta:
        model = Model
        fields = [
        	'race', 'sex', 'hair_color', 'bust_size', 'figure', 'speaks_language', 'extra']