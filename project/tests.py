import os
from  django.test import TestCase
from django.conf import settings
from django.contrib.auth.password_validation import validate_password

class ConfigTest(TestCase):
    # check unittest - python library
    def test_secret_key_strength(self):
        password_is_strong = validate_password(settings.SECRET_KEY)
        self.assertNotEqual(settings.SECRET_KEY, '123') # dump example
