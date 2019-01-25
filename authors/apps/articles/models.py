from django.db import models
from django.utils.text import slugify
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey

from authors.apps.authentication.models import User


class LikeDislikeManager(models.Manager):
    """
    Manager class for like and dislike
    """
    use_for_related_fields = True

    def likes(self):
        """
        get all the likes for an object
        """
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        """
        get all the dislikes of an object
        """
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        """
        obtain the aggregate likes/dislikes
        """
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0

    def articles(self):
        """
        obtain the votes of a particular user
        """
        return self.get_queryset().filter(content_type__model='article').order_by('-articles__published_at')


class LikeDislike(models.Model):
    """
    Users should be able to like and/or dislike an article or comment.
    This class creates the fields for like/dislike
    """
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Dislike'),
        (LIKE, 'Like')
    )

    vote = models.SmallIntegerField(verbose_name=_("vote"), choices=VOTES)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("user"))
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()


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
    votes = GenericRelation(LikeDislike, related_query_name='article')

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


class ArticleRatings(models.Model):
    """
    Ratings given by different users
    """
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='articleratings')
    rating = models.IntegerField(default=0)
    rated_by = models.ForeignKey(User, on_delete=models.CASCADE)
