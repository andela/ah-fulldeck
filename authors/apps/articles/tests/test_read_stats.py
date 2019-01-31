from rest_framework import status

from .base_test import TestBaseCase


class ReadStatsTest(TestBaseCase):
    def base_stats(self, data, response):
        self.assertIn(data.encode(), response.content)

    def http_200_ok(self, response):
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def authorized_post_request(self, url, token):
        response = self.client.post(
            url, self.rating, format='json',
            HTTP_AUTHORIZATION='Token ' + token)
        return response

    def test_initial_stats_are_zero(self):
        self.create_article()
        response = self.article_stats()
        data = '"view_count": 0'
        self.base_stats(data, response)

    def test_owner_view_is_not_added_to_stats(self):
        self.authorize()
        self.view_single_article()

        response = self.article_stats()
        self.http_200_ok(response)
        data = '"view_count": 0'
        self.base_stats(data, response)

    def test_views_by_different_users_are_added_to_stats(self):
        token = self.login_user2()
        slug = self.create_article()
        url = self.single_article_url(slug)
        self.client.get(url,
                        HTTP_AUTHORIZATION="Token " + token, format='json')
        response = self.article_stats()
        self.http_200_ok(response)
        data = '"view_count": 1'
        self.base_stats(data, response)

    def test_comments_by_same_user_are_added_to_stats(self):

        slug = self.create_article()
        response = self.add_comment(slug)
        response = self.article_stats()
        self.http_200_ok(response)
        data = '"comment_count": 1'
        self.base_stats(data, response)

    def test_likes_on_articles_are_added_to_stats(self):
        token = self.login_user2()
        slug = self.create_article()
        url = self.like_arcticle_url(slug)
        self.authorized_post_request(url, token)
        response = self.article_stats()
        self.http_200_ok(response)
        data = 'likes_count": 1'
        self.base_stats(data, response)

    def test_dislikes_on_articles_are_added_to_stats(self):
        token = self.login_user2()
        slug = self.create_article()
        url = self.dislike_article_url(slug)
        self.authorized_post_request(url, token)
        response = self.article_stats()
        self.http_200_ok(response)
        data = 'dislikes_count": 1'
        self.base_stats(data, response)

    def test_ratings_on_articles_are_added_to_stats(self):
        slug = self.create_article()
        self.rate_article(slug)
        response = self.article_stats()
        self.http_200_ok(response)
        data = '"average_rating": 5.0}'
        self.base_stats(data, response)
