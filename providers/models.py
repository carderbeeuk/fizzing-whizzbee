from django.db import models

# Create your models here.
class Provider(models.Model):
    name = models.CharField(max_length=32, unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'providers'