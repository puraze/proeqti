# Generated by Django 5.1.2 on 2025-04-21 22:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='type',
        ),
    ]
