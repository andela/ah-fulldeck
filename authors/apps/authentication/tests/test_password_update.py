# Python and Django imports
from rest_framework.views import status
from django.urls import reverse

# local imports
from .base_test import TestBaseCase
from .test_password_reset import TestPasswordReset


class TestPasswordUpdate(TestBaseCase):
    def base_password_update(self, message, password, confirm_password):
        TestPasswordReset.test_successful_email_sent(self)
        self.passwords['password'] = password
        self.passwords['confirm_password'] = confirm_password
        response = self.client.put(self.password_update_url,
                                   data=self.passwords,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(message.encode(), response.content)

    def test_password_not_same(self):
        message = "Passwords do not match"
        self.base_password_update(message, 'Nicanor123', 'Nicanor2')

    def test_successful_password_update(self):
        TestPasswordReset.test_successful_email_sent(self)
        response = self.client.put(self.password_update_url,
                                   data=self.passwords,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(b'Your password has been reset', response.content)

    def test_password_length(self):
        message = "Password must be at least 8 characters long"
        self.base_password_update(message, 'Nican', 'Nican')

    def test_unique_password(self):
        message = "Password must have at least a number, and a least an uppercase and a lowercase letter"
        self.base_password_update(message, 'nicanor', 'nicanor')
