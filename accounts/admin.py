from django.contrib import admin
from .models import Profile


admin.site.site_header = 'Администрирование AnalogVibe'
admin.site.site_title = 'Админка AnalogVibe'
admin.site.index_title = 'Управление сайтом'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'favorite_style')
    list_editable = ('nickname', 'favorite_style')
    list_filter = ('favorite_style',)
    search_fields = ('nickname', 'bio', 'favorite_style', 'user__username')
    list_select_related = ('user',)