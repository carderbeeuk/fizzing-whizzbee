from django.contrib import admin
from .models import Category, GoogleCategory

# Register your models here.
# admin.site.register(Category)
# admin.site.register(GoogleCategory)

@admin.register(GoogleCategory)
class GoogleCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'cardinality',
        'parent_category',
        'active',
    )