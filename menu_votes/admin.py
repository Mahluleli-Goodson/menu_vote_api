from django.contrib import admin

from menu_votes.models import MenuVote


class MenuVoteAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at']


admin.site.register(MenuVote, MenuVoteAdmin)
