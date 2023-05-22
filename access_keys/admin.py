from django.contrib import admin

from .models import AccessKey


class AccessKeyAdmin(admin.ModelAdmin):
    readonly_fields = ['resource_key', 'secret_key', 'created_at', 'updated_at']

    def get_readonly_fields(self, request, obj=None):
        if obj:  # If obj exists then let it be read-only, otherwise allow adding/creation
            return self.readonly_fields
        return ['created_at', 'updated_at']


admin.site.register(AccessKey, AccessKeyAdmin)
