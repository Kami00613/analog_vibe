from django.contrib import admin

from .models import Exhibition, ExhibitionPhoto, ExhibitionReview


class ExhibitionPhotoInline(admin.TabularInline):
    model = ExhibitionPhoto
    extra = 0
    fields = ('position', 'image_path', 'caption')
    ordering = ('position', 'id')


@admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):
    list_display = ('title', 'curator', 'get_photos_count', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('title', 'description')
    inlines = [ExhibitionPhotoInline]

    @admin.display(description='Фото')
    def get_photos_count(self, obj):
        return obj.photos.count()


@admin.register(ExhibitionPhoto)
class ExhibitionPhotoAdmin(admin.ModelAdmin):
    list_display = ('exhibition', 'position', 'image_path', 'caption')
    list_filter = ('exhibition',)
    search_fields = ('exhibition__title', 'image_path', 'caption')
    ordering = ('exhibition', 'position', 'id')


@admin.register(ExhibitionReview)
class ExhibitionReviewAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'exhibition', 'rating', 'created_at', 'is_visible')
    list_filter = ('rating', 'is_visible', 'created_at')
    search_fields = ('author_name', 'text', 'exhibition__title')