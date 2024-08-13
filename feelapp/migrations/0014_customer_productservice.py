# Generated by Django 5.0.4 on 2024-08-08 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("feelapp", "0013_brandandproduct_logo"),
    ]

    operations = [
        migrations.CreateModel(
            name="Customer",
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
                ("is_register", models.BooleanField(default=False)),
                ("mobile_number", models.CharField(max_length=15, unique=True)),
                ("email", models.EmailField(max_length=254)),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("birth_date", models.DateField()),
                ("anniversary_date", models.DateField(blank=True, null=True)),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female")], max_length=1
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductService",
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
                ("product_name", models.CharField(max_length=255)),
                ("service_name", models.CharField(max_length=255)),
                ("product_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("service_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("quantity", models.PositiveIntegerField(default=1)),
                (
                    "subtotal_price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("appointment_date", models.DateField()),
                ("comment", models.TextField(blank=True, null=True)),
            ],
        ),
    ]
