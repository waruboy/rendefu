from .models import Pengingat

def ambil_pengingat(organisasi, user):
	return Pengingat.objects.filter(organisasi=organisasi, user=user, selesai=False)
