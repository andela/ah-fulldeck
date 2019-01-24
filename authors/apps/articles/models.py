from django.db import models
from django.utils.text import slugify

from authors.apps.authentication.models import User


class Article(models.Model):
    """
    The model for creating the articles is defined here
    """
    slug = models.SlugField(
        db_index=True, max_length=1000, unique=True, blank=True)
    title = models.CharField(max_length=1000, blank=False)
    description = models.CharField(max_length=2000, blank=False)
    body = models.TextField(blank=False)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    author = models.ForeignKey(
        User, related_name='article', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def create_slug(self):
        """
        Before the title is saved it has to be converted to a slug
        'This is a title' will be converted to This-is-a-title
        """
        slug = slugify(self.title)
        new_slug = slug
        n = 1
        while Article.objects.filter(slug=new_slug).exists():
            new_slug = '{}-{}'.format(slug, n)
            n += 1

        return new_slug

    def save(self, *args, **kwargs):
        """
        Ensure that before an article is saved,
        it must have a slug created from the title
        """
        if not self.slug:
            self.slug = self.create_slug()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    """
    Model for comments
    """

    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User, related_name='comments', on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, related_name='comments', on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='threads',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.body

    class Meta:
        ordering = ('-created_at',)
