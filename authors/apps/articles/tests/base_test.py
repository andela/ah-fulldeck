from django.urls import reverse
from rest_framework.test import APITestCase


class TestBaseCase(APITestCase):
    def setUp(self):
        self.signup_url = reverse('app_authentication:signup')
        self.login_url = reverse('app_authentication:login')
        self.create_list_article_url = reverse('articles:articles')
        self.test_user = {
            'user': {
                'username': 'testuser',
                'email': 'test@user.com',
                'password': 'TestUser123'
            }}
        self.test_user2 = {
            'user': {
                'username': 'testuser2',
                'email': 'test2@user.com',
                'password': 'TestUser123'
            }}
        self.article = {
            "article": {
                "title": "Test Article",
                "description": "Test description for the article",
                "body": "Test body for the article",
                "author": 1
            }
        }
        self.rating = {
            "rating": {
                "rating": 5
            }
        }
        self.bad_Rating = {
            "rating": {
                "rating": 7
            }
        }
        self.no_email = ['email']
        self.no_username = ['username']
        self.no_password = ['password']

        self.comment = {
            "comment": {
                "body": "This is a test comment body."
            }
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

    def signup_user2(self):
        return self.client.post(self.signup_url,
                                self.test_user2,
                                format='json')

    def login_user(self):
        self.signup_user()
        try:
            self.remove_data(self.no_username)
        except:
            pass
        response = self.client.post(self.login_url,
                                    self.test_user,
                                    format='json')
        token = response.data['token']
        return token

    def login_user2(self):
        self.signup_user2()
        response = self.client.post(self.login_url,
                                    self.test_user2,
                                    format='json')
        token = response.data['token']
        return token

    def create_article(self):
        token = self.login_user()
        url = self.create_list_article_url
        response = self.client.post(
            url, self.article, format='json',
            HTTP_AUTHORIZATION="Token " + token)
        slug = response.data['slug']
        return slug

    def single_article_url(self, slug):
        url = reverse('articles:article-details', args=[slug])
        return url

    def single_article_details(self):
        slug = self.create_article()
        url = reverse('articles:article-details', {slug: 'slug'})
        return url

    def create_comment(self, slug):
        url = reverse("articles:comments", kwargs={"slug": slug})
        return url

    def add_comment(self, slug):
        url = self.create_comment(slug)
        token = self.login_user()
        response = self.client.post(
            url,
            self.comment,
            format="json",
            HTTP_AUTHORIZATION="Token " + token
        )
        return response

    def specific_comment(self, slug, id):
        url = reverse('articles:comment-details',
                      kwargs={"slug": slug, "id": id})
        return url
        
    def like_arcticle_url(self, slug):
        url = reverse('articles:article_like', args=[slug])
        return url

    def dislike_article_url(self, slug):
        url = reverse('articles:article_dislike', args=[slug])

    def rating_url(self, slug):
        url = reverse('articles:rate-articles', args=[slug])
        return url

    def ratings_url(self, slug):
        url = reverse('articles:article-ratings', args=[slug])
        return url