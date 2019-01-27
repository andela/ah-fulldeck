import os
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
        self.social_auth_url = reverse('app_authentication:social_auth')
        self.invalid_token = 'thsnmbnscjkxcmm.btydghvhjb'
        self.oauth2_token = os.getenv('FACEBOOK_TOKEN')
        self.oauth1_token = os.getenv('TWITTER_TOKEN')
        self.oauth1_token_secret = os.getenv('TWITTER_TOKEN_SECRET')

        self.invalid_provider_data = {
            "provider": "fb",
            "access_token": self.oauth2_token

        }
        self.invalid_token_data = {
            "provider": "facebook",
            "access_token": self.invalid_token

        }
        self.oauth2_data = {
            "provider": "facebook",
            "access_token": self.oauth2_token
        }
        self.oauth1_data = {
            "provider": "twitter",
            "access_token": self.oauth1_token,
            "access_token_secret": self.oauth1_token_secret
        }
        self.no_token_data = {
            "provider": "facebook"
        }
        self.no_provider_data = {
            "access_token": self.oauth2_token
        }
        self.no_token_secret_data = {
            "provider": "twitter",
            "access_token": self.oauth1_token,

        }
        self.test_user = {
            'user': {
                'username': 'testuser',
                'email': 'test@user.com',
                'password': 'TestUser123'
            }}
        self.test_user_2 = {
            "user": {
                'username': 'TestUser2',
                'email': 'testuser2@email.com',
                'password': 'TestUser2@123',
            }
        }

        email = 'test@user.com'
        token = jwt.encode({"email": "test@user.com"},
                           settings.SECRET_KEY, algorithm='HS256').decode()
        self.password_update_url = reverse(
            'authentication:password_update', kwargs={'token': token})

        self.user_profile = {
            'profile': {
                'bio': 'see me see you',
                'image': 'https://static.productionready.io/images/smiley-cyrus.jpg'
            }
        }
        self.username = self.test_user['user']['username']
        self.no_email = ['email']
        self.no_username = ['username']
        self.no_password = ['password']
        self.passwords = {
            'password': 'Nicanor12nic',
            'confirm_password': 'Nicanor12nic'
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

    def token(self):
        self.signup_user()
        return self.login_user().data['token']

    def get_profile_url(self, username):
        return reverse('profiles:user_profile', args={username})
