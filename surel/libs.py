import json, urllib2

from django.utils import simplejson

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