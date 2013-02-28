
from django.http import HttpResponse
from django.shortcuts import redirect


from utama.views import ambil_organisasi

from .models import Pengingat
from .forms import PengingatTambahForm

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
	return redirect ("/")

