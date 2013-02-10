from django import forms

class KolegaTambahForm(forms.Form):
	nama = forms.CharField()
	telepon = forms.CharField()
	alamat = forms.CharField(widget=forms.Textarea)
	
class KontakTambahForm(forms.Form):
	kontak = forms.CharField(widget=forms.Textarea)