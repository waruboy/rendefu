
from django.http import HttpResponse
from django.shortcuts import redirect, render


from utama.views import ambil_organisasi

from .models import Pengingat
from .forms import PengingatDetailForm, PengingatTambahForm
from .libs import ambil_pengingat

def pengingat_detail(request, kode_organisasi, id_pengingat):
	organisasi = ambil_organisasi(kode_organisasi)
	user =  request.user
	pengingat_daftar = ambil_pengingat(organisasi, user)
	pengingat_detail = Pengingat.objects.get(pk = id_pengingat)
	if request.method == "POST":
		form = PengingatDetailForm(request.POST)
		if form.is_valid():
			judul = form.cleaned_data['judul']
			keterangan = form.cleaned_data['keterangan']
			pengingat_detail.judul = judul
			pengingat_detail.keterangan = keterangan
			pengingat_detail.save()
	else:
		form = PengingatDetailForm(instance=pengingat_detail)
	form_pengingat = PengingatTambahForm()

	if pengingat_detail.selesai:
		tombol_selesai = "Aktfikan kembali"
	else:
		tombol_selesai = "Tandai selesai"
	return render (request, 'pengingat_detail.jade' , {
		'form': form,
		'form_pengingat': form_pengingat,
		'organisasi': organisasi,
		'pengingat': pengingat_daftar,
		'pengingat_detail': pengingat_detail,
		'tombol_selesai': tombol_selesai
		})


def pengingat_tambah(request, kode_organisasi):
	if request.method == "POST":
		form = PengingatTambahForm(request.POST)
		organisasi = ambil_organisasi(kode_organisasi)
		if form.is_valid():
			
			judul = form.cleaned_data['judul']
			pengingat_baru = Pengingat.objects.create(
				judul = judul,
				organisasi = organisasi,
				user = request.user,
				)
	return redirect("/" + kode_organisasi + "/")

def pengingat_selesai(request, kode_organisasi, id_pengingat):
	if request.method == "POST":
		pengingat = Pengingat.objects.get(pk = id_pengingat)
		if pengingat.selesai:
			pengingat.selesai = False
		else:
			pengingat.selesai = True
		pengingat.save()
	return redirect("/" + kode_organisasi + "/pengingat/" + id_pengingat)



