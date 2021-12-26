from django.contrib import admin
from .models import Merchant

# Register your models here.
# admin.site.register(Merchant)

@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    search_fields = ['name', 'source', 'default_google_category__name',]
    list_display = (
        'name',
        'source',
        'feed_name',
        'default_google_category',
        'approved',
        'active',
        'created',
        'last_updated'
    )