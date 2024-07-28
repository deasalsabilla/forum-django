from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError


class KatMateri(models.Model):
    id = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name_plural = "Kategori Materi"
        ordering = ['id']


class MataKuliah(models.Model):
    id = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=50)
    semester = models.ForeignKey(KatMateri, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name_plural = "Mata Kuliah"
        ordering = ['id']


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    # Replace 'uploads/' with desired path
    file_upload = models.FileField(blank=True, null=True, upload_to='uploads/')
    judul = models.CharField(max_length=100)
    deskripsi = models.CharField(max_length=100)
    semester = models.ForeignKey(KatMateri, on_delete=models.CASCADE)
    matkul = models.ForeignKey(MataKuliah, on_delete=models.CASCADE)
    pengguna = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.judul

    class Meta:
        verbose_name_plural = "Posting"
        ordering = ['id']


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.judul}'

    class Meta:
        verbose_name_plural = "Comment"


class Proyek(models.Model):
    KATEGORI_CHOICES = [
        ('lomba', 'Lomba'),
        ('pengabdian', 'Pengabdian'),
        ('individu', 'Individu'),
    ]

    STATUS_CHOICES = [
        ('diterima', 'Diterima'),
        ('direview', 'Direview'),
        ('ditolak', 'Ditolak'),
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    sampul = models.ImageField(upload_to='sampul_proyek/')
    judul = models.CharField(max_length=255)
    deskripsi = models.TextField()
    syarat = models.TextField()
    kategori_proyek = models.CharField(max_length=10, choices=KATEGORI_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.judul

    class Meta:
        verbose_name_plural = "Proyek"


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    pamflet = models.ImageField(upload_to='event_covers/')
    judul = models.CharField(max_length=200)
    deskripsi = models.TextField()
    tanggal = models.DateTimeField()
    url = models.URLField(max_length=200, default='https://google.com')

    def __str__(self):
        return self.judul

    class Meta:
        verbose_name_plural = "Event"


def validate_file_extension(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError("Hanya file PDF saja yang diperbolehkan.")


class LamarProyek(models.Model):
    STATUS_CHOICES = [
        ('menunggu', 'Menunggu'),
        ('direview', 'Direview'),
        ('diterima', 'Diterima'),
    ]

    KATEGORI_CHOICES = [
        ('lomba', 'Lomba'),
        ('pengabdian', 'Pengabdian'),
        ('individu', 'Individu'),
    ]
    nama = models.CharField(max_length=100)
    jurusan = models.CharField(max_length=100)
    cv = models.FileField(upload_to='cv/', validators=[validate_file_extension])
    kategori = models.CharField(max_length=10, choices=KATEGORI_CHOICES, null=True, blank=True)
    nama_proyek = models.ForeignKey(Proyek, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='menunggu')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.nama

    class Meta:
        verbose_name_plural = "LamarProyek"
