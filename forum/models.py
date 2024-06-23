from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
    gambar = models.ImageField(blank=True, null=True, upload_to='uploads/')
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
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.judul}'
    class Meta:
        verbose_name_plural = "Comment"