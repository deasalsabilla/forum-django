# Generated by Django 4.2.5 on 2024-07-04 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0026_rename_sampul_event_pamflet'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='url',
            field=models.URLField(default='https://google.com'),
        ),
    ]