from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'), 
    path('logout/', views.logout_user, name='logout'),
    path('materi-kuliah/', views.materiKuliah, name='materiKuliah'),
    path('get-mata-kuliah/', views.get_mata_kuliah, name='get_mata_kuliah'),
    path('buat-posting/', views.buat_post, name='buatPost'),
]
