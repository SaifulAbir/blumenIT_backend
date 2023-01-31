# Generated by Django 4.0 on 2023-01-30 06:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0067_remove_shippingclass_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingclass',
            name='shipping_city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipping_class_shipping_city', to='product.shippingcity'),
        ),
        migrations.AlterField(
            model_name='shippingclass',
            name='shipping_country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipping_class_shipping_country', to='product.shippingcountry'),
        ),
        migrations.AlterField(
            model_name='shippingclass',
            name='shipping_state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipping_class_shipping_state', to='product.shippingstate'),
        ),
    ]