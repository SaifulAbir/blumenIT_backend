# Generated by Django 4.0 on 2023-01-24 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0047_offercategory_offer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='offer_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Offer_category', to='product.offercategory'),
        ),
    ]