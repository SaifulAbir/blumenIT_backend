# Generated by Django 4.0 on 2022-01-05 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_remove_product_category_remove_product_colors_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productcategory',
            name='product',
        ),
        migrations.AddField(
            model_name='product',
            name='product_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='product.productcategory'),
        ),
    ]
