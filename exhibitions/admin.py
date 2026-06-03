from django.contrib import admin
from .models import Exhibition, ExhibitionComment


class ExhibitionCommentInline(admin.TabularInline):
    model = ExhibitionComment
    extra = 0
    fields = ('author_name', 'rating', 'text', 'is_visible', 'created_at')
    readonly_fields = ('created_at',)
    show_change_link = True


@admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):
    list_display = ('title', 'curator', 'photos_count', 'is_published')
    list_editable = ('photos_count', 'is_published')
    list_filter = ('is_published', 'curator')
    search_fields = ('title', 'description', 'curator__username')
    list_select_related = ('curator',)
    inlines = [ExhibitionCommentInline]


@admin.register(ExhibitionComment)
class ExhibitionCommentAdmin(admin.ModelAdmin):
    list_display = ('exhibition', 'author_name', 'rating', 'is_visible', 'created_at')
    list_editable = ('rating', 'is_visible')
    list_filter = ('rating', 'is_visible', 'created_at')
    search_fields = ('text', 'exhibition__title', 'author_name')
    list_select_related = ('exhibition',)