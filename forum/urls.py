from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('event/', views.event, name='event'),
    path('event/event-detail/<int:event_id>/',views.event_detail, name='detail-event'),
    path('mypost/edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('myprojects/', views.myprojects, name='myprojects'),
    path('myprojects/proyek-pribadi/',views.proyek_pribadi, name='proyek-pribadi'),
    path('myprojects/proyek-pribadi/pelamar/<int:proyek_id>/',views.proyek_pribadi_detail, name='proyek-pribadi-detail'),
    path('myprojects/proyek-dilamar/', views.proyek_dilamar, name='proyek-dilamar'),
    path('myprojects/proyek-dilamar/delete/<int:pk>/', views.delete_lamar_proyek, name='delete_lamar_proyek'),
    path('mypost/', views.mypost, name='mypost'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('materi-kuliah/', views.materiKuliah, name='materiKuliah'),
    path('get-mata-kuliah/', views.get_mata_kuliah, name='get_mata_kuliah'),
    path('buat-posting/', views.buat_post, name='buatPost'),
    path('materi-kuliah/detail-posting/<int:post_id>/',views.detail_post, name='detailPost'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('delete_comment/', views.delete_comment, name='delete_comment'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('download-file/<path:filename>/',views.download_file, name='download_file'),
    path('proyek-kolaboratif/', views.proyek_kolaboratif,name='proyek-kolaboratif'),
    path('buat-proyek/', views.buat_proyek, name='buat_proyek'),
    path('proyek-detail/<int:proyek_id>/',views.proyek_detail, name='proyek-detail'),
    path('proyek-kolaboratif/bergabung-sekarang/<int:proyek_id>/',views.submit_application, name='submit_application'),
    path('filter_projects/', views.filter_projects, name='filter_projects'),
    path('terima-pelamar/<int:pelamar_id>/', views.terima_pelamar, name='terima_pelamar'),
    path('tolak-pelamar/<int:pelamar_id>/', views.tolak_pelamar, name='tolak_pelamar'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
