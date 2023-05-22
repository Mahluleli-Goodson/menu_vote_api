from django.db import models


class AccessKey(models.Model):
    resource_key = models.CharField(max_length=200, unique=True, null=False, blank=False)
    secret_key = models.CharField(max_length=200, unique=True, null=False, blank=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.resource_key)
