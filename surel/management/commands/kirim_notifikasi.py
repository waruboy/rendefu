from django.core.management.base import BaseCommand, CommandError

from surel.libs import kirim_notifikasi

class Command(BaseCommand):
	help = 'Cek dan kirimkan notifikasi yang tertunda'
	def handle(self, *args, **options):
		status = kirim_notifikasi()

		self.stdout.write(status + "\n")