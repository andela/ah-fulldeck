from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    bio = serializers.CharField(allow_blank=True, required=False)
    image = serializers.URLField(required=False)

    followers_count = serializers.IntegerField(
        read_only=True,
        source="followers.count"
    )

    following_count = serializers.IntegerField(
        read_only=True,
        source="following.count"
    )

    class Meta:
        model = Profile
        fields = ('username', 'bio', 'image', 'followers_count',
                  'following_count', 'created_at', 'updated_at')
