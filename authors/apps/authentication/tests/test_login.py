# Django imports
from rest_framework.views import status

# local imports
from .base_test import TestBaseCase


class TestLogin(TestBaseCase):
    def base_login(self, credential):
        self.signup_user()
        self.remove_data(credential)
        response = self.login_user()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'This field is required', response.content)

    def test_valid_user_login(self):
        self.signup_user()
        response = self.login_user()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_email_login(self):
        self.base_login(self.no_email)

    def test_no_password_login(self):
        self.base_login(self.no_password)

    def test_unregistered_user_login(self):
        response = self.login_user()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
