from django.db import models

# Create your models here.
class Index(models.Model):
    name = models.CharField(max_length=64)
    provider = models.CharField(max_length=32, null=False)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Indices'
        db_table = 'indices'
        ordering = ('-active', '-created')
        constraints = [
            models.UniqueConstraint(fields=['name'], name='name')
        ]