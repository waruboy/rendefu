from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from utama.libs import unique_slugify


class Profil(models.Model):
	user = models.OneToOneField(User)
	nama = models.CharField('nama lengkap',max_length=80)
	panggilan = models.CharField('nama panggilan',max_length=80, blank=True, null=True)

	class Meta:
		verbose_name_plural = 'profil'

	def __unicode__(self):
		return self.nama

	def get_panggilan(self):
		if self.panggilan == "":
			return self.nama
		return self.panggilan
	def get_organisasi(self):
		organisasi = Organisasi.objects.get(anggota=self)
		return organisasi
	def save(self, *args, **kwargs):
		try:
			existing = Profil.objects.get(user=self.user)
			self.id = existing.id
		except Profil.DoesNotExist:
			pass
		models.Model.save(self, *args, **kwargs)

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profil.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)


class Organisasi(models.Model):
	JENIS_LANGGANAN = (
		(u'perunggu', u'perunggu'),
		(u'perak', u'perak'),
		(u'emas', u'emas'),
		(u'platina', u'platina'),
		(u'spesial', u'spesial'),
	)
	nama = models.CharField(max_length=30)
	kode = models.SlugField()
	bergabung = models.DateField('tanggal bergabung',auto_now_add=True)
	anggota = models.ManyToManyField(User, through='Status', blank=True, null=True)
	jenis = models.CharField(max_length=10, choices=JENIS_LANGGANAN, default=u'perunggu')
	aktif = models.BooleanField(default=True)

	class Meta:
		verbose_name_plural = 'organisasi'

	def __unicode__(self):
		return self.nama

	def save(self, *args, **kwargs):
		if not self.kode:
			unique_slugify(self, self.nama, 'kode')
		super(Organisasi, self).save(*args, **kwargs)


class Status(models.Model):
	JENIS_STATUS = (
		(u'anggota',u'anggota'),
		(u'manajer',u'manajer'),
		(u'pemilik',u'pemilik'),
		)
	user = models.ForeignKey(User)
	organisasi = models.ForeignKey(Organisasi)
	masuk = models.DateField(auto_now_add=True)
	status = models.CharField(max_length=10, choices=JENIS_STATUS, default=u'anggota')

	class Meta:
		verbose_name_plural = 'status anggota'

	def __unicode__(self):
		return self.user.get_profile().nama + u' di ' + self.organisasi.nama

class Kolega(models.Model):
	nama = models.CharField(max_length=64)
	kode = models.SlugField()
	telepon = models.CharField(max_length=64, blank=True, null=True)
	email = models.EmailField(blank=True, null=True)
	alamat = models.TextField(blank=True, null=True)
	keterangan = models.TextField(blank=True)
	ditambahkan = models.DateField(auto_now_add=True)
	dilihat = models.DateTimeField(null=True,blank=True)
	organisasi = models.ForeignKey(Organisasi)
	tanggal_lahir = models.DateField(blank="True", null="True")
	dihapus = models.BooleanField(default=False)


	class Meta:
		verbose_name_plural = 'kolega'

	def __unicode__(self):
		return self.nama

	def save(self, *args, **kwargs):
		if not self.kode:
			unique_slugify(self, self.nama, 'kode')
		super(Kolega, self).save(*args, **kwargs)

class Aktivitas(models.Model):
	kolega = models.ForeignKey(Kolega)
	nama = models.CharField("nama aktivitas", max_length=140)
	dibuat = models.DateField(auto_now_add=True)
	selesai = models.BooleanField(default=False)
	tanggal_selesai = models.DateField(blank=True, null=True)

	class Meta:
		verbose_name_plural = 'aktivitas'

	def __unicode__(self):
		return self.nama

class PoinKontak(models.Model):
	waktu = models.DateTimeField(auto_now_add=True)
	kontak = models.TextField("Catatan")
	kolega = models.ForeignKey(Kolega)
	user = models.ForeignKey(User, blank=True, null=True)
	aktivitas = models.ForeignKey(Aktivitas, blank=True, null=True)

	class Meta:
		verbose_name_plural = 'poin kontak'

	def __unicode__(self):
		label = "%s: %s" % (str(self.waktu), self.kolega.nama)
		return label


