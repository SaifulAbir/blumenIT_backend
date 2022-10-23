# Generated by Django 4.0 on 2022-10-19 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0101_alter_product_vendor'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlashDealInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(default='', max_length=255)),
                ('background_color', models.CharField(default='', max_length=255)),
                ('banner', models.ImageField(blank=True, null=True, upload_to='flash_deal_info')),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'FlashDealInfo',
                'verbose_name_plural': 'FlashDealInfos',
                'db_table': 'flash_deal_info',
            },
        ),
        migrations.CreateModel(
            name='TextColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(default='', max_length=255)),
                ('code', models.CharField(default='', max_length=20)),
            ],
            options={
                'verbose_name': 'TextColor',
                'verbose_name_plural': 'TextColors',
                'db_table': 'text_color',
            },
        ),
        migrations.AlterField(
            model_name='product',
            name='warranty',
            field=models.CharField(blank=True, help_text='eg: 1 year or 6 months', max_length=255, null=True),
        ),
        migrations.CreateModel(
            name='FlashDealProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('discount_amount', models.FloatField(blank=True, default=0, max_length=255, null=True)),
                ('discount_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='flash_deal_product_discount_type', to='product.discounttypes')),
                ('flashDealInfo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='flash_deal_product_flash_deal_info', to='product.flashdealinfo')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='flash_deal_product_product', to='product.product')),
            ],
            options={
                'verbose_name': 'FlashDealProduct',
                'verbose_name_plural': 'FlashDealProducts',
                'db_table': 'flash_deal_product',
            },
        ),
        migrations.AddField(
            model_name='flashdealinfo',
            name='text_color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='flash_deal_info_text_color', to='product.textcolor'),
        ),
    ]