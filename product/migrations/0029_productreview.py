# Generated by Django 4.0 on 2022-02-23 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_subscription'),
        ('product', '0028_productcategory_cover_productcategory_logo'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('rating_number', models.IntegerField(default=0)),
                ('review_text', models.TextField(default='')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='customer_product_review', to='user.customerprofile')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='product_review', to='product.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_product_review', to='user.user')),
            ],
            options={
                'verbose_name': 'ProductReview',
                'verbose_name_plural': 'ProductReviews',
                'db_table': 'productReview',
            },
        ),
    ]