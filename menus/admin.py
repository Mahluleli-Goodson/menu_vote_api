from django.contrib import admin

from menus.models import Menu


class MenuAdmin(admin.ModelAdmin):
    readonly_fields = ['uuid', 'slug', 'created_at', 'updated_at', 'published_for']


admin.site.register(Menu, MenuAdmin)
