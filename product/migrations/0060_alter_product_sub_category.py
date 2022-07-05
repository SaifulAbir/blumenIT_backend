# Generated by Django 4.0 on 2022-07-04 05:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0059_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='product_sub_category', to='product.subcategory'),
        ),
    ]
