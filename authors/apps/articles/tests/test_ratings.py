from .base_test import TestBaseCase

from rest_framework import status


class TestRating(TestBaseCase):

    def base_rating(self, message, response):
        self.assertIn(message.encode(), response.content)

    def authorized_post_request(self, url):
        token = self.login_user()
        response = self.client.post(
            url, self.rating, format='json',
            HTTP_AUTHORIZATION='Token ' + token)
        return response

    def authorized_post_request2(self, url):
        token = self.login_user2()
        response = self.client.post(
            url, self.rating, format='json',
            HTTP_AUTHORIZATION='Token ' + token)
        return response

    def http_200_ok(self, response):
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def http_403_forbidden(self, response):
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def http_400_badrequest(self, response):
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_rating_authorized(self):
        slug = self.create_article()
        url = self.rating_url(slug)
        response = self.authorized_post_request2(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        message = "You have rated this article successfully"
        self.assertIn(message.encode(), response.content)

    def test_article_owner_cannot_rate(self):
        slug = self.create_article()
        url = self.rating_url(slug)
        response = self.authorized_post_request(url)
        self.http_403_forbidden(response)
        message = "You cannot rate your own article"
        self.base_rating(message, response)

    def test_create_rating_unauthorized(self):
        slug = self.create_article()
        url = self.rating_url(slug)
        response = self.client.post(url,
                                    self.rating, format='json')
        self.http_403_forbidden(response)
        message = "Authentication credentials were not provided."
        self.base_rating(message, response)

    def test_user_rating_nonexistent_article(self):
        slug = self.create_article()
        url = self.rating_url(slug+'tes-aetrc')
        response = self.authorized_post_request2(url)
        self.http_400_badrequest(response)
        message = "No article found for the slug given"
        self.base_rating(message, response)

    def test_view_ratings_authorized(self):
        token = self.login_user()
        slug = self.create_article()
        url = self.ratings_url(slug)
        response = self.client.get(url,
                                   HTTP_AUTHORIZATION='Token ' + token)
        self.http_200_ok(response)

    def test_view_ratings_unauthorized(self):
        slug = self.create_article()
        url = self.ratings_url(slug)
        response = self.client.get(url)
        self.http_403_forbidden(response)
        message = "Authentication credentials were not provided."
        self.base_rating(message, response)

    def test_rating_is_betwen_one_and_five(self):
        slug = self.create_article()
        bad_rating = self.bad_Rating
        token = self.login_user2()
        url = self.rating_url(slug)
        response = self.client.post(url,
                                    data=bad_rating,
                                    format="json",
                                    HTTP_AUTHORIZATION='Token ' + token)
        self.http_400_badrequest(response)
        message = "Rating should be a number between 1 and 5"
        self.base_rating(message, response)
