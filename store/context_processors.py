from store.models import Category
from django.core.cache import cache

def get_categories(request):

    cache_key = 'categories_list'
    categories = cache.get(cache_key)

    if categories is None:
        categories = Category.objects.all()
        cache.set(cache_key, categories, timeout = 60*15 )

    return {'categories':categories}