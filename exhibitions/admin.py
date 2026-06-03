from django.contrib import admin
from .models import Exhibition


@admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):
    list_display = ('title', 'curator', 'photos_count', 'is_published')
    list_editable = ('photos_count', 'is_published')
    list_filter = ('is_published', 'curator')
    search_fields = ('title', 'description', 'curator__username')
    list_select_related = ('curator',)