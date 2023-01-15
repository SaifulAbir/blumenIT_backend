# Generated by Django 4.0 on 2023-01-08 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0032_brand_is_gaming'),
    ]

    operations = [
        migrations.CreateModel(
            name='Warranty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(default='', max_length=800)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Warranty',
                'verbose_name_plural': 'Warranties',
                'db_table': 'warranty',
            },
        ),
        migrations.CreateModel(
            name='ProductWarranty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('warranty_value', models.IntegerField()),
                ('warranty_value_type', models.CharField(choices=[('PERCENTAGE', '%'), ('FIX', 'Fix')], default='PERCENTAGE', max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='product_warranty_product', to='product.product')),
                ('warranty', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='product_warranty_warranty', to='product.warranty')),
            ],
            options={
                'verbose_name': 'ProductWarranty',
                'verbose_name_plural': 'ProductWarranties',
                'db_table': 'product_warranty',
            },
        ),
    ]