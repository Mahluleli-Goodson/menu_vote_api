from django.db import models

from api.utils import generate_uuid, generate_slug
from restaurants.models import Restaurant


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)
    uuid = models.CharField(max_length=10, null=False, blank=False, default=generate_uuid, unique=True)
    title = models.CharField(max_length=100, null=False, blank=False)
    slug = models.CharField(max_length=150, null=False, blank=True, unique=True)
    description = models.TextField(null=False, blank=True)
    published_for = models.DateField(auto_now_add=True, null=False, editable=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} | {self.uuid}'
