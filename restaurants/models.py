from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from access_keys.models import AccessKey

from api.utils import generate_uuid, generate_slug


class Restaurant(models.Model):
    access_key = models.OneToOneField(AccessKey, on_delete=models.CASCADE, null=True, blank=True)
    uuid = models.CharField(max_length=10, null=False, blank=False, default=generate_uuid, unique=True)
    label = models.CharField(max_length=100, null=False, blank=False)
    slug = models.CharField(max_length=150, null=False, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self.label)

        self.full_clean()

        if self.pk is None and not self.access_key:
            access_key = AccessKey.objects.create(
                resource_key=generate_uuid(8),
                secret_key=generate_uuid(20),
            )
            self.access_key = access_key
            super().save(*args, **kwargs)

        elif self.pk and self.access_key:  # on update, save everything
            super().save(*args, **kwargs)

    def __str__(self):
        return self.label


@receiver(pre_save, sender=Restaurant)
def restaurant_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = generate_slug(instance.label)
