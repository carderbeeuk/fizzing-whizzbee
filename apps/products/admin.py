from django.contrib import admin
from .models import Product


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['title', 'product_uuid', 'product_code', 'offer_id', 'manufacturer', 'merchant__name', 'google_category__name']
    actions = ['toggle_active_inactive_state', 'toggle_gsa_state']
    list_display = (
        # 'product_code',
        # 'product_uuid',
        # 'offer_id',
        'title',
        'availability',
        'global_identifier',
        'price',
        'active',
        'get_gsa',
        'get_shipping',
        # 'manufacturer',
        'merchant',
        # 'google_category',
        # 'delivery_cost',
        # 'currency',
        # 'created',
        'last_updated',
    )

    @admin.display(
        description='Shipping'
    )
    def get_shipping(self, obj):
        return obj.google_shopping_delivery

    @admin.display(
        description='GSA',
        ordering='-google_shopping_active',
        boolean=True
    )
    def get_gsa(self, obj):
        return obj.google_shopping_active == True

    @admin.action(
        description='Toogle active/inactive state'
    )
    def toggle_active_inactive_state(self, request, queryset):
        for product in queryset:
            product.active = not product.active
            product.save()

    @admin.action(
        description='Toggle GSA state'
    )
    def toggle_gsa_state(self, request, queryset):
        for product in queryset:
            product.google_shopping_active = not product.google_shopping_active
            product.save()