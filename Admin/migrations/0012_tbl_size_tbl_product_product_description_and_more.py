# Generated by Django 5.2 on 2025-04-20 08:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0011_tbl_product_product_total_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='tbl_product',
            name='product_description',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='tbl_product',
            name='size',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Admin.tbl_size'),
        ),
    ]
