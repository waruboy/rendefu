from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Surel
from .libs import cek_kolega, cek_pengirim


@csrf_exempt
def suara_masuk(request):
	if request.method == 'POST':
		sender    = request.POST.get('sender')
		recipient = request.POST.get('recipient')
		subject   = request.POST.get('subject', '')
		body_plain = request.POST.get('body-plain', '')
		body_without_quotes = request.POST.get('stripped-text', '')
		to = request.POST.get('To','')
		# attachments:
		for key in request.FILES:
			file = request.FILES[key]
		surel_masuk = Surel.objects.create(
			sender = sender,
			recipient = recipient,
			body_plain = body_plain,
			subject =subject,
			to = to,
			)
		user = cek_pengirim(sender)
		if not user:
			return HttpResponse('Pengirim tak dikenal')
		kolega = cek_kolega(user, recipient, body_plain)
		return HttpResponse('OK')
	return HttpResponse('Tempat nerima email')
