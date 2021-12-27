import uuid
from django.db import models
from apps.categories.models import GoogleCategory
from apps.merchants.models import Merchant


AVAILABILITY_CHOICES = (
    ('IN_STOCK', 'in_stock'),
    ('OUT_OF_STOCK', 'out_of_stock'),
    ('PRE_ORDER', 'pre_order'),
    ('CHECK_SITE', 'check_site'),
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


# Create your models here.
class Product(models.Model):
    product_code = models.CharField(max_length=128)
    product_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    offer_id = models.CharField(max_length=128)
    availability = models.CharField(max_length=32, choices=AVAILABILITY_CHOICES, null=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.CharField(max_length=128)
    publisher = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    price_without_rebate = models.DecimalField(max_digits=11, decimal_places=2)
    month_price = models.DecimalField(max_digits=11, decimal_places=2)
    manufacturer = models.CharField(max_length=128)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    google_category = models.ForeignKey(GoogleCategory, on_delete=models.CASCADE)
    click_out_url = models.TextField()
    merchant_landing_url = models.TextField()
    merchant_mobile_landing_url = models.TextField()
    image_large = models.TextField()
    image_small = models.TextField()
    delivery_time = models.CharField(max_length=32)
    delivery_cost = models.DecimalField(max_digits=11, decimal_places=2)
    discount_percentage = models.IntegerField()
    currency = models.CharField(max_length=8, choices=CURRENCY_CHOICES, default='GBP')
    country = models.CharField(max_length=4, choices=COUNTRY_CHOICES, default='UK')
    features = models.JSONField()
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