# Generated by Django 3.2.19 on 2023-05-21 15:32

import api.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='uuid',
            field=models.CharField(default=api.utils.generate_uuid, max_length=10, unique=True),
        ),
    ]
