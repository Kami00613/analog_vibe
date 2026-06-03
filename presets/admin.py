from django.contrib import admin
from .models import Preset, PresetReview


class PresetReviewInline(admin.TabularInline):
    model = PresetReview
    extra = 0
    fields = ('author_name', 'rating', 'text', 'is_visible', 'created_at')
    readonly_fields = ('created_at',)
    show_change_link = True


@admin.register(Preset)
class PresetAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'tone', 'intensity', 'is_public')
    list_editable = ('tone', 'intensity', 'is_public')
    list_filter = ('is_public', 'tone', 'author')
    search_fields = ('title', 'description', 'tone', 'author__username')
    list_select_related = ('author',)
    inlines = [PresetReviewInline]


@admin.register(PresetReview)
class PresetReviewAdmin(admin.ModelAdmin):
    list_display = ('preset', 'author_name', 'rating', 'is_visible', 'created_at')
    list_editable = ('rating', 'is_visible')
    list_filter = ('rating', 'is_visible', 'created_at')
    search_fields = ('text', 'preset__title', 'author_name')
    list_select_related = ('preset',)