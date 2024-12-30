import django_filters
from elements.models import Element

class ElementFilter(django_filters.FilterSet):

    created_date = django_filters.DateFilter(field_name='created_date__date')
    updated_date = django_filters.DateFilter(field_name='updated_date__date')

    class Meta:
        model = Element
        fields = {
            'average_before_normalization': ['exact', 'lt', 'gt'],
            'average_after_normalization': ['exact', 'lt', 'gt'],
            'data_size': ['lt', 'gt','exact'],
            'created_date': ['lt', 'gt', 'exact'],
            'updated_date': ['exact', 'lt', 'gt'],
        }