# Generated by Django 4.0 on 2022-12-18 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support_ticket', '0006_ticket_solution_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='issue_photo',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='solution_photo',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='ticket_description',
        ),
        migrations.AddField(
            model_name='ticketconversation',
            name='conversation_photo',
            field=models.FileField(blank=True, null=True, upload_to='ticket_photo'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_id',
            field=models.SlugField(allow_unicode=True, blank=True, max_length=255),
        ),
    ]
