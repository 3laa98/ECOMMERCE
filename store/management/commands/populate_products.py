import io
import os
import random

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from faker import Faker

from store.models import Category, Product

fake = Faker()


class Command(BaseCommand):
    help = "Populate the database with fake products"

    def handle(self, *args, **kwargs):
        categories = (
            Category.objects.all()
        )  # Assume you already have some categories in the database

        for category in categories:
            for _ in range(8):
                # category = random.choice(categories) if categories.exists() else None
                image_file = self.get_random_image_from_static(category.name, _)
                product = Product.objects.create(
                    name=fake.word(),
                    category=category,
                    price=random.uniform(10.00, 500.00),
                    description=fake.text(max_nb_chars=100),
                )
                if image_file:
                    product.image.save(
                        image_file.name, image_file
                    )  # Save the open file

                print(f"Created product: {product.name}")
        # self.stdout.write(self.style.SUCCESS("Successfully added fake products!"))

    def get_random_image_from_static(self, category_name, index):

        img_dir = os.path.join(settings.BASE_DIR, 'static', 'img', category_name)

        # List all files in the img directory (only images, e.g., .jpg, .png)
        image_files = [
            f for f in os.listdir(img_dir) if f.endswith(('jpg', 'jpeg', 'png', 'gif'))
        ]

        # If there are images in the directory, return a random one
        if image_files:
            files_number = len(image_files)
            random_image_path = os.path.join(img_dir, image_files[index % files_number])

            # Open the image file and return as a Django File object
            with open(random_image_path, 'rb') as img_file:
                image_content = io.BytesIO(img_file.read())  # Store file in memory
                return File(image_content, name=os.path.basename(random_image_path))
        print("Warning: No images found in media/img!")
        return None
