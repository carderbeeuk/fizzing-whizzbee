from django.contrib import admin
from .models import Merchant
from .models import GoogleMerchantCenterAccount

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
        'default_google_category',
        'approved',
        'active',
        'created',
        'last_updated',
    )


@admin.register(GoogleMerchantCenterAccount)
class GoogleMerchantCenterAccountAdmin(admin.ModelAdmin):
    search_fields = ['merchant__name', 'merchant__domain', 'account_id']
    list_display = (
        'get_merchant_name',
        'get_merchant_domain',
        'account_id',
        'active',
        'created',
        'last_updated',
    )

    def get_merchant_name(self, obj):
        return obj.merchant.name

    def get_merchant_domain(self, obj):
        return obj.merchant.domain