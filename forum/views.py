from django.shortcuts import render, redirect
from .models import KatMateri, MataKuliah, Post
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.http import JsonResponse
from django.contrib.auth import logout as django_logout

def home(request):
    return render(request, 'index.html')

def materiKuliah(request):
    return render(request, 'materiKuliah.html')

def login_view(request):
    if request.method == 'POST':
        # Ambil data dari form
        username = request.POST['username']
        password = request.POST['password']

        # Authentikasi user
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

#menampilkan sidebarMK diambil dari db
def materiKuliah(request):
    kategori_materi = KatMateri.objects.all()
    mata_kuliah = MataKuliah.objects.all()

    context = {
        'kategori_materi': kategori_materi,
        'mata_kuliah': mata_kuliah,
    }

    return render(request, 'materiKuliah.html', context)

def get_mata_kuliah(request):
    # Ambil ID semester dari permintaan AJAX
    semester_id = request.GET.get('semester_id')
    # Dapatkan mata kuliah yang sesuai dengan ID semester
    mata_kuliah = MataKuliah.objects.filter(semester_id=semester_id)
    # Buat daftar JSON dari mata kuliah yang ditemukan
    mata_kuliah_list = list(mata_kuliah.values('id', 'nama'))
    # Kembalikan respons JSON
    return JsonResponse(mata_kuliah_list, safe=False)


def register(request):
    if request.method == 'POST':
        # Ambil data dari form
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        repeat_password = request.POST['repeat_password']

        # Validasi password
        if password == repeat_password:
            # Buat user baru
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
        judul = request.POST.get('judul')
        deskripsi = request.POST.get('deskripsi')
        semester_id = request.POST.get('semester')
        matkul_id = request.POST.get('matakuliah')
        
        # Periksa apakah semua data diterima dari formulir
        if judul and deskripsi and semester_id and matkul_id:
            # Cari objek Kategori Materi dan Mata Kuliah sesuai dengan ID yang diterima
            try:
                semester = KatMateri.objects.get(id=semester_id)
                matkul = MataKuliah.objects.get(id=matkul_id)
                
                # Simpan data post ke dalam database
                Post.objects.create(
                    judul=judul,
                    deskripsi=deskripsi,
                    semester=semester,
                    matkul=matkul,
                    pengguna=request.user
                )
                
                return redirect('materiKuliah')  # Ganti 'halaman_beranda' dengan nama URL halaman beranda Anda
            except (KatMateri.DoesNotExist, MataKuliah.DoesNotExist):
                # Tangani jika ID tidak valid
                return render(request, 'error.html', {'error_message': 'Data tidak valid'})
        else:
            # Tangani jika formulir tidak lengkap
            return render(request, 'error.html', {'error_message': 'Formulir tidak lengkap'})
    else:
        # Jika bukan request POST, kirimkan formulir kosong
        return render(request, 'buatPosting.html')  # Ganti 'nama_template_form.html' dengan nama template HTML untuk form Anda
    