from django import forms
from utama.models import Kolega

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
		exclude = ['kode', 'ditambahkan', 'organisasi']
	
class KontakTambahForm(forms.Form):
	kontak = forms.CharField(widget=forms.Textarea)