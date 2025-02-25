from django.contrib import admin

from store.models import Category, Product

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    prepopulated_fields = {'slug': ('name',)}
    list_display = [field.name for field in Product._meta.fields]
    list_per_page = 5
    ordering = ['id']
    list_filter = ['price']


admin.site.register(Category)
# admin.site.register(Product, ProductAdmin)
