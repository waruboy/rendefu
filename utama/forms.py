from django import forms

class KolegaTambahForm(forms.Form):
	nama = forms.CharField()
	
class KontakTambahForm(forms.Form):
	kontak = forms.CharField(widget=forms.Textarea)