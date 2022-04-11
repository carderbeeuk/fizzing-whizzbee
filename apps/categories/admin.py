from django.contrib import admin
from .models import Category, GoogleCategory
from apps.products.models import Product

# Register your models here.
# admin.site.register(Category)
# admin.site.register(GoogleCategory)

@admin.register(GoogleCategory)
class GoogleCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name', 'parent_category__name', 'google_category_id',]
    list_display = (
        'name',
        'cardinality',
        'google_category_id',
        'get_offer_count',
        'parent_category',
        'active',
    )

    @admin.display(description='Offer Count')
    def get_offer_count(self, obj):
        """gets the offer count for this merchant"""
        offers = Product.objects.filter(
            google_category_id=obj.google_category_id,
            active=True
        )
        return len(offers)
