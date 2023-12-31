# Generated by Django 4.0 on 2022-11-20 04:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vendor', '0001_initial'),
        ('user', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=15)),
                ('coupon_type', models.CharField(max_length=255)),
                ('min_shopping', models.FloatField()),
                ('amount', models.FloatField()),
                ('discount_type', models.CharField(max_length=255)),
                ('number_of_uses', models.IntegerField(default=0)),
                ('start_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Coupon',
                'verbose_name_plural': 'Coupons',
                'db_table': 'coupons',
                'unique_together': {('code',)},
            },
        ),
        migrations.CreateModel(
            name='DeliveryAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(default='', max_length=100)),
                ('address', models.CharField(default='', max_length=100)),
                ('phone', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('email', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('country', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('city', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('zip_code', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('default', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'verbose_name': 'DeliveryAddress',
                'verbose_name_plural': 'DeliveryAddresses',
                'db_table': 'delivery_addresses',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order_id', models.SlugField(allow_unicode=True)),
                ('product_count', models.IntegerField(blank=True, null=True)),
                ('total_price', models.FloatField(default=0, max_length=255)),
                ('order_status', models.CharField(choices=[('PENDING', 'Pending'), ('CONFIRMED', 'Confirmed'), ('PICKED-UP', 'Picked Up'), ('DELIVERED', 'Delivered'), ('RETURN', 'Return'), ('CANCEL', 'Cancel')], default='Confirmed', max_length=20)),
                ('payment_status', models.CharField(choices=[('UN-PAID', 'Un-Paid'), ('PAID', 'Paid')], default='Paid', max_length=20)),
                ('delivery_agent', models.CharField(blank=True, max_length=100, null=True)),
                ('refund', models.BooleanField(default=False)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('coupon_discount_amount', models.FloatField(blank=True, max_length=255, null=True)),
                ('tax_amount', models.FloatField(blank=True, max_length=255, null=True)),
                ('shipping_cost', models.FloatField(blank=True, max_length=255, null=True)),
                ('cash_on_delivery', models.BooleanField(default=False)),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cart.coupon')),
                ('delivery_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.deliveryaddress')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'db_table': 'orders',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('quantity', models.IntegerField(default=1)),
                ('unit_price', models.FloatField(default=0, max_length=255)),
                ('total_price', models.FloatField(default=0, max_length=255)),
                ('is_attribute', models.BooleanField(default=False)),
                ('is_varient', models.BooleanField(default=False)),
                ('attribute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.productattributes')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('variation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='order_items_variation', to='product.productvariation')),
            ],
            options={
                'verbose_name': 'OrderItem',
                'verbose_name_plural': 'OrderItems',
                'db_table': 'order_items',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('charge_id', models.CharField(max_length=50)),
                ('amount', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
                'db_table': 'payments',
            },
        ),
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type_name', models.CharField(max_length=50)),
                ('note', models.TextField(blank=True, default='', null=True)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'PaymentType',
                'verbose_name_plural': 'PaymentTypes',
                'db_table': 'payment_types',
            },
        ),
        migrations.CreateModel(
            name='ShippingType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type_name', models.CharField(max_length=50)),
                ('price', models.FloatField(default=0.0)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'ShippingType',
                'verbose_name_plural': 'ShippingTypes',
                'db_table': 'shipping_types',
            },
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='wishlist_user', to='user.user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VendorOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('vendor_order_id', models.SlugField(allow_unicode=True)),
                ('ordered_date', models.DateTimeField(auto_now_add=True)),
                ('ordered', models.BooleanField(default=True)),
                ('received', models.BooleanField(default=False)),
                ('refund_requested', models.BooleanField(default=False)),
                ('refund_granted', models.BooleanField(default=False)),
                ('order_status', models.CharField(choices=[('PENDING', 'pending'), ('PROCESSING', 'processing'), ('SHIPPED', 'shipped'), ('DELIVERED', 'delivered'), ('RETURN', 'return'), ('CANCEL', 'cancel')], default='processing', max_length=20)),
                ('customer_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vendor_order_customer_profile', to='user.customerprofile')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vendor_order_order', to='cart.order')),
                ('shipping_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vendor_order_shipping_type', to='cart.shippingtype')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vendor_order_user', to='user.user')),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vendor_order_vendor', to='vendor.vendor')),
            ],
            options={
                'verbose_name': 'VendorOrder',
                'verbose_name_plural': 'VendorOrders',
                'db_table': 'vendor_orders',
            },
        ),
        migrations.CreateModel(
            name='UseRecordOfCoupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('coupon_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coupon', to='cart.coupon')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='user.user')),
            ],
            options={
                'verbose_name': 'UseRecordOfCoupon',
                'verbose_name_plural': 'UseRecordOfCoupons',
                'db_table': 'use_record_of_coupon',
            },
        ),
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reason', models.TextField()),
                ('accepted', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=254)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items_refund', to='cart.order')),
            ],
            options={
                'verbose_name': 'Refund',
                'verbose_name_plural': 'Refunds',
                'db_table': 'refunds',
            },
        ),
        migrations.CreateModel(
            name='OrderItemCombination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product_attribute_value', models.CharField(default='', max_length=500)),
                ('product_attribute_price', models.FloatField(blank=True, default=0, max_length=255, null=True)),
                ('variant_value', models.CharField(blank=True, max_length=500, null=True)),
                ('variant_price', models.FloatField(blank=True, default=0, max_length=255, null=True)),
                ('variant_ordered_quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_item_combination_order', to='cart.order')),
                ('orderItem', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_item_combination_order_item', to='cart.orderitem')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_item_combination_product', to='product.product')),
                ('product_attribute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='order_item_combination_product_attributes', to='product.productattributes')),
                ('variant_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='order_item_combination_variant_type', to='product.varianttype')),
            ],
            options={
                'verbose_name': 'OrderItemCombination',
                'verbose_name_plural': 'OrderItemCombinations',
                'db_table': 'order_item_combination',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='payment_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cart.paymenttype'),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.shippingclass'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='order_user', to='user.user'),
        ),
        migrations.AddField(
            model_name='order',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='order_vendor', to='vendor.seller'),
        ),
        migrations.CreateModel(
            name='CustomerAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(default='', max_length=100)),
                ('last_name', models.CharField(default='', max_length=100)),
                ('country', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('company_name', models.CharField(default='', max_length=100)),
                ('street_address', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('city', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('zip_code', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('phone', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('email', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('address_type', models.CharField(default='', max_length=100)),
                ('default', models.BooleanField(default=False)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.order')),
            ],
            options={
                'verbose_name': 'CustomerAddress',
                'verbose_name_plural': 'CustomerAddresses',
                'db_table': 'customer_addresses',
            },
        ),
        migrations.CreateModel(
            name='BillingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(default='', max_length=100)),
                ('last_name', models.CharField(default='', max_length=100)),
                ('country', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('company_name', models.CharField(default='', max_length=100)),
                ('street_address', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('city', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('zip_code', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('phone', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('email', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('address_type', models.CharField(default='', max_length=100)),
                ('title', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('default', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='billing_address_user', to='user.user')),
            ],
            options={
                'verbose_name': 'BillingAddress',
                'verbose_name_plural': 'BillingAddresses',
                'db_table': 'Billing_addresses',
            },
        ),
    ]
