from django.http import HttpResponse
from django.shortcuts import render, redirect
from utama.models import Organisasi, Kolega, PoinKontak
from utama.forms import KolegaTambahForm, KontakTambahForm

def depan(request):
	return render(request, 'dasar.jade')
	
def ambil_organisasi(kode_organisasi):
	return Organisasi.objects.get(kode = kode_organisasi)

def ambil_kolega(kode_organisasi, kode_kolega):
	organisasi = ambil_organisasi(kode_organisasi)
	kolega = Kolega.objects.get(kode = kode_kolega, organisasi = organisasi)
	return (organisasi, kolega)

def link_kolega(kolega):
	link = "/%s/kolega/%s/" % (kolega.organisasi.kode, kolega.kode)

def organisasi(request, kode_organisasi):
	organisasi = ambil_organisasi(kode_organisasi)
	if request.method == "POST":
		form = KolegaTambahForm(request.POST)
		if form.is_valid():
			kontak = form.cleaned_data['kontak']
			kontak_baru = PoinKontak.objects.create(
				kontak = kontak, 
				kolega = kolega,
				)
			link = link_kolega(kolega)
			return redirect(request.path)
	else:
		form = KolegaTambahForm()
	kolega = organisasi.kolega_set.all()[0:9]
	return render(request, 'organisasi.jade', {
		'kolega': kolega,
		'organisasi': organisasi,
		'form': form,
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
				)
			link = link_kolega(kolega)
			return redirect(request.path)
	else:
		form = KontakTambahForm()
	kontak = kolega.poinkontak_set.all()[0:9]
	return render(request, 'kolega.jade', {
		'kolega': kolega,
		'kontak': kontak,
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
