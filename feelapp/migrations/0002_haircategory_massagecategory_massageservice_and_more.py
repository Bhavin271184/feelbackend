# Generated by Django 5.0.7 on 2024-07-29 14:12

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("feelapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="HairCategory",
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
            ],
        ),
        migrations.CreateModel(
            name="MassageCategory",
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
                (
                    "type",
                    models.CharField(
                        choices=[("classic", "Classic"), ("executive", "Executive")],
                        max_length=50,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MassageService",
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
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "gender",
                    models.CharField(
                        choices=[("male", "Male"), ("female", "Female")], max_length=10
                    ),
                ),
                ("time", models.DurationField(blank=True, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name="UnisexCategory",
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
                (
                    "choice",
                    models.CharField(
                        choices=[
                            ("makeup", "Makeup"),
                            ("nail art", "Nail Art"),
                            ("skin", "Skin"),
                            ("aesthetic skin care", "Aesthetic Skin Care"),
                            ("package", "Package"),
                        ],
                        max_length=20,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UnisexService",
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
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("gender", models.CharField(max_length=10)),
                ("time", models.DurationField(blank=True, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name="HairService",
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
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("gender", models.CharField(max_length=50)),
                ("time", models.DurationField(blank=True, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="services",
                        to="feelapp.haircategory",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="massagecategory",
            constraint=models.UniqueConstraint(
                fields=("name", "type"), name="unique_name_type"
            ),
        ),
        migrations.AddField(
            model_name="massageservice",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="feelapp.massagecategory",
            ),
        ),
        migrations.AddConstraint(
            model_name="unisexcategory",
            constraint=models.UniqueConstraint(
                fields=("name", "choice"), name="unique_name_choice"
            ),
        ),
        migrations.AddField(
            model_name="unisexservice",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="feelapp.unisexcategory"
            ),
        ),
    ]
