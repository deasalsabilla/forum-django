# Generated by Django 4.2.5 on 2024-07-03 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0025_event'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='sampul',
            new_name='pamflet',
        ),
    ]
