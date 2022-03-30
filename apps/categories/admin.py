from django.contrib import admin
from .models import Category, GoogleCategory

# Register your models here.
# admin.site.register(Category)
# admin.site.register(GoogleCategory)

@admin.register(GoogleCategory)
class GoogleCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name', 'parent_category__name', 'google_category_id',]
    list_display = (
        'name',
        'cardinality',
        'google_category_id',
        'parent_category',
        'active',
    )