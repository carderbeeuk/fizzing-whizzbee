from django.db import models
from apps.categories.models import GoogleCategory


SOURCES = (
    ('AWIN', 'awin'),
    ('KELKOO', 'kelkoo'),
)


# Create your models here.
class Merchant(models.Model):
    name = models.CharField(max_length=64)
    source = models.CharField(max_length=32, choices=SOURCES, null=False)
    feed_name = models.CharField(max_length=128)
    feed_url = models.TextField()
    default_google_category = models.ForeignKey(GoogleCategory, on_delete=models.CASCADE, null=True, blank=True)
    approved = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'({self.source}) {self.name} - {self.feed_name}'

    class Meta:
        db_table = 'merchants'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(fields=['name', 'source', 'feed_name'], name='name_source_feed_name')
        ]