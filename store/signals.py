from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from store.models import Category

@receiver(post_save, sender=Category)
@receiver(post_delete, sender=Category)
def clear_category_cache(sender, **kwargs):
    """Clears cached categories when a category is modified."""
    cache.delete("categories_list")
