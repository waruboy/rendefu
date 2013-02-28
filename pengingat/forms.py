from django import forms
from .models import Pengingat

class PengingatTambahForm(forms.ModelForm):

	class Meta:
		model = Pengingat
		fields = ("judul",)

class PengingatDetailForm(forms.ModelForm):

	class Meta:
		model =  Pengingat
		fields = ("judul", "keterangan", )
