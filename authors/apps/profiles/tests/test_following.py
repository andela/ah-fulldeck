from rest_framework import status
from rest_framework.reverse import reverse
from authors.apps.authentication.tests.base_test import TestBaseCase


class FollowUnfollowTest(TestBaseCase):
    """
    User follow/ unfollow test cases
    """

    def login_user2(self):
        self.client.post(self.signup_url, self.test_user_2, format='json')
        """This will login an existing user"""
        response = self.client.post(
            self.login_url, self.test_user_2, format='json')
        token = response.data['token']
        return token

    def following_url(self):
        url = reverse("profiles:following", kwargs={
            "username": 'testuser'})
        return url

    def followers_url(self):
        url = reverse("profiles:followers", kwargs={
            "username": self.test_user_2['user']['username']})
        return url

    def follow_existing_user_url(self):
        url = reverse("profiles:follow", kwargs={
                      "username": self.test_user_2['user']['username']})
        return url

    def follow_non_existing_user_url(self):
        url = reverse("profiles:follow", kwargs={
                      "username": 'nonExistingUser'})
        return url

    def follow_yourself(self):
        url = reverse("profiles:follow", kwargs={
                      "username": self.test_user['user']['username']})
        return url

    def follow(self, url):
        self.login_user2()
        self.signup_user()
        data = {}
        token = self.login_user().data['token']
        response = self.client.post(
            url, data,
            HTTP_AUTHORIZATION='Token ' + token, format='json')
        return response

    def forbidden_403(self, response):
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def ok_200(self, response):
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def not_found_404(self, response):
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def response_message_test(self, message, response):
        self.assertIn(message.encode(), response.content)

    def test_get_followers_without_authorization(self):
        response = self.client.get(
            self.followers_url(), format='json')
        self.forbidden_403(response)
        msesage = 'Authentication credentials were not provided.'
        self.response_message_test(msesage, response)

    def test_get_following_without_auth(self):
        response = self.client.get(
            self.following_url(), format='json')
        self.forbidden_403(response)
        msesage = 'Authentication credentials were not provided.'
        self.response_message_test(msesage, response)

    def test_get_following_with_auth(self):
        self.follow(self.follow_existing_user_url())
        token = self.login_user2()
        response = self.client.get(
            self.following_url(),
            HTTP_AUTHORIZATION='Token ' + token, format='json')
        msesage = 'Here is a list users following testuser'
        self.response_message_test(msesage, response)
        self.ok_200(response)

    def test_get_followers_with_auth(self):
        self.follow(self.follow_existing_user_url())
        token = self.login_user2()
        response = self.client.get(
            self.followers_url(),
            HTTP_AUTHORIZATION='Token ' + token, format='json')
        msesage = 'Here is a list of followers'
        self.response_message_test(msesage, response)
        self.ok_200(response)

    def test_follow_with_auth(self):
        response = self.follow(self.follow_existing_user_url())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        msesage = 'You are now following'
        self.response_message_test(msesage, response)

    def test_follow_without_auth(self):
        self.signup_user()
        self.login_user2()
        url = reverse("profiles:follow", kwargs={
            "username": self.test_user_2['user']['username']})
        response = self.client.post(url, format='json')
        self.not_found_404(response)
        msesage = 'You must be logged in first'
        self.response_message_test(msesage, response)

    def test_unfollow_with_auth(self):
        self.follow(self.follow_existing_user_url())
        self.signup_user()
        self.test_user['user']['username'] = 'testuser'
        token = self.login_user().data['token']
        response = self.client.delete(
            self.follow_existing_user_url(),
            HTTP_AUTHORIZATION='Token ' + token, format='json')
        self.ok_200(response)
        msesage = 'You have successfuly unfollowed'
        self.response_message_test(msesage, response)

    def test_unfollow_without_auth(self):
        self.follow(self.follow_existing_user_url())
        response = self.client.delete(
            self.follow_existing_user_url(), format='json')
        self.not_found_404(response)
        msesage = 'You must be logged in first'
        self.response_message_test(msesage, response)

    def test_follow_non_existing_user(self):
        response = self.follow(self.follow_non_existing_user_url())
        self.not_found_404(response)
        msesage = '{"Details": {"detail": "You are trying to follow a user who does not exist, please check the username again"}}'
        self.response_message_test(msesage, response)

    def test_following_yourself(self):
        response = self.follow(self.follow_yourself())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        msesage = 'You cannot follow yourself'
        self.response_message_test(msesage, response)
