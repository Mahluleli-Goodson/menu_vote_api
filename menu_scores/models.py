from django.db import models

from api.utils import generate_uuid


class MenuScore(models.Model):
    uuid = models.CharField(max_length=10, null=False, blank=False, default=generate_uuid, unique=True)
    label = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.label
