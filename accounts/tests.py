from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserTestCase(TestCase):
    def setUp(self):
        self.testuser_username = 'testuser'
        self.testuser_password = 'Qazxsw123'
        self.testuser = User.objects.create_user(self.testuser_username, password=self.testuser_password)

    def test_user_pw(self):
        checked = self.testuser.check_password(self.testuser_password)
        self.assertTrue(checked)
