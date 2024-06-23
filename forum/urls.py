from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'), 
    path('logout/', views.logout_user, name='logout'),
    path('materi-kuliah/', views.materiKuliah, name='materiKuliah'),
    path('get-mata-kuliah/', views.get_mata_kuliah, name='get_mata_kuliah'),
    path('buat-posting/', views.buat_post, name='buatPost'),
    path('materi-kuliah/detail-posting/<int:post_id>/', views.detail_post, name='detailPost'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('delete_comment/', views.delete_comment, name='delete_comment'),
    path('unduh_galeri/<path>', views.unduh_galeri, name='unduh_galeri'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

