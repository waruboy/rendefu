import datetime
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from utama.models import Organisasi, Kolega, PoinKontak
from utama.forms import DepanForm, KolegaTambahForm, KontakTambahForm, KolegaUbahForm

def depan(request):
	if request.user.is_authenticated():
		return redirect('/'+request.user.organisasi_set.all()[0].kode)
	if request.method == "POST":
		form = DepanForm(request.POST)
		if form.is_valid():

			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			user = authenticate(email=email, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect('/'+user.organisasi_set.all()[0].kode)
			else:
				return HttpResponse('User/Pass Salah')
	else:
		form = DepanForm()

	return render(request, 'depan.jade',{
		'form': form,
		})
	
def ambil_organisasi(kode_organisasi):
	return Organisasi.objects.get(kode = kode_organisasi)

def ambil_kolega(kode_organisasi, kode_kolega):
	organisasi = ambil_organisasi(kode_organisasi)
	kolega = Kolega.objects.get(kode = kode_kolega, organisasi = organisasi)
	return (organisasi, kolega)

def link_kolega(kolega):
	link = '/%s/kolega/%s/' % (kolega.organisasi.kode, kolega.kode)
	return link

def organisasi(request, kode_organisasi):
	organisasi = ambil_organisasi(kode_organisasi)
	if request.method == "POST":
		form = KolegaTambahForm(request.POST)
		if form.is_valid():
			nama = form.cleaned_data['nama']
			kolega_baru = Kolega.objects.create(
				nama = nama,
				organisasi = organisasi, 
				)
			return redirect(request.path + "kolega/" +kolega_baru.kode)
	else:
		form = KolegaTambahForm()
	kolega_g = organisasi.kolega_set.all()
	kolega_baru = kolega_g.order_by('-ditambahkan')[0:9]
	hari_ini = datetime.date.today() +datetime.timedelta(1)

	awal_minggu = hari_ini - datetime.timedelta(7)
	kontak_g = PoinKontak.objects.filter(kolega__in=kolega_g).filter(waktu__range=[awal_minggu, hari_ini]) 
	return render(request, 'organisasi.jade', {
		'kolega': kolega_baru,
		'organisasi': organisasi,
		'form': form,
		'kontak_g': kontak_g,
		})

def kolega(request, kode_organisasi, kode_kolega):
	
	(organisasi, kolega) = ambil_kolega(kode_organisasi, kode_kolega)
	if request.method == "POST":
		form = KontakTambahForm(request.POST)
		if form.is_valid():
			kontak = form.cleaned_data['kontak']
			kontak_baru = PoinKontak.objects.create(
				kontak = kontak, 
				kolega = kolega,
				user = request.user,
				)
			link = link_kolega(kolega)
			return redirect(request.path)
	else:
		form = KontakTambahForm()
	kontak = kolega.poinkontak_set.all()[0:9]
	return render(request, 'kolega.jade', {
		'kolega': kolega,
		'kontak': kontak,
		'organisasi': organisasi,
		'form': form,
		})

def kolega_daftar(request, kode_organisasi):
	organisasi = ambil_organisasi(kode_organisasi)
	kolega = Kolega.objects.filter(organisasi=organisasi)
	return render(request, 'kolega_daftar.jade', {
		'organisasi': organisasi,
		'kolega': kolega,
		})

def kolega_tambah(request, kode_organisasi):
	organisasi = ambil_organisasi(kode_organisasi)
	if request.method == "POST":
		form = KolegaTambahForm(request.POST)
		if form.is_valid():
			nama = form.cleaned_data['nama']
			kolega_baru = Kolega.objects.create(
				nama = nama, 
				organisasi = organisasi,
				)
			return HttpResponse(kolega_baru.nama)
	else:
		form = KolegaTambahForm()
	return render(request, 'kolega_tambah.jade', {
		'organisasi': organisasi,
		'form': form,
		})

def kolega_ubah(request, kode_organisasi, kode_kolega):
	(organisasi, kolega) = ambil_kolega(kode_organisasi, kode_kolega)
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
		})


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
