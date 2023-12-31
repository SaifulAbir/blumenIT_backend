# Generated by Django 4.0 on 2022-11-21 06:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
        ('product', '0002_delete_productmedia'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productreview',
            name='vendor',
        ),
        migrations.AddField(
            model_name='productreview',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='product_review_seller', to='vendor.seller'),
        ),
    ]
