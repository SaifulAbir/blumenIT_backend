# Generated by Django 4.0 on 2023-01-24 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0053_remove_offer_offer_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='offer_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Offer_category', to='product.category'),
        ),
    ]