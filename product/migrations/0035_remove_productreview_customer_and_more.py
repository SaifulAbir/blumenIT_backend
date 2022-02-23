# Generated by Django 4.0 on 2022-02-23 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_subscription'),
        ('product', '0034_productreview_customer_productreview_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productreview',
            name='customer',
        ),
        migrations.AlterField(
            model_name='productreview',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user_review', to='user.user'),
        ),
    ]
