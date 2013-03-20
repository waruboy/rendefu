from django.db import models

class Surel(models.Model):
    sender = models.TextField()
    recipient = models.TextField()
    body_plain = models.TextField()
    diterima = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return str(self.diterima) + " " + self.sender

class NotifikasiTunda(models.Model):
	tujuan = models.EmailField()
	judul = models.CharField(max_length=141)
	isi =  models.TextField()
	dibuat = models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return self.tujuan + " " + self.judul
