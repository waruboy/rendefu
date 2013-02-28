from django.core.management.base import BaseCommand, CommandError

from utama.models import Organisasi

class Command(BaseCommand):
	args = '<organisasi_id organisasi_id ...>'
	help = 'Mengaktifkan akun organisasi yang terdaftar'

	def handle(self, *args, **options):
		for organisasi_id in args:
			try:
				organisasi = Organisasi.objects.get(pk=int(organisasi_id))
			except Organisasi.DoesNotExist:
				raise CommandError('Organisasi ber-id: %s tidak terdaftar' % organisasi_id)

			organisasi.aktif = True
			organisasi.save()

			self.stdout.write('Organisasi ber-id: %s diaktfikan \n' % organisasi_id)