from django.contrib import admin
from .models import Preset


@admin.register(Preset)
class PresetAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'tone', 'intensity', 'is_public')
    list_editable = ('tone', 'intensity', 'is_public')
    list_filter = ('is_public', 'tone', 'author')
    search_fields = ('title', 'description', 'tone', 'author__username')
    list_select_related = ('author',)