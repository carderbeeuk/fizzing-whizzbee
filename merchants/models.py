from django.db import models
from providers.models import Provider
from categories.models import Category


# Create your models here.
class Merchant(models.Model):
    name = models.CharField(max_length=64)
    source = models.ForeignKey(Provider, on_delete=models.CASCADE)
    feed_name = models.CharField(max_length=128)
    feed_url = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    approved = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'merchants'