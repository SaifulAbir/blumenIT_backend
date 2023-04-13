# Generated by Django 4.0 on 2023-04-13 06:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0078_alter_productfilterattributes_attribute_value_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filterattributes',
            name='attribute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filter_attributes_attribute', to='product.attribute'),
        ),
        migrations.AlterField(
            model_name='filterattributes',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='filter_attributes_category', to='product.category'),
        ),
        migrations.AlterField(
            model_name='filterattributes',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='filter_attributes_sub_category', to='product.subcategory'),
        ),
        migrations.AlterField(
            model_name='filterattributes',
            name='sub_sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='filter_attributes_sub_sub_category', to='product.subsubcategory'),
        ),
    ]
