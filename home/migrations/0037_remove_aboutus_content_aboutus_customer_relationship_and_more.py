# Generated by Django 4.0 on 2023-05-18 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0036_advertisement_image_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aboutus',
            name='content',
        ),
        migrations.AddField(
            model_name='aboutus',
            name='customer_relationship',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='customer_relationship_image',
            field=models.ImageField(default='', upload_to='About_us'),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='footer_text',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='our_goals',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='our_mission',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='our_target_market',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='our_target_market_image',
            field=models.ImageField(default='', upload_to='About_us'),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='our_values',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='our_values_image',
            field=models.ImageField(default='', upload_to='About_us'),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='our_vision',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='retail_wholesale_trade',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='retail_wholesale_trade_image',
            field=models.ImageField(default='', upload_to='About_us'),
        ),
    ]
