# Generated by Django 4.2.11 on 2024-05-29 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0015_post_delete_posting'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='gambar',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
