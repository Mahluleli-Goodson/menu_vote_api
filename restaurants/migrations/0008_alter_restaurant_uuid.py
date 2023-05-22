# Generated by Django 3.2.19 on 2023-05-21 13:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0007_alter_restaurant_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('a15987de-9f98-487e-8e9c-3e175177be2b')),
        ),
    ]