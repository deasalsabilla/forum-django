# Generated by Django 4.2.11 on 2024-04-01 06:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_alter_katmateri_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='katmateri',
            name='kode',
        ),
    ]
