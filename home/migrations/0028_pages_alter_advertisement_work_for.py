# Generated by Django 4.0 on 2023-05-10 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_aboutus_onlineservicesupport_paymentmethod_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('type', models.CharField(choices=[('INFO', 'Info'), ('CS', 'customer_service')], default='INFO', max_length=30)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
                'db_table': 'pages',
            },
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='work_for',
            field=models.CharField(choices=[('SLIDER', 'slider'), ('SLIDER_SMALL_CAROUSEL', 'slider_small_carousel'), ('SLIDER_SMALL_STATIC', 'slider_small_static'), ('POPULAR_PRODUCT_POSTER', 'popular_product_poster'), ('FEATURED_PRODUCT_POSTER', 'featured_product_poster'), ('OFFER', 'offer')], default='SLIDER', max_length=30),
        ),
    ]
