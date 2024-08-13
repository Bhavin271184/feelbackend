# Generated by Django 5.0.7 on 2024-07-29 15:09

import django.db.models.deletion
import feelapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("feelapp", "0002_haircategory_massagecategory_massageservice_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="BrandAndProduct",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="BrandImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                # (
                #     "image",
                #     models.ImageField(
                #         blank=True,
                #         default="",
                #         null=True,
                #         upload_to=feelapp.models.brand_image_upload_path,
                #     ),
                # ),
                (
                    "brand",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="feelapp.brandandproduct",
                    ),
                ),
            ],
        ),
    ]
