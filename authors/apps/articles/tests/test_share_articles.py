from rest_framework import status

from .base_test import TestBaseCase


class TestShareArticle(TestBaseCase):
    def base_email_share(self, slug, email):
        """
        allows a logged in user to share an article via email
        """
        self.authorize()
        url = self.article_email_share_url(slug)
        email = {"email": "nicnic@nic.com"}
        response = self.client.post(url, data=email, format='json')
        return response
    
    def base_social_share(self, slug, url):
        """
        allows a logged in user to share an article via twitter or facebook
        """
        self.authorize()
        response = self.client.post(url)
        return response

    def return_200_ok(self, response):
        """ Returns success status code """
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def return_unavailable(self, response):
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_email_share_fail(self):
        self.authorize()
        slug = self.create_article()
        email = {"email": "test@user.com"}
        response = self.base_email_share(slug, email)
        self.return_unavailable(response)

    def test_invalid_email(self):
        self.authorize()
        slug = self.create_article()
        email = {"email": "testuser.com"}
        response = self.base_email_share(slug, email)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_email_share_unavailable_slug(self):
        slug = 'i-dont-exist-slug'
        email = {"email": "test@user.com"}
        response = self.base_email_share(slug, email)
        self.return_unavailable(response)

    def test_empty_email(self):
        slug = self.create_article()
        email = {"email": ""}
        response = self.base_email_share(slug, email)
        self.return_unavailable(response)

    def test_twitter_share(self):
        slug = self.create_article()
        url = self.article_twitter_share_url(slug)
        response = self.base_social_share(slug, url)
        self.return_200_ok(response)
    
    def test_twittter_share_unavailable_slug(self):
        slug = 'am-unavailable-slug'
        url = self.article_twitter_share_url(slug)
        response = self.base_social_share(slug, url)
        self.return_unavailable(response)

    def test_facebook_share(self):
        slug = self.create_article()
        url = self.article_facebook_share_url(slug)
        response = self.base_social_share(slug, url)
        self.return_200_ok(response)
    
    def test_facebook_share_unavailable_slug(self):
        slug = 'i-dont-exist-slug'
        url = self.article_facebook_share_url(slug)
        response = self.base_social_share(slug, url)
        self.return_unavailable(response)
