# Generated by Django 4.0 on 2022-10-27 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0136_alter_flashdealinfo_background_color_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flashdealinfo',
            name='text_color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='flash_deal_info_text_color', to='product.textcolor'),
        ),
    ]