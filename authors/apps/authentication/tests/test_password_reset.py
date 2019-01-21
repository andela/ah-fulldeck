# Python and Django imports
from rest_framework.views import status
from django.urls import reverse

# local imports
from .base_test import TestBaseCase


class TestPasswordReset(TestBaseCase):
    def test_if_email_exists(self):
        response = self.client.post(self.password_reset_url,
                                    data={"email": "tes@user.com"},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn(b'Email does not exists', response.content)

    def test_no_email_provided(self):
        response = self.client.post(self.password_reset_url,
                                    data={"email": ""},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'Email field cannot be blank', response.content)

    def test_successful_email_sent(self):
        self.signup_user()
        response = self.client.post(self.password_reset_url,
                                    data={"email": "test@user.com"},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            b'A password reset link has been sent to your email', response.content)
