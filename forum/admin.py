from django.contrib import admin
from .models import KatMateri, MataKuliah, Post, Comment

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
