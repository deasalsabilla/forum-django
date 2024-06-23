from django.shortcuts import render, redirect, get_object_or_404
from .models import KatMateri, MataKuliah, Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.http import JsonResponse
from django.contrib.auth import logout as django_logout
from django.http import HttpResponse, Http404
import os
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def home(request):
    return render(request, 'index.html')

def detail_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'post': post,
    }
    return render(request, 'post-details.html', context)

def proyek_kolaboratif(request):
    return render(request,'proyek-kolaboratif.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')

def logout_user(request):
    django_logout(request)
    return redirect('login')

def materiKuliah(request):
    posts = Post.objects.all()
    kategori_materi = KatMateri.objects.all()
    mata_kuliah = MataKuliah.objects.all()
    context = {
        'posts': posts,
        'kategori_materi': kategori_materi,
        'mata_kuliah': mata_kuliah,
    }
    return render(request, 'materiKuliah.html', context)

def get_mata_kuliah(request):
    semester_id = request.GET.get('semester_id')
    mk_id = request.GET.get('mk_id')

    if semester_id:
        # Jika hanya semester_id yang ada, kembalikan daftar mata kuliah
        mata_kuliah = MataKuliah.objects.filter(semester_id=semester_id).values('id', 'nama')
        return JsonResponse(list(mata_kuliah), safe=False)
    elif mk_id:
        # Jika hanya mk_id yang ada, kembalikan postingan berdasarkan mata kuliah yang dipilih
        posts = Post.objects.filter(matkul_id=mk_id)
        return render(request, 'partials/post_list.html', {'posts': posts})
    else:
        # Jika tidak ada parameter yang diberikan, kembalikan semua postingan
        posts = Post.objects.all()
        return render(request, 'partials/post_list.html', {'posts': posts})
    
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        repeat_password = request.POST['repeat_password']
        if password == repeat_password:
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
            user.save()
            return redirect('login')
        else:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
    else:
        return render(request, 'register.html')
    
@login_required(login_url='/login/')
def buat_post(request):
    if request.method == 'POST':
        judul = request.POST['judul']
        deskripsi = request.POST['deskripsi']
        semester_id = request.POST.get('semester')
        matkul_id = request.POST.get('matakuliah')
        gambar = request.FILES.get('gambar')
        if judul and deskripsi and semester_id and matkul_id:
            try:
                semester = KatMateri.objects.get(id=semester_id)
                matkul = MataKuliah.objects.get(id=matkul_id)
                post = Post(judul=judul, deskripsi=deskripsi, semester=semester, matkul=matkul, pengguna=request.user)
                if gambar:
                    post.gambar = gambar
                post.save()
                return redirect('materiKuliah')
            except (KatMateri.DoesNotExist, MataKuliah.DoesNotExist):
                return render(request, 'error.html', {'error_message': 'Data tidak valid'})
        else:
            return render(request, 'error.html', {'error_message': 'Formulir tidak lengkap'})
    else:
        return render(request, 'buatPosting.html') 

def add_comment(request, post_id):
    if request.method == 'POST':
        comment_content = request.POST.get('comment')
        if comment_content:
            post = get_object_or_404(Post, pk=post_id)
            comment = Comment.objects.create(post=post, user=request.user, content=comment_content, created_at=timezone.now())
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                response = {
                    'success': True,
                    'user': {
                        'username': comment.user.username,
                    },
                    'content': comment.content,
                    'created_at': comment.created_at.strftime('%d %B %Y %H:%M')
                }
                return JsonResponse(response)
    return redirect('detail_post', post_id=post_id)

def unduh_galeri(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
