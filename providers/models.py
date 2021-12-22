from django.db import models

# Create your models here.
class Provider(models.Model):
    name = models.CharField(max_length=32, unique=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'providers'