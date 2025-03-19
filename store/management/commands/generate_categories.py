from django.core.management.base import BaseCommand
from store.models import Category

class Command(BaseCommand):
    help = "Generate base categories"

    def handle(self, *args, **kwargs):
        categories = [
            "Laptops",
            "Smartphones",
            "Cameras",
            "Accessories",
        ]

        for category_name in categories:
            category, created = Category.objects.get_or_create(name=category_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Category "{category_name}" created.'))
            else:
                self.stdout.write(self.style.WARNING(f'Category "{category_name}" already exists.'))

        self.stdout.write(self.style.SUCCESS("Category generation complete!"))
