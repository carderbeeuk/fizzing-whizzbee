from django.db import models


class GoogleCategory(models.Model):
    """this is assumed to be a source of truth"""
    name = models.CharField(max_length=64)
    cardinality = models.IntegerField()
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    google_category_id = models.IntegerField()
    google_category_full_path = models.TextField()

    class Meta:
        db_table = 'google_categories'


class Category(models.Model):
    """all categories should match up with a google category"""
    name = models.CharField(max_length=64)
    google_category = models.ForeignKey(GoogleCategory, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = 'categories'