# Generated by Django 5.0.7 on 2024-07-30 12:02

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("feelapp", "0007_haircategory_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="brandandproductmulimage",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
