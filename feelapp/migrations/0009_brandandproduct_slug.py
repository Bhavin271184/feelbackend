# Generated by Django 5.0.7 on 2024-07-31 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("feelapp", "0008_brandandproductmulimage_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="brandandproduct",
            name="slug",
            field=models.SlugField(default="", unique=True),
        ),
    ]
