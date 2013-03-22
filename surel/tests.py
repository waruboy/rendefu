"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""


from django.contrib.auth.models import User
from django.test import TestCase

from .libs import ambil_alamat

class SimpleTest(TestCase):
	def test_basic_addition(self):
		"""
		Tests that 1 + 1 always equals 2.
		"""
		self.assertEqual(1 + 1, 2)
	def test_ambil_alamat(self):
		"""
		Cek parsing email
		"""
		teks = '"Taufiq Muhammadi <taufiq.muhammadi@gmail.com>'
		alamat = ambil_alamat(teks)
		self.assertEqual(alamat, 'taufiq.muhammadi@gmail.com')

