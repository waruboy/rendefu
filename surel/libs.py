import json, re, urllib2

from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils import simplejson

from .models import NotifikasiTunda

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

	user = User.objects.filter(email=pengirim)
	if not user:
		notif = 'Alamat anda tidak terdaftar sebagai pengguna di rendefu.com'
		NotifikasiTunda.objects.create(
			tujuan=pengirim,
			judul="Terjadi Kesalahan",
			isi=notif,
			)
		return notif
	return 'OK'