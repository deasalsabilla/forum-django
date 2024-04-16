from django.db import models
from django.contrib.auth.models import User

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
        