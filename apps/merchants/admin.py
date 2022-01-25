from django.contrib import admin
from .models import Merchant
from .models import GoogleMerchantCenterAccount
from apps.products.models import Product

# Register your models here.
# admin.site.register(Merchant)

@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    search_fields = ['name', 'source', 'default_google_category__name',]
    list_display = (
        'name',
        'source',
        'feed_name',
        'domain',
        'get_offer_count',
        'default_google_category',
        'approved',
        'active',
        'created',
        'last_updated',
    )

    @admin.display(
        description='Offer Count'
    )
    def get_offer_count(self, obj):
        """gets the offer count for this merchant"""
        offers = Product.objects.filter(
            merchant=obj,
            active=True
        )
        return len(offers)


@admin.register(GoogleMerchantCenterAccount)
class GoogleMerchantCenterAccountAdmin(admin.ModelAdmin):
    search_fields = ['merchant__name', 'merchant__domain', 'account_id']
    list_display = (
        'get_merchant_name',
        'get_merchant_domain',
        'account_id',
        'get_gsa_count',
        'active',
        'created',
        'last_updated',
    )

    @admin.display(
        description='Merchant'
    )
    def get_merchant_name(self, obj):
        return obj.merchant.name

    @admin.display(
        description='Domain'
    )
    def get_merchant_domain(self, obj):
        return obj.merchant.domain

    @admin.display(
        description='GSA Count'
    )
    def get_gsa_count(self, obj):
        """gets the offer count for google_shopping_active"""
        offers = Product.objects.filter(
            merchant=obj.merchant,
            google_shopping_active=True,
            active=True
        )
        return len(offers)