# Generated by Django 4.2.11 on 2024-04-11 03:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0012_rename_passwd_pengguna_password_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Pengguna',
        ),
    ]