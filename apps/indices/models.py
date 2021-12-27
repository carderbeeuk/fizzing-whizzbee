from django.db import models

# Create your models here.
class Index(models.Model):
    name = models.CharField(max_length=64, unique=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'indices'
        ordering = ('created',)