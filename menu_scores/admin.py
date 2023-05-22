from django.contrib import admin

from menu_scores.models import MenuScore


class MenuScoreAdmin(admin.ModelAdmin):
    readonly_fields = ['uuid', 'created_at', 'updated_at']


admin.site.register(MenuScore, MenuScoreAdmin)
