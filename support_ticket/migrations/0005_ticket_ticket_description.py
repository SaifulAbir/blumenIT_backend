# Generated by Django 4.0 on 2022-12-18 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support_ticket', '0004_ticket_issue_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='ticket_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]