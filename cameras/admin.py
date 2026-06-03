from django.contrib import admin
from .models import CameraBrand, Camera, CameraReview


class CameraInline(admin.TabularInline):
    model = Camera
    extra = 0
    fields = ('name', 'year', 'is_working', 'is_rare')
    show_change_link = True


class CameraReviewInline(admin.TabularInline):
    model = CameraReview
    extra = 0
    fields = ('author_name', 'rating', 'text', 'is_visible', 'created_at')
    readonly_fields = ('created_at',)
    show_change_link = True


@admin.register(CameraBrand)
class CameraBrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'cameras_count')
    search_fields = ('name', 'country')
    inlines = [CameraInline]

    @admin.display(description='Количество камер')
    def cameras_count(self, obj):
        return obj.cameras.count()


@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'year', 'is_working', 'is_rare')
    list_editable = ('year', 'is_working', 'is_rare')
    list_filter = ('brand', 'is_working', 'is_rare', 'year')
    search_fields = ('name', 'description', 'brand__name')
    list_select_related = ('brand',)
    inlines = [CameraReviewInline]


@admin.register(CameraReview)
class CameraReviewAdmin(admin.ModelAdmin):
    list_display = ('camera', 'author_name', 'rating', 'is_visible', 'created_at')
    list_editable = ('rating', 'is_visible')
    list_filter = ('rating', 'is_visible', 'created_at')
    search_fields = ('text', 'camera__name', 'author_name')
    list_select_related = ('camera',)