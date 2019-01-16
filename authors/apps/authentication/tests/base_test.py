from django.urls import reverse
from rest_framework.test import APITestCase
import jwt
from authors import settings


class TestBaseCase(APITestCase):
    def setUp(self):
        self.signup_url = reverse('app_authentication:signup')
        self.login_url = reverse('app_authentication:login')
        self.current_user_url = reverse('app_authentication:current_user')
        self.password_reset_url = reverse('app_authentication:password_reset')
        self.invalid_token = 'thsnmbnscjkxcmm.btydghvhjb'

        self.test_user = {
            'user': {
                'username': 'testuser',
                'email': 'test@user.com',
                'password': 'TestUser123'
            }}

        email = 'test@user.com'
        token = jwt.encode({"email": "test@user.com"},
                        settings.SECRET_KEY, algorithm='HS256').decode()
        self.password_update_url = reverse(
            'authentication:password_update', kwargs={'token': token})
            
        self.no_email = ['email']
        self.no_username = ['username']
        self.no_password = ['password']
        self.passwords = {
            'password':'Nicanor12nic',
            'confirm_password':'Nicanor12nic'
        }

    def remove_data(self, keys=None):
        if keys:
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
    
