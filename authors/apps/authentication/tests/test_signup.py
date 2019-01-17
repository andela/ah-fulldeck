# Python and Django imports
from rest_framework.views import status


# local imports
from .base_test import TestBaseCase


class TestRegistration(TestBaseCase):
    def base_signup(self, credentials):
        self.remove_data(credentials)
        response = self.signup_user()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'This field is required', response.content)

    def test_valid_user_registration(self):
        response = self.signup_user()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_no_username_registration(self):
        self.base_signup(self.no_username)

    def test_no_email_registration(self):
        self.base_signup(self.no_email)

    def test_no_password_registration(self):
        self.base_signup(self.no_password)
