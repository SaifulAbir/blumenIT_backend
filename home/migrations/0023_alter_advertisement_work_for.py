# Generated by Django 4.0 on 2023-03-12 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_requestquote_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='work_for',
            field=models.CharField(choices=[('SLIDER', 'slider'), ('SLIDER_SMALL_CAROUSEL', 'slider_small_carousel'), ('SLIDER_SMALL_STATIC', 'slider_small_static'), ('POPULAR_PRODUCT_POSTER', 'popular_product_poster'), ('FEATURED_PRODUCT_POSTER', 'featured_product_poster')], default='SLIDER', max_length=30),
        ),
    ]
