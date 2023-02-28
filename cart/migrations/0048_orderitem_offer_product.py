# Generated by Django 4.0 on 2023-02-26 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0071_subcategory_is_featured'),
        ('cart', '0047_alter_order_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='offer_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_item_offer_product', to='product.offerproduct'),
        ),
    ]