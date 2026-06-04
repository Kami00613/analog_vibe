from django.contrib import admin

from .models import Exhibition, ExhibitionReview


@admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):
    list_display = ('title', 'curator', 'photos_count', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('title', 'description')


@admin.register(ExhibitionReview)
class ExhibitionReviewAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'exhibition', 'rating', 'created_at', 'is_visible')
    list_filter = ('rating', 'is_visible', 'created_at')
    search_fields = ('author_name', 'text', 'exhibition__title')