from django.contrib import admin
from .models import Restaurant


class RestaurantAdmin(admin.ModelAdmin):
    readonly_fields = ['uuid', 'slug', 'created_at', 'updated_at']


admin.site.register(Restaurant, RestaurantAdmin)
