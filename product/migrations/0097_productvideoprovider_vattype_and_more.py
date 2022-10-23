# Generated by Django 4.0 on 2022-10-19 06:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0096_productcombinations_product_attribute_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductVideoProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(default='', max_length=800)),
            ],
            options={
                'verbose_name': 'ProductVideoProvider',
                'verbose_name_plural': 'ProductVideoProviders',
                'db_table': 'product_video_provider',
            },
        ),
        migrations.CreateModel(
            name='VatType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(default='', max_length=800)),
            ],
            options={
                'verbose_name': 'VatType',
                'verbose_name_plural': 'VatTypes',
                'db_table': 'vat_type',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='active_short_description',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='bar_code',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='product',
            name='cash_on_delivery',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='digital',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='discount_end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='discount_start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='external_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='external_link_button_text',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='in_house_product',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='low_stock_quantity_warning',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='minimum_purchase_quantity',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='pre_payment_amount',
            field=models.FloatField(default=0, max_length=255),
        ),
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='refundable',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='show_stock_quantity',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='todays_deal',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='vat',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='video_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(default=0, help_text='Unit price', max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='shipping_time',
            field=models.IntegerField(default=0, help_text='eg: Days in count.'),
        ),
        migrations.AddField(
            model_name='product',
            name='video_provider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='product_video_provider', to='product.productvideoprovider'),
        ),
    ]