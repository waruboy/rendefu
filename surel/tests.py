"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""




from django.contrib.auth.models import User
from django.test import TestCase

from emailusernames.utils import create_user, create_superuser

from utama.models import Kolega, Organisasi, Status

from .libs import ambil_alamat, cek_pengirim, cek_kolega, deteksi_terusan, tulis_catatan
from .isi_email import naskah_bergabung

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

	def test_cek_kolega__dari_kolega_berhasil(self):
		user = User.objects.all()[0]
		isi_surat = "Dari: Mister Uji <mister_uji@rendefu.com>\nIsi surat"
		(kolega_set, status) = cek_kolega(user, 'Mister Uji <mister_uji@rendefu.com>', isi_surat)
		nama_kolega = kolega_set[0].nama
		self.assertEqual(nama_kolega, "Mister Uji")
		self.assertEqual(status, 'dari kolega')

	def test_cek_kolega__from_kolega_berhasil(self):
		user = User.objects.all()[0]
		isi_surat = "From: Mister Uji <mister_uji@rendefu.com>\nIsi surat"
		(kolega_set, status) = cek_kolega(user, 'Mister Uji <mister_uji@rendefu.com>', isi_surat)
		nama_kolega = kolega_set[0].nama
		self.assertEqual(nama_kolega, "Mister Uji")
		self.assertEqual(status, 'dari kolega')

	def test_cek_kolega__untuk_kolega_berhasil(self):
		user = User.objects.all()[0]
		(kolega_set, status) = cek_kolega(user, 'Mister Uji <mister_uji@rendefu.com>', "isi_surat")
		nama_kolega = kolega_set[0].nama
		self.assertEqual(nama_kolega, "Mister Uji")
		self.assertEqual(status, 'untuk kolega')

	def test_cek_kolega__gagal(self):
		user = User.objects.all()[0]
		kolega_set = cek_kolega(user, "mister_uji_emisi@rendefu.com", "isi_surat")
		self.assertEqual(kolega_set, [])

	def test_tulis_catatan__dari_kolega(self):
		user = User.objects.all()[0]
		kolega = Kolega.objects.all()[0]
		catatan = tulis_catatan(user, kolega, "Judul Email", "Isi Email", 'dari kolega')
		isi_catatan = "Email dari kolega:\n%s \n\n%s" % ("Judul Email", "Isi Email")
		self.assertEqual(catatan.user.username, "penguji@rendefu.com")
		self.assertEqual(catatan.kontak, isi_catatan)

	def test_tulis_catatan__untuk_kolega(self):
		user = User.objects.all()[0]
		kolega = Kolega.objects.all()[0]
		catatan = tulis_catatan(user, kolega, "Judul Email", "Isi Email", 'untuk kolega')
		isi_catatan = "Email untuk kolega:\n%s \n\n%s" % ("Judul Email", "Isi Email")
		self.assertEqual(catatan.user.username, "penguji@rendefu.com")
		self.assertEqual(catatan.kontak, isi_catatan)

	def test_deteksi_terusan__gagal(self):
		teks = "kokoww wawaww"
		alamat = deteksi_terusan(teks)
		self.assertEqual(alamat , '')


	def test_deteksi_terusan__from(self):
		teks = "From: Taufiq <taufiq@rendefu.com>"
		alamat = deteksi_terusan(teks)
		self.assertEqual(alamat , 'taufiq@rendefu.com')
		teks = "From: Taufiq <taufiq@rendefu.com> \n Isi email. \n baris kedua"
		alamat = deteksi_terusan(teks)
		self.assertEqual(alamat , 'taufiq@rendefu.com')

	def test_deteksi_terusan__dari(self):
		teks = "Dari: Taufiq <taufiq@rendefu.com>"
		alamat = deteksi_terusan(teks)
		self.assertEqual(alamat , 'taufiq@rendefu.com')
		teks = "Dari: Taufiq <taufiq@rendefu.com> \n Isi email. \n baris kedua"
		alamat = deteksi_terusan(teks)
		self.assertEqual(alamat , 'taufiq@rendefu.com')




class SuaraMasukTest(TestCase):

	def setUp(self):
		user = create_superuser('penguji@rendefu.com','passpenguji')
		organisasi = Organisasi.objects.create(nama="Organisasi Uji")
		kolega = Kolega.objects.create(
			nama="Mister Uji", 
			organisasi=organisasi,
			email = "kolega_uji@rendefu.com",)
		status = Status.objects.create(user=user, organisasi=organisasi)

	def test_get(self):
		"""
		Kalau get harusnya ada pesan aja
		"""
		response = self.client.get('/sistem/kotak_surel/')
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Tempat nerima email")

	def test_post__untuk_kolega(self):
		response = self.client.post('/sistem/kotak_surel/', {
			'sender':'penguji@rendefu.com',
			'recipient':'penerima@email.com',
			'To':'Mister Uji <kolega_uji@rendefu.com>',
			'body-plain':'isi_email',
			})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "untuk kolega")

	def test_post__dari_kolega(self):
		isi_email = "Dari: Kolega Uji <kolega_uji@rendefu.com>\nIsi Surat"
		response = self.client.post('/sistem/kotak_surel/', {
			'sender':'penguji@rendefu.com',
			'recipient':'penerima@email.com',
			'To':'Mister Uji <kolega_uji@rendefu.com>',
			'body-plain':isi_email,
			})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "dari kolega")

class NaskahTest(TestCase):

	def test_naskah_bergabung(self):
		naskah = naskah_bergabung('Pelanggan', 'Organisasi')
		kunci = """Pelanggan,


Selamat bergabung dengan rendefu.com
Alamat email anda sudah terdaftar sebagai administrator Organisasi."""
		self.assertEqual(naskah, kunci)