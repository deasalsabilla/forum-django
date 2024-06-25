from django.shortcuts import render, redirect, get_object_or_404
from .models import KatMateri, MataKuliah, Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.http import JsonResponse
from django.contrib.auth import logout as django_logout
from django.http import HttpResponse, Http404
import os
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

@login_required(login_url='/login/')
def mypost(request):
    posts = Post.objects.filter(pengguna=request.user)
    context = {
        'posts': posts,
    }
    return render(request, 'mypost.html', context)


def detail_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'post': post,
    }
    return render(request, 'post-details.html', context)

def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    edit_success = request.session.pop('edit_success', False)  # Get and remove the flag from session

    if request.method == 'POST':
        try:
            # Check if a new image is uploaded
            if 'gambar' in request.FILES:
                post.gambar = request.FILES['gambar']

            # Update judul and deskripsi
            post.judul = request.POST.get('judul', post.judul)
            post.deskripsi = request.POST.get('deskripsi', post.deskripsi)

            post.save()

            # Set a flag or variable to indicate success
            request.session['edit_success'] = True
            return redirect('edit_post', post_id=post.id)
        except Exception as e:
            # Optionally, handle specific exceptions here if needed
            print(f'Gagal mengubah data. Kesalahan: {e}')
            messages.error(request, f'Gagal mengubah data. Kesalahan: {e}')
            return redirect('edit_post', post_id=post.id)

    return render(request, 'edit.html', {'post': post, 'edit_success': edit_success})

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
    posts_list = Post.objects.all()
    paginator = Paginator(posts_list, 5)  # Show 5 posts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

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
                request.session['create_success'] = True  # Set success flag
                return redirect('materiKuliah')  # Redirect to the same view to display the success message
            except (KatMateri.DoesNotExist, MataKuliah.DoesNotExist):
                return render(request, 'error.html', {'error_message': 'Data tidak valid'})
        else:
            return render(request, 'error.html', {'error_message': 'Formulir tidak lengkap'})
    else:
        create_success = request.session.pop('create_success', False)  # Retrieve and remove the flag from the session
        return render(request, 'buatPosting.html', {
            'kategori_materi': KatMateri.objects.all(),
            'create_success': create_success
        })        
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

@require_POST
def delete_comment(request):
    comment_id = request.POST.get('comment_id')
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    post_id = comment.post.id
    comment.delete()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    return redirect('detail_post', post_id=post_id)

@require_POST
@login_required
def delete_post(request, post_id):
    try:
        post = get_object_or_404(Post, id=post_id, pengguna=request.user)
        post.delete()
        return JsonResponse({'success': True})
    except Post.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Post does not exist'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

def unduh_galeri(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
