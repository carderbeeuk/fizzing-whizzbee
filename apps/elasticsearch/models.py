from django.db import models

# Create your models here.
class Index(models.Model):
    name = models.CharField(max_length=64)
    provider = models.CharField(max_length=32, null=False)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{name}'

    class Meta:
        db_table = 'indices'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(fields=['name'], name='name')
        ]