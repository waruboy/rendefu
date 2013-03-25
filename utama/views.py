import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from emailusernames.utils import create_user

from pengingat.forms import PengingatTambahForm
from pengingat.libs import ambil_pengingat
from surel.isi_email import naskah_bergabung
from surel.libs import kirim_mailgun

from .models import Aktivitas, Organisasi, Kolega, PoinKontak, Status
from .forms import AktivitasTambahForm, AnggotaForm, DaftarForm, DepanForm
from .forms import KolegaTambahForm, KontakTambahForm, KolegaUbahForm
from .libs import sekarang

def ambil_organisasi(kode_organisasi):
	return Organisasi.objects.get(kode = kode_organisasi)

def ambil_kolega(kode_organisasi, kode_kolega):
	organisasi = ambil_organisasi(kode_organisasi)
	kolega = Kolega.objects.get(kode = kode_kolega, organisasi = organisasi)
	return (organisasi, kolega)

def link_kolega(kolega):
	link = '/%s/kolega/%s/' % (kolega.organisasi.kode, kolega.kode)
	return link

def inisiasi_halaman(kode_organisasi, request):
	organisasi = ambil_organisasi(kode_organisasi)
	pengingat = ambil_pengingat(organisasi, request.user)
	form_pengingat = PengingatTambahForm()
	return (organisasi, pengingat, form_pengingat)


@login_required
def anggota_profil(request, kode_organisasi):
	user = request.user
	profil = user.get_profile()
	organisasi = ambil_organisasi(kode_organisasi)
	pengingat = ambil_pengingat(organisasi, request.user)
	if request.method == 'POST':
		form = AnggotaForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			user.email = email
			user.save()
			nama = form.cleaned_data['nama']
			profil.nama = nama
			profil.save()
			return redirect('/' + organisasi.kode + '/')
	else:
		form = AnggotaForm()
		form.email = user.email
	return render (request, 'anggota_profil.jade', {
		'form': form,
		'organisasi': organisasi,
		'pengingat': pengingat,
		'profil': profil,


		})

@login_required
def anggota_tambah(request, kode_organisasi):
	organisasi = ambil_organisasi(kode_organisasi)
	if request.method == 'POST':
		form = AnggotaForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			if User.objects.filter(email=email):
				pesan = 'Email sudah terdaftar'
				return render(request, 'kesalahan.jade', {
					'pesan': pesan, 
					})
			password = 'password'
			user_baru = create_user(email, password)
			nama = form.cleaned_data['nama']
			nama = nama.title()
			profil_baru = user_baru.get_profile()
			profil_baru.nama = nama
			profil_baru.save()
			status_baru = Status.objects.create(user=user_baru, organisasi=organisasi)
			return redirect('/')
		else:
			return HttpResponse('salah')
	else:
		form = AnggotaForm()
	return render(request, 'anggota_tambah.jade',{
		'organisasi': organisasi,
		'form': form,
		})



def daftar(request):
	if request.method == 'POST':
		form = DaftarForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			nama = form.cleaned_data['nama']
			nama = nama.title()
			nama_organisasi = form.cleaned_data['organisasi']
			nama_organisasi = nama_organisasi.title()
			if User.objects.filter(email=email):
				return HttpResponse('Email sudah terdaftar')
			user_baru = create_user(email, password)
			profil_baru = user_baru.get_profile()
			profil_baru.nama = nama
			profil_baru.save()
			organisasi_baru = Organisasi.objects.create(nama=nama_organisasi)
			status_baru = Status.objects.create(user=user_baru, organisasi=organisasi_baru)
			user = authenticate(email=email, password=password)
			naskah = naskah_bergabung(nama, nama_organisasi)
			notifikasi = kirim_mailgun(email, 'Selamat Menggunakan Rendefu', naskah)
			if user.is_active:
				login(request, user)
				return redirect('/'+user.organisasi_set.all()[0].kode)
			return HttpResponseRedirect('/'+pelanggan.get_profile().get_organisasi().kode)
	else:
		return HttpResponseRedirect('/')

def depan(request):
	form_daftar = DaftarForm()
	if request.user.is_authenticated():
		return redirect('/'+request.user.organisasi_set.all()[0].kode)
	if request.method == "POST":
		form = DepanForm(request.POST)
		if form.is_valid():

			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			user = authenticate(email=email, password=password)
			if user:
				if user.is_active:
					login(request, user)
					return redirect('/'+user.organisasi_set.all()[0].kode)
			else:
				return HttpResponse('User/Pass Salah')
	else:
		form = DepanForm()

	return render(request, 'depan.jade',{
		'form': form,
		'form_daftar': form_daftar,
		})
	


@login_required
def aktivitas(request, kode_organisasi, kode_kolega):
	form_pengingat = PengingatTambahForm()
	(organisasi, kolega) = ambil_kolega(kode_organisasi, kode_kolega)
	aktivitas_grup = Aktivitas.objects.filter(kolega=kolega)
	aktivitas_berlangsung_grup = aktivitas_grup.filter(selesai=False)
	aktivitas_selesai_grup = aktivitas_grup.filter(selesai=True)
	user = request.user
	pengingat = ambil_pengingat (organisasi, user)
	return render(request, 'aktivitas.jade', {
		'aktivitas_berlangsung_grup': aktivitas_berlangsung_grup,
		'aktivitas_selesai_grup': aktivitas_selesai_grup,
		'form_pengingat': form_pengingat,
		'kolega': kolega,
		'organisasi': organisasi,
		'pengingat': pengingat,

		})
@login_required
def aktivitas_detail(request, kode_organisasi, kode_kolega, pk_aktivitas):
	(organisasi, kolega) = ambil_kolega(kode_organisasi, kode_kolega)
	aktivitas = Aktivitas.objects.get(pk=pk_aktivitas)
	user = request.user
	pengingat = ambil_pengingat(organisasi, user)
	if request.method == "POST":
		form = KontakTambahForm(request.POST)
		if form.is_valid():
			kontak = form.cleaned_data['kontak']
			kontak_baru = PoinKontak.objects.create(
				kontak = kontak, 
				kolega = kolega,
				user = request.user,
				aktivitas = aktivitas,
				)
			return redirect(request.path)
	else:
		form = KontakTambahForm()
	kontak_grup = PoinKontak.objects.filter(aktivitas = aktivitas)
	form_pengingat = PengingatTambahForm()
	return render(request, 'aktivitas_detail.jade',{
		'organisasi': organisasi,
		'pengingat': pengingat,
		'kontak_grup': kontak_grup,
		'kolega': kolega,
		'form': form,
		'form_pengingat': form_pengingat,
		'aktivitas': aktivitas,
		})


@login_required
def aktivitas_tambah(request, kode_organisasi, kode_kolega):
	(organisasi, kolega) = ambil_kolega(kode_organisasi, kode_kolega)
	if request.method == "POST":
		form = AktivitasTambahForm(request.POST)
		if form.is_valid():
			nama = form.cleaned_data['nama']
			aktivitas_baru = Aktivitas.objects.create(
				nama=nama,
				kolega=kolega,
				)
			return HttpResponse(aktivitas_baru.pk)
		else:
			return HttpResponse('gak valid')

@login_required
def aktivitas_selesai(request, kode_organisasi, kode_kolega, pk_aktivitas):
	if request.method == "POST":
		aktivitas = Aktivitas.objects.get(pk=pk_aktivitas)
		aktivitas.selesai = True
		aktivitas.tanggal_selesai = sekarang()
		aktivitas.save()
		return redirect("/"+kode_organisasi+"/kolega/"+kode_kolega+"/aktivitas/"+pk_aktivitas+"/")
	return HttpResponse('selesaikan aktivitas')
	

@login_required
def organisasi(request, kode_organisasi):
	(organisasi, pengingat, form_pengingat) = inisiasi_halaman(kode_organisasi, request)
	if request.method == "POST":
		form = KolegaTambahForm(request.POST)
		if form.is_valid():
			nama = form.cleaned_data['nama']
			kolega_baru = Kolega.objects.create(
				nama = nama.title(),
				organisasi = organisasi, 
				)
			return redirect(request.path + "kolega/" +kolega_baru.kode)
	else:
		form = KolegaTambahForm()
	kolega_g = organisasi.kolega_set.filter(dihapus=False)
	kolega_baru = kolega_g.order_by('-ditambahkan')[0:9]
	hari_ini = datetime.date.today() +datetime.timedelta(1)

	awal_minggu = hari_ini - datetime.timedelta(7)
	kontak_g = PoinKontak.objects.filter(kolega__in=kolega_g).filter(waktu__range=[awal_minggu, hari_ini]).order_by("-waktu")
	return render(request, 'organisasi.jade', {
		'kolega': kolega_baru,
		'organisasi': organisasi,
		'form': form,
		'form_pengingat': form_pengingat,
		'pengingat': pengingat,
		'kontak_g': kontak_g,
		})

@login_required
def keluar(request):
	logout(request)
	return redirect('/')

@login_required
def kolega(request, kode_organisasi, kode_kolega):
	
	(organisasi, kolega) = ambil_kolega(kode_organisasi, kode_kolega)
	aktivitas_g = Aktivitas.objects.filter(kolega=kolega)
	aktivitas_hidup_g = aktivitas_g.filter(selesai=False)
	form_pengingat = PengingatTambahForm()
	user = request.user
	pengingat = ambil_pengingat(organisasi, user)
	if request.method == "POST":
		form = KontakTambahForm(request.POST)
		if form.is_valid():
			kontak = form.cleaned_data['kontak']
			kontak_baru = PoinKontak.objects.create(
				kontak = kontak, 
				kolega = kolega,
				user = request.user,
				)
			return redirect(request.path)
	else:
		form = KontakTambahForm()
	kontak = kolega.poinkontak_set.all().order_by('-waktu')[0:9]
	form_aktivitas = AktivitasTambahForm()
	return render(request, 'kolega.jade', {
		'kolega': kolega,
		'kontak': kontak,
		'pengingat': pengingat,
		'organisasi': organisasi,
		'form': form,
		'form_aktivitas': form_aktivitas,
		'form_pengingat': form_pengingat,
		'aktivitas_g': aktivitas_g,
		'aktivitas_hidup_g': aktivitas_hidup_g,
		})

@login_required
def kolega_daftar(request, kode_organisasi):
	organisasi = ambil_organisasi(kode_organisasi)
	kolega = Kolega.objects.filter(organisasi=organisasi, dihapus=False).order_by('nama')
	user = request.user
	pengingat = ambil_pengingat(organisasi, user)
	form_pengingat = PengingatTambahForm()
	return render(request, 'kolega_daftar.jade', {
		'form_pengingat': form_pengingat,
		'organisasi': organisasi,
		'pengingat': pengingat,
		'kolega': kolega,

		})

def kolega_tambah(request, kode_organisasi):
	organisasi = ambil_organisasi(kode_organisasi)

	if request.method == "POST":
		form = KolegaTambahForm(request.POST)
		if form.is_valid():
			nama = form.cleaned_data['nama']
			kolega_baru = Kolega.objects.create(
				nama = nama.title(), 
				organisasi = organisasi,
				)
			return HttpResponse(kolega_baru.nama)
	else:
		form = KolegaTambahForm()
	return render(request, 'kolega_tambah.jade', {
		'organisasi': organisasi,
		'form': form,
		})

@login_required
def kolega_ubah(request, kode_organisasi, kode_kolega):
	(organisasi, kolega) = ambil_kolega(kode_organisasi, kode_kolega)
	form_pengingat = PengingatTambahForm()
	user = request.user
	pengingat = ambil_pengingat(organisasi, user)
	if request.method == "POST":
		form = KolegaUbahForm(request.POST, instance=kolega)
		if form.is_valid():
			form.save()
			link = link_kolega(kolega)
			return redirect(link)
	else:
		form = KolegaUbahForm(instance=kolega)
	return render(request, 'kolega_ubah.jade', {
		'kolega': kolega,
		'form': form,
		'form_pengingat': form_pengingat,
		'organisasi': organisasi,
		'pengingat': pengingat,
		})

@login_required
def kolega_hapus(request, kode_organisasi, kode_kolega):
	(organisasi, kolega) = ambil_kolega(kode_organisasi, kode_kolega)
	if request.method == "POST":
		kolega.dihapus = True
		kolega.save()
	link = link_kolega(kolega)
	return redirect('/'+ kode_organisasi +'/')

def kontak_tambah(request, kode_organisasi, kode_kolega):
	(organisasi, kolega) = ambil_kolega(kode_organisasi, kode_kolega)
	if request.method == "POST":
		form = KontakTambahForm(request.POST)
		if form.is_valid():
			kontak = form.cleaned_data['kontak']
			kontak_baru = PoinKontak.objects.create(
				kontak = kontak, 
				kolega = kolega,
				)
			link = link_kolega(kolega)
			return HttpResponse(kontak_baru.kontak)
	form = KontakTambahForm()
	return render(request, 'kontak_tambah.jade', {
		'kolega': kolega,
		'form': form,
		})

def selengkapnya(request):
	return render(request, 'selengkapnya.jade')
