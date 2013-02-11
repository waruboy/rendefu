from django import forms
from utama.models import Kolega

class KolegaTambahForm(forms.Form):
	nama = forms.CharField()

class KolegaUbah1Form(forms.Form):
	nama = forms.CharField()
	telepon = forms.CharField()
	alamat = forms.CharField(widget=forms.Textarea)

class KolegaUbahForm(forms.ModelForm):
	class Meta:
		model = Kolega
		exclude = ['kode', 'ditambahkan', 'organisasi']
	
class KontakTambahForm(forms.Form):
	kontak = forms.CharField(widget=forms.Textarea)