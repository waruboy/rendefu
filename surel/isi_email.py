

def naskah_bergabung(nama, organisasi):
	naskah = """%s,


Selamat bergabung dengan rendefu.com
Alamat email anda sudah terdaftar sebagai administrator %s.""" % (nama.title(), organisasi)
	return naskah