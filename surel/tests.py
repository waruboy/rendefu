"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""




from django.contrib.auth.models import User
from django.test import TestCase

from emailusernames.utils import create_user, create_superuser

from utama.models import Kolega, Organisasi, Status

from .libs import ambil_alamat, cek_pengirim, cek_kolega, tulis_catatan

class SimpleTest(TestCase):

	def setUp(self):
		user = create_superuser('penguji@rendefu.com','passpenguji')
		organisasi = Organisasi.objects.create(nama="Organisasi Uji")
		kolega = Kolega.objects.create(
			nama="Mister Uji", 
			organisasi=organisasi,
			email = "mister_uji@rendefu.com",)
		status = Status.objects.create(user=user, organisasi=organisasi)
	def test_basic_addition(self):
		"""
		Tests that 1 + 1 always equals 2.
		"""
		self.assertEqual(1 + 1, 2)
	
	def test_ambil_alamat(self):
		"""
		Cek parsing email
		"""
		teks = '"Taufiq Muhammadi <taufiq.muhammadi@gmail.com>'
		alamat = ambil_alamat(teks)
		self.assertEqual(alamat, 'taufiq.muhammadi@gmail.com')

	def test_cek_pengirim__berhasil(self):
		user = cek_pengirim('penguji@rendefu.com')
		self.assertEqual(user.username, 'penguji@rendefu.com')

	def test_cek_pengirim__gagal(self):
		user = cek_pengirim('penguji_apa_ini@rendefu.com')
		self.assertEqual(user, [])

	def test_cek_kolega__berhasil(self):
		user = User.objects.all()[0]
		kolega_set = cek_kolega(user, "mister_uji@rendefu.com", "isi_surat")
		nama_kolega = kolega_set[0].nama
		self.assertEqual(nama_kolega, "Mister Uji")

	def test_cek_kolega__gagal(self):
		user = User.objects.all()[0]
		kolega_set = cek_kolega(user, "mister_uji_emisi@rendefu.com", "isi_surat")
		self.assertEqual(kolega_set, [])

	def test_tulis_catatan(self):
		user = User.objects.all()[0]
		kolega = Kolega.objects.all()[0]
		catatan = tulis_catatan(user, kolega, "Judul Email", "Isi Email")
		self.assertEqual(catatan.user.username, "penguji@rendefu.com")



