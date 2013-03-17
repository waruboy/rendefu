from django import forms
from .models import Aktivitas, Kolega, PoinKontak

class AktivitasTambahForm(forms.ModelForm):

	class Meta:
		model = Aktivitas
		fields = ("nama", )

class AnggotaForm(forms.Form):
	nama = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'placeholder':"Nama"}))
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':"Email"}))

class AnggotaPasswordForm(forms.Form):
	password_lama = forms.CharField(widget=forms.PasswordInput(render_value=True, attrs={'placeholder':"Password lama"}))
	password_baru = forms.CharField(widget=forms.PasswordInput(render_value=True, attrs={'placeholder':"Password baru"}))
	password_baru_ulang = forms.CharField(widget=forms.PasswordInput(render_value=True, attrs={'placeholder':"Password baru (lagi)"}))


class DaftarForm(forms.Form):
    nama = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'placeholder':"Nama"}))
    organisasi = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder':"Organisasi/Perusahaan"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':"Email"}))
    password = forms.CharField(widget=forms.PasswordInput(render_value=True, attrs={'placeholder':"Password"}))

class DepanForm(forms.Form):
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':"Email"}))
	password = forms.CharField(widget=forms.PasswordInput(render_value=True, attrs={'placeholder':"Password"}))

class KolegaTambahForm(forms.Form):
	nama = forms.CharField()

class KolegaUbah1Form(forms.Form):
	nama = forms.CharField()
	telepon = forms.CharField()
	alamat = forms.CharField(widget=forms.Textarea)

class KolegaUbahForm(forms.ModelForm):
	class Meta:
		model = Kolega
		fields = ('nama', 'telepon', 'alamat', 'email', )
	
class KontakTambahForm(forms.ModelForm):
	class Meta:
		model = PoinKontak
		fields = ('kontak', )


