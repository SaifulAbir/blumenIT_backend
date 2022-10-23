# Generated by Django 4.0 on 2022-10-19 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_rename_first_name_user_name_remove_user_last_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTPModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('contact_number', models.CharField(max_length=20, verbose_name='Contact Number')),
                ('otp_number', models.IntegerField(verbose_name='OTP Number')),
                ('verified_phone', models.BooleanField(default=False)),
                ('expired_time', models.DateTimeField(verbose_name='Expired Time')),
            ],
            options={
                'verbose_name': 'OTPModel',
                'verbose_name_plural': 'OTPModels',
                'db_table': 'otp_models',
            },
        ),
        migrations.RemoveField(
            model_name='user',
            name='verified_phone',
        ),
    ]