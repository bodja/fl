from django.contrib import admin

from file_processing.models import FileModel


@admin.register(FileModel)
class FileModelAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'supplier_id',
        'date',
        'currency',
        'get_processing_status_display',
    ]
