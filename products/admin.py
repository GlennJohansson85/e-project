from django.contrib import admin
from. models import Product, Category

# Register your models here.
# Classes below will extend the built in model admin class. The order is how it will be displayed on admin dashboard.


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )
    
    ordering = ('sku',) # sort the products by SKU using the ordering attribute.

    
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)