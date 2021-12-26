from django.db import models


class GoogleCategory(models.Model):
    """this is assumed to be a source of truth"""
    name = models.CharField(max_length=64)
    cardinality = models.IntegerField()
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    google_category_id = models.IntegerField()
    google_category_full_path = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.google_category_full_path

    class Meta:
        db_table = 'google_categories'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(fields=['name', 'cardinality', 'parent_category_id'], name='name_cardinality_parent_category_id')
        ]


class Category(models.Model):
    """all categories should match up with a google category"""
    name = models.CharField(max_length=64)
    google_category = models.ForeignKey(GoogleCategory, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'