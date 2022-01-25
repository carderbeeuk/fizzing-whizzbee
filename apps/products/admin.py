from django.contrib import admin
from .models import Product


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['title', 'product_uuid', 'product_code', 'offer_id', 'manufacturer', 'merchant__name', 'google_category__name']
    list_display = (
        # 'product_code',
        # 'product_uuid',
        # 'offer_id',
        'title',
        'availability',
        'price',
        'active',
        'google_shopping_active',
        # 'manufacturer',
        'merchant',
        'google_category',
        # 'delivery_cost',
        # 'currency',
        # 'created',
        'last_updated',
    )