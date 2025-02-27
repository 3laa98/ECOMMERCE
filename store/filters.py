# filters.py
import django_filters

from store.models import Product


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Product Name')
    min_price = django_filters.NumberFilter(
        field_name='price', lookup_expr='gte', label='Min Price'
    )
    max_price = django_filters.NumberFilter(
        field_name='price', lookup_expr='lte', label='Max Price'
    )

    class Meta:
        model = Product
        fields = ['name', 'min_price', 'max_price']
