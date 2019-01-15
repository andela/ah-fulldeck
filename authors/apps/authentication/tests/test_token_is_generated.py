from django.urls import reverse
from rest_framework.views import status
from rest_framework.test import APITestCase, APIClient
from authors.apps.authentication.models import User


class JwtTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('authentication:user-login')
        self.signup_url = reverse('authentication:user-registration')
        self.current_user_url = reverse('authentication:current_user')
        self.email = "marani@gmail.com"

        self.user_data = {
            "user": {
                "username": "marani",
                "email": "marani@gmail.com",
                "password": "@Allano19"
            }}

        self.invalid_token = 'thsnmbnscjkxcmm.btydghvhjb'
        self.registration = self.client.post(
            self.signup_url, self.user_data, format='json')
        del self.user_data['user']['username']
        self.login = self.client.post(self.login_url,
                                      self.user_data, format='json')
        self.token = self.login.data["token"]

    def test_token_on_register(self):
        """if user is registers successfully, a token is generated"""
        response = self.registration
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)

    def test_token_on_login(self):
        """Test if a user logs in successfully, a token is generated"""

        response = self.login
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_get_current_user(self):
        """Test to get current user when token is passed in the request"""

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(self.current_user_url)
        assert response.status_code == 200
        assert response.data["email"] == "marani@gmail.com"
        assert response.data["username"] == "marani"

    def test_get_user_no_token(self):
        """Test getting a user with no token provided in the request"""

        response = self.client.get(self.current_user_url)
        assert response.status_code == 403
        msg = "Authentication credentials were not provided."
        assert response.data["detail"] == msg

    def test_get_user_invalid_token(self):
        """Test getting a user with an expired or invalid token"""

        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.invalid_token)
        response = self.client.get(self.current_user_url)
        assert response.status_code == 403
        assert response.data["detail"] == "Invalid token"

    def test_get_non_existent_user(self):
        """Test getting a user who doesn't exist in db"""

        User.objects.get(email=self.email).delete()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(self.current_user_url)
        assert response.status_code == 403
        assert response.data["detail"] == "User does not exist"
