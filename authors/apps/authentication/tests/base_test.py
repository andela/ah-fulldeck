from django.urls import reverse
from rest_framework.test import APITestCase


class TestBaseCase(APITestCase):
    def setUp(self):
        self.signup_url = reverse('app_authentication:signup')
        self.login_url = reverse('app_authentication:login')
        self.current_user_url = reverse('app_authentication:current_user')
        self.invalid_token = 'thsnmbnscjkxcmm.btydghvhjb'

        self.test_user = {
            'user': {
                'username': 'testuser',
                'email': 'test@user.com',
                'password': 'TestUser123'
            }}

        self.no_email = ['email']
        self.no_username = ['username']
        self.no_password = ['password']

    def remove_data(self, keys):
        for key in keys:
            del self.test_user['user'][key]
        return self.test_user

    def signup_user(self):
        return self.client.post(self.signup_url,
                                self.test_user,
                                format='json')

    def login_user(self):
        self.remove_data(self.no_username)
        return self.client.post(self.login_url,
                                self.test_user,
                                format='json')
