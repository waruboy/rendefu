import json, re, urllib2

from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils import simplejson

from utama.models import Kolega, PoinKontak

from .models import NotifikasiTunda, NotifikasiDikirim

def ambil_alamat(teks):
	alamat = teks[teks.find("<")+1:teks.find(">")]
	return alamat

def kirim_emailyak(judul, isi, tujuan):
	asal = 'jangan_balas@rendefu.com'
	url = 'https://api.emailyak.com/v1/3l3dw99ee1lxfds/json/send/email/'
	data = json.dumps({
		'FromAddress': asal,
		'ToAddress': tujuan,
		'Subject': judul,
		'TextBody': isi,
		})
	req = urllib2.Request(url, data, {'Content-Type': 'application/json; charset=utf-8'})

	try:
		response = urllib2.urlopen(req)

		return response.read()
	except urllib2.HTTPError, error:

		return error.read()

def parse_emailyak(request):
	data = simplejson.loads(request.body)
	pengirim = data['FromAddress']
	penerima = data['ToAddress']
	body_plain = data['TextBody']
	email = {'pengirim': pengirim, 'penerima': penerima, 'body_plain': body_plain}
	return email

def kirim_mailgun(tujuan, judul, isi):
	pengirim = 'jangan_balas@rendefu.mailgun.org'
	kirim = send_mail(judul, isi, pengirim, [tujuan], fail_silently=False)
	return kirim

def cek_pengirim(pengirim):

	user_set = User.objects.filter(email=pengirim)
	if not user_set:
		notif = 'Alamat anda tidak terdaftar sebagai pengguna di rendefu.com'
		NotifikasiTunda.objects.create(
			tujuan=pengirim,
			judul="Terjadi Kesalahan",
			isi=notif,
			)
		return []
	return user_set[0]

def cek_kolega(user, to_address, body_plain):
	organisasi = user.organisasi_set.all()[0]
	email_pengirim = ambil_alamat(to_address)
	kolega_set = organisasi.kolega_set.filter(email=email_pengirim)
	if not kolega_set:
		notif = 'Email %s tidak terdaftar sebagai kolega di %s' % (to_address, organisasi.nama)
		NotifikasiTunda.objects.create(
			tujuan=user.email,
			judul="Terjadi Kesalahan",
			isi=notif,
			)
		return []
	return kolega_set

def tulis_catatan(user, kolega, judul_email, isi_email):
	isi_catatan = "Email \n Judul: %s \n\n %isi_email"
	catatan = PoinKontak.objects.create(
		kontak = isi_catatan,
		kolega = kolega,
		user = user,
		)
	return catatan

def kirim_notifikasi():
	notifikasi_set = NotifikasiTunda.objects.all()
	for notifikasi in notifikasi_set:
		tujuan = notifikasi.tujuan
		judul = notifikasi.judul
		isi = notifikasi.isi
		status = kirim_mailgun(tujuan, judul, isi)
		if status == 1:
			NotifikasiDikirim.objects.create(
				tujuan=tujuan,
				judul=judul,
				isi=isi,
				)
			notifikasi.delete()
	return 'OK'