from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User 
from utama.models import Profil, Organisasi, Status, Kolega, PoinKontak

class ProfilInline(admin.StackedInline):
	model = Profil
	can_delete = False

class UserAdmin(UserAdmin):
	inlines = (ProfilInline, )

class StatusInline(admin.StackedInline):
	model = Status

class OrganisasiAdmin(admin.ModelAdmin):
	exclude = ('kode', )
	inlines = (StatusInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Organisasi, OrganisasiAdmin)
admin.site.register(Kolega)
admin.site.register(PoinKontak)

