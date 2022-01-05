from django.contrib import admin, messages
from django.utils.translation import ngettext
from apps.elasticsearch.models import Index
from lib.elastic_helper import ElasticHelper

# Register your models here.
@admin.register(Index)
class IndexAdmin(admin.ModelAdmin):
    search_fields = ['name', 'provider',]
    actions = ['delete_and_remove_indices',]
    list_display = (
        'name',
        'provider',
        'active',
        'created',
        'last_updated',
    )

    @admin.action(description='Delete selected indices and remove from elasticsearch')
    def delete_and_remove_indices(self, request, queryset):
        for index in queryset:
            helper = ElasticHelper()
            helper.delete_index(index)

        updated = queryset.delete()
        self.message_user(request, ngettext(
            'index was successfully removed.',
            'indices were successfully removed.',
            updated,
        ), messages.SUCCESS)