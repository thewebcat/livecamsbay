import django_filters

from .models import Model

class ModelsFilter(django_filters.FilterSet):
    #name = django_filters.CharFilter(lookup_expr='iexact')
    min_price = django_filters.NumberFilter(name="age", lookup_expr='gte')
    max_price = django_filters.NumberFilter(name="age", lookup_expr='lte')
    #speaks_language = django_filters.ModelChoiceFilter(name=

    class Meta:
        model = Model
        fields = [
        	'sex', 'race', 'hair_color', 'bust_size', 'figure', 'speaks_language', 'extra']