from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('utama.views',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sistem/keluar/$', 'keluar'),
    url(r'^sistem/daftar/$', 'daftar'),
    url(r'^sistem/profil/$', 'anggota_profil'),
    url(r'^$', 'depan', name='depan'),
    url(r'^(?P<kode_organisasi>[a-z0-9_-]+)/$', 'organisasi'),
    url(r'^(?P<kode_organisasi>[a-z0-9_-]+)/profil/$', 'anggota_profil'),
    url(r'^(?P<kode_organisasi>[a-z0-9_-]+)/tambah_anggota/$', 'anggota_tambah'),
    url(r'^(?P<kode_organisasi>[a-z0-9_-]+)/kolega/$', 'kolega_daftar'),
    url(r'^(?P<kode_organisasi>[a-z0-9_-]+)/kolega/tambah$', 'kolega_tambah'),
    url(r'^(?P<kode_organisasi>[a-z0-9_-]+)/kolega/ubah$', 'kolega_ubah'),
    url(r'^(?P<kode_organisasi>[a-z0-9_-]+)/kolega/(?P<kode_kolega>[a-z0-9_-]+)/$', 'kolega'),
    url(r'^(?P<kode_organisasi>[a-z0-9_-]+)/kolega/(?P<kode_kolega>[a-z0-9_-]+)/ubah/$', 'kolega_ubah'),
    url(r'^(?P<kode_organisasi>[a-z0-9_-]+)/kolega/(?P<kode_kolega>[a-z0-9_-]+)/hapus/$', 'kolega_hapus'),
    url(r'^(?P<kode_organisasi>[a-z0-9_-]+)/kolega/(?P<kode_kolega>[a-z0-9_-]+)/aktivitas/$', 'aktivitas'),
    url(r'^(?P<kode_organisasi>[a-z0-9_-]+)/kolega/(?P<kode_kolega>[a-z0-9_-]+)/aktivitas/tambah/$', 'aktivitas_tambah'),
    url(r'^(?P<kode_organisasi>[a-z0-9_-]+)/kolega/(?P<kode_kolega>[a-z0-9_-]+)/aktivitas/(?P<pk_aktivitas>[0-9]+)/$', 'aktivitas_detail'),
    url(r'^(?P<kode_organisasi>[a-z0-9_-]+)/kolega/(?P<kode_kolega>[a-z0-9_-]+)/aktivitas/(?P<pk_aktivitas>[0-9]+)/selesai/$', 'aktivitas_selesai'),
    url(r'^(?P<kode_organisasi>[a-z0-9_-]+)/kolega/(?P<kode_kolega>[a-z0-9_-]+)/kontak/tambah/$', 'kontak_tambah'),
    # url(r'^aplikasi/', include('aplikasi.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	
)

urlpatterns += patterns('pengingat.views',
    url(r'^(?P<kode_organisasi>[a-z0-9_-]+)/pengingat/tambah$', 'pengingat_tambah'),
    url(r'^(?P<kode_organisasi>[a-z0-9_-]+)/pengingat/(?P<id_pengingat>[0-9]+)/$', 'pengingat_detail'),
    url(r'^(?P<kode_organisasi>[a-z0-9_-]+)/pengingat/(?P<id_pengingat>[0-9]+)/selesai/$', 'pengingat_selesai'),
)
