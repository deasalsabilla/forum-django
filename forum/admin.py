from django.contrib import admin
from .models import KatMateri, MataKuliah, Post, Comment, Proyek, Event, LamarProyek

admin.site.site_header = "Forum Admin"

@admin.register(KatMateri)
class KatMateriAdmin(admin.ModelAdmin):
    pass

@admin.register(MataKuliah)
class MataKuliahAdmin(admin.ModelAdmin):
    pass
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass

@admin.register(LamarProyek)
class LamarProyekAdmin(admin.ModelAdmin):
    pass

@admin.register(Proyek)
class ProyekAdmin(admin.ModelAdmin):
    list_display = ['judul', 'kategori_proyek', 'status']
    search_fields = ['judul']
    list_filter = ['kategori_proyek', 'status']