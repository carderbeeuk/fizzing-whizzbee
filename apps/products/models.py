import uuid
from django.db import models
from apps.categories.models import GoogleCategory
from apps.merchants.models import Merchant


AVAILABILITY_CHOICES = (
    ('IN_STOCK', 'in_stock'),
    ('OUT_OF_STOCK', 'out_of_stock'),
    ('PRE_ORDER', 'pre_order'),
    ('CHECK_SITE', 'check_site'),
    ('AVAILABLE_ON_ORDER', 'available_on_order'),
    ('STOCK_ON_ORDER', 'stock_on_order'),
)

COUNTRY_CHOICES = (
    ('UK', 'uk'),
    ('US', 'us'),
)

CURRENCY_CHOICES = (
    ('EUR', 'EUR'),
    ('GBP', 'GBP'),
    ('USD', 'USD'),
)

PROVIDERS = (
    ('AWIN', 'awin'),
    ('KELKOO', 'kelkoo'),
)


# Create your models here.
class Product(models.Model):
    product_code = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    product_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    offer_id = models.CharField(max_length=128)
    global_identifier = models.CharField(max_length=128, null=True, blank=True)
    availability = models.CharField(max_length=32, choices=AVAILABILITY_CHOICES, null=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.CharField(max_length=128, null=True, blank=True)
    publisher = models.CharField(max_length=128, null=True, blank=True)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    price_without_rebate = models.DecimalField(max_digits=11, decimal_places=2)
    month_price = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    manufacturer = models.CharField(max_length=128)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    provider = models.CharField(max_length=32, choices=PROVIDERS, null=False)
    google_category = models.ForeignKey(GoogleCategory, on_delete=models.CASCADE)
    condition = models.CharField(max_length=16, default='new', null=True, blank=True)
    click_out_url = models.TextField()
    merchant_landing_url = models.TextField()
    merchant_mobile_landing_url = models.TextField()
    image_large = models.TextField()
    image_small = models.TextField()
    delivery_time = models.CharField(max_length=64, null=True, blank=True)
    google_shopping_delivery = models.CharField(max_length=128, null=True, blank=True)
    delivery_cost = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    discount_percentage = models.IntegerField()
    currency = models.CharField(max_length=8, choices=CURRENCY_CHOICES, default='GBP')
    country = models.CharField(max_length=4, choices=COUNTRY_CHOICES, default='UK')
    google_shopping_active = models.BooleanField(default=False, null=False)
    features = models.JSONField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        ordering = ('title',)
        constraints = [
            models.UniqueConstraint(fields=['title', 'offer_id'], name='title_offer_id')
        ]
        indexes = [
            models.Index(fields=[
                'product_code',
                'product_uuid',
            ]),
        ]