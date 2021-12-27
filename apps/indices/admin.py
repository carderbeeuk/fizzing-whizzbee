from django.contrib import admin
from .models import Index

# Register your models here.
@admin.register(Index)
class IndexAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = (
        'name',
        'active',
        'created',
        'last_updated',
    )