# Generated by Django 5.2 on 2025-04-16 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0010_rename_catgeory_tbl_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbl_product',
            name='product_total_price',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
