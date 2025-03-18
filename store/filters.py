import django_filters

from store.models import Category, Product


class ProductFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr='icontains')

    # Filter by multiple categories (using checkboxes)
    category = django_filters.ModelMultipleChoiceFilter(
        field_name='category__name',
        to_field_name='name',
        queryset=Category.objects.all(),
        widget=django_filters.widgets.CSVWidget,  # Allows multiple values
    )

    # Filter by price range
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    # Sorting
    sort = django_filters.OrderingFilter(
        fields=(
            ('price', 'price'),  # Sort by price ascending
            # ('-price', 'price_desc'),  # Sort by price descending
            ('name', 'name'),  # Sort by name ascending
            # ('-name', 'name_desc'),  # Sort by name descending
        ),

        field_labels={
            'price': 'Price (Low to High)',
            '-price': 'Price (High to Low)',
            'name': 'Name (A to Z)',
            '-name': 'Name (Z to A)',
        },
    )

    class Meta:
        model = Product
        fields = ['name', 'category', 'min_price', 'max_price', 'sort']

