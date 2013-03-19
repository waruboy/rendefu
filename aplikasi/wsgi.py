"""
WSGI config for aplikasi project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aplikasi.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.

## komentar 2 baris berikut
# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()

## definisikan aplikasi baru
import django.core.handlers.wsgi
_application = django.core.handlers.wsgi.WSGIHandler()

def application(environ, start_response):
  os.environ['EC2_S3_ID'] = environ['EC2_S3_ID']
  os.environ['EC2_S3_SECRET'] = environ['EC2_S3_SECRET']
  os.environ['RENDEFU_MAILGUN_USER'] = environ['RENDEFU_MAILGUN_USER']
  os.environ['RENDEFU_MAILGUN_PASSWORD'] = environ['RENDEFU_MAILGUN_PASSWORD']
  return _application(environ, start_response)


# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
