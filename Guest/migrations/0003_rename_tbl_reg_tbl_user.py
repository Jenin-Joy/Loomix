# Generated by Django 4.2.16 on 2025-01-16 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0004_tbl_brand_rename_tbl_admin_tbl_adminreg_and_more'),
        ('Guest', '0002_rename_reg_district_tbl_reg_reg_contact_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='tbl_reg',
            new_name='tbl_user',
        ),
    ]
