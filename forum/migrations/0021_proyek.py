# Generated by Django 4.2.5 on 2024-07-02 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0020_remove_post_gambar_post_file_upload'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proyek',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sampul', models.ImageField(upload_to='sampul_proyek/')),
                ('judul', models.CharField(max_length=255)),
                ('deskripsi', models.TextField()),
                ('syarat', models.TextField()),
                ('kategori_proyek', models.CharField(choices=[('lomba', 'Lomba'), ('pengabdian', 'Pengabdian'), ('individu', 'Individu')], max_length=10)),
                ('status', models.CharField(choices=[('diterima', 'Diterima'), ('diriview', 'Diriview'), ('ditolak', 'Ditolak')], max_length=10)),
            ],
            options={
                'verbose_name_plural': 'Proyek',
            },
        ),
    ]