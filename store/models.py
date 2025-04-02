from datetime import timedelta
from io import BytesIO

from autoslug import AutoSlugField
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from PIL import Image
from slugify import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return ''


class Product(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    # slug = models.SlugField(max_length=150, unique=True)
    slug = AutoSlugField(populate_from='name', max_length=100, unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        null=True,
        blank=True,
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, max_length=255)
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

    def resize_image(self, image, size=(600, 600)):
        img = Image.open(image)
        img = img.resize(size, Image.Resampling.LANCZOS)

        ext = image.name.split('.')[-1].lower()
        valid_extensions = {'jpg': 'JPEG', 'jpeg': 'JPEG', 'png': 'PNG', 'gif': 'GIF'}

        if ext not in valid_extensions:
            raise ValueError(f"Unsupported image extension: {ext}")

        thumb_io = BytesIO()
        img.save(thumb_io, format=valid_extensions[ext])
        thumb_io.seek(0)
        image.name = f"{self.slug}.{ext}"  # Optionally set the image name to the slug
        return InMemoryUploadedFile(
            thumb_io,
            None,
            f"{self.slug}.{ext}",  # Keep original extension
            f"image/{ext}",
            thumb_io.tell(),
            None,
        )

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.name)
    #     super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.image:
            self.image = self.resize_image(self.image)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product-info', args=[self.slug])

    @property
    def is_new(self):
        return self.created_at >= now() - timedelta(days=30)
