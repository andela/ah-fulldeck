from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        'authentication.User', on_delete=models.CASCADE
    )
    bio = models.TextField(blank=True)
    image = models.URLField(
        blank=True,
        default="https://d1nhio0ox7pgb.cloudfront.net/_img/o_collection_png/green_dark_grey/512x512/plain/user.png")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    following = models.ManyToManyField(
        'self', related_name='is_following', symmetrical=False)
    followers = models.ManyToManyField('self', symmetrical=False)
    bookmarks = models.ManyToManyField('articles.Article',
                                       related_name='bookmarks')

    def __str__(self):
        return self.user.username

    def follow(self, profile):
        self.following.add(profile)
        profile.followers.add(self.user.id)

    def unfollow(self, profile):
        self.following.remove(profile)
        profile.followers.remove(self.user.id)

    def list_followers(self, profile):
        return profile.is_following.all()

    def list_following(self, profile):
        return profile.following.all()

    class Meta:
        ordering = ['user__username']
