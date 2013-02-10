from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('utama.views',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'depan', name='depan'),
    url(r'^(?P<kode_organisasi>[a-z0-9_-]+)/$', 'organisasi'),
    url(r'^(?P<kode_organisasi>[a-z0-9_-]+)/kolega/$', 'kolega_daftar'),
    url(r'^(?P<kode_organisasi>[a-z0-9_-]+)/kolega/tambah$', 'kolega_tambah'),
    url(r'^(?P<kode_organisasi>[a-z0-9_-]+)/kolega/(?P<kode_kolega>[a-z0-9_-]+)/$', 'kolega'),
    url(r'^(?P<kode_organisasi>[a-z0-9_-]+)/kolega/(?P<kode_kolega>[a-z0-9_-]+)/kontak/tambah/$', 'kontak_tambah'),
    # url(r'^aplikasi/', include('aplikasi.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	
)
