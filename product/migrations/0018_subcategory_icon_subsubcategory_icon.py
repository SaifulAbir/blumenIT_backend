# Generated by Django 4.0 on 2022-12-18 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0017_subcategory_pc_builder_subsubcategory_pc_builder'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='product_sub_category'),
        ),
        migrations.AddField(
            model_name='subsubcategory',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='product_sub_sub_category'),
        ),
    ]
