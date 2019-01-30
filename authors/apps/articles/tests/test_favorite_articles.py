from .base_test import TestBaseCase

from rest_framework import status
from .test_like_dislike_articles import TestLikeDislike


class TestFavoriteArticles(TestBaseCase):
    def favorite_Article(self, url):
        """
        allows a logged in user to favorite article
        """
        self.authorize()
        response = self.client.put(url)
        return response
    
    def return_200_ok(self, response):
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_favorite_Article(self):
        slug = self.create_article()
        response = self.favorite_Article(self.favorite_article_url(slug))
        self.return_200_ok(response)
        self.assertIn(b'Article favorited', response.content)

    def test_unfavorite_favorited_Article(self):
        slug = self.create_article()
        url = self.favorite_article_url(slug)
        self.favorite_Article(url)
        response = self.favorite_Article(url)
        self.return_200_ok(response)
        self.assertIn(b'Article unfavorited', response.content)

    def test_favorite_unavailable_Article(self):
        slug = 'am-unavailable-slug'
        response = self.favorite_Article(self.favorite_article_url(slug))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'No article found for the slug given', response.content)

    def test_get_all_favorites_articles(self):
        slug = self.create_article()
        self.favorite_Article(self.favorite_article_url(slug))
        self.authorize()
        response = self.client.get(self.my_favorites_url())
        self.return_200_ok(response)

    def test_no_all_favorites_articles(self):
        self.authorize()
        response = self.client.get(self.my_favorites_url())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_token_favorites_articles(self):
        token = 'sdsfsdfsd'
        response = self.client.get(
            self.my_favorites_url(),
            format='json',
            HTTP_AUTHORIZATION='Token ' + token
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
