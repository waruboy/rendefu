from django.contrib import admin
from .models import NotifikasiDikirim, Surel, NotifikasiTunda

admin.site.register(Surel, )
admin.site.register(NotifikasiTunda, )
admin.site.register(NotifikasiDikirim, )