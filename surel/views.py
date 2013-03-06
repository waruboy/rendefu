from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .libs import parse_emailyak


@csrf_exempt
def suara_masuk(request):
	if request.method == 'POST':
		email = parse_emailyak(request)
		surel_masuk = Surel.objects.create(
			sender = email['pengirim'],
			recipient = email['penerima'],
			body_plain = email['body_plain'],
			)
		respon = proses_surel(surel_masuk)
		return respon
	return HttpResponse('Tempat nerima email')
