from django.db import models
from django.contrib.auth.models import User

from utama.models import Organisasi


class Pengingat(models.Model):
	dibuat = models.DateTimeField(auto_now_add=True)
	judul = models.CharField(max_length=64)
	keterangan = models.TextField(blank=True, null=True)
	selesai = models.BooleanField(default=False)
	user = models.ForeignKey(User)
	organisasi = models.ForeignKey(Organisasi)

	def __unicode__(self):
		return self.judul
