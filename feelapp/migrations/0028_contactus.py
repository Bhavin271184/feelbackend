# Generated by Django 5.0.2 on 2024-08-30 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feelapp', '0027_alter_services_service_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
            ],
        ),
    ]