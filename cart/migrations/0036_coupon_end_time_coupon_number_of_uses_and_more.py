# Generated by Django 4.0 on 2022-06-22 09:24

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_subscription'),
        ('cart', '0035_order_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='end_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='coupon',
            name='number_of_uses',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='coupon',
            name='start_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.CreateModel(
            name='UseRecordOfCupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cupon_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coupon', to='cart.coupon')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='user.user')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]