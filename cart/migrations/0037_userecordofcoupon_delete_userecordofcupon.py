# Generated by Django 4.0 on 2022-06-22 09:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_subscription'),
        ('cart', '0036_coupon_end_time_coupon_number_of_uses_and_more'),
    ]

    operations = [
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
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='UseRecordOfCupon',
        ),
    ]