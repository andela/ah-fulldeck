from .base_test import TestBaseCase

from rest_framework import status


class TestLikeDislike(TestBaseCase):
    def base_like_dislike_article(self, token, url):
        response = self.client.post(
            url,
            format='json',
            HTTP_AUTHORIZATION='Token ' + token
        )
        return response

    def base_create_article(self, token):
        """
        creates an articles
        """
        url = self.create_list_article_url
        response = self.client.post(url, self.article, format='json',
                                    HTTP_AUTHORIZATION='Token ' + token)
        return response

    def base_test(self):
        token = self.login_user()
        article_response = self.base_create_article(token)
        slug = article_response.data['slug']
        url = self.like_arcticle_url(slug)
        response = self.base_like_dislike_article(token, url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response

    def test_like_an_article(self):
        """
        Test than an authenticated user can like an article
        """
        self.base_test()

    def test_dislike_an_article(self):
        """
        Test than an authenticated user can dislike an article
        """
        self.base_test()

    def test_like_already_liked(self):
        """
        Test than an authenticated user can like an article that he/she had already liked
        """
        self.base_test()

    def test_like_already_disliked(self):
        """
        Test than an authenticated user can dislike an article that he/she had already disliked
        """
        self.base_test()

    def test_like_dislike_non_existing_article(self):
        """
        Test than an authenticated user can like/dislike non existent article
        """
        token = self.login_user()
        slug_response = self.base_create_article(token)
        slug = slug_response.data['slug'] + "test-artle"
        url = self.like_arcticle_url(slug)
        response = self.base_like_dislike_article(token, url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn(b'Not found', response.content)
