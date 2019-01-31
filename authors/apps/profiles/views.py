from rest_framework import status
from rest_framework.generics import (
    RetrieveUpdateAPIView, CreateAPIView, RetrieveAPIView, ListAPIView)
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated)
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound

from .exceptions import ProfileDoesNotExist
from authors.apps.core.pagination import StandardPagination
from .models import Profile
from .renderers import (ProfileJSONRenderer, FollowUnfollowJsonRenderer,
                        FollowingFollowrsJsonRenderer)
from .serializers import ProfileSerializer


def current_user_profile(request):
    authenticated_user = request.user
    return authenticated_user.profile


def followed_user_profile(username, action=None):
    try:
        profile_to_follow = Profile.objects.get(user__username=username)
        return profile_to_follow
    except Exception:
        raise NotFound(
            'You are trying to {} a user who does not exist, please check the username again'.format(action))


def check_user_profile(request):
    try:
        following_user = current_user_profile(request)
        return following_user
    except Exception:
        raise NotFound(
            'You must be logged in first')


class ListProfile(ListAPIView):
    renderer_classes = (ProfileJSONRenderer,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        paginator = StandardPagination()
        queryset = Profile.objects.all().exclude(user=self.request.user)
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = ProfileSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class ProfileRetrieveAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    def get(self, request, username, *args, **kwargs):
        try:
            profile = Profile.objects.select_related('user').get(
                user__username=username
            )
        except Profile.DoesNotExist:
            raise ProfileDoesNotExist

        serializer = self.serializer_class(profile)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, username):

        if request.user.username != username:
            error_message = {
                'error': 'You are not allowed to update the details for user {}'.format(username)
            }
            return Response(error_message, status=status.HTTP_403_FORBIDDEN)
        user_data = request.data.get('profile', {})

        serializer = ProfileSerializer(
            request.user.profile,
            data=user_data,
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            self.check_object_permissions(request, user_data)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowUnfollow(CreateAPIView):
    renderer_classes = (FollowUnfollowJsonRenderer,)
    permision_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def post(self, request, username):
        """
        This method handles following a user
        """
        # get current user
        following_user = check_user_profile(request)
        # check if the user to be followed exists
        try:
            followed_user = followed_user_profile(username, 'follow')
        except Profile.DoesNotExist:
            pass
        # Check if user is trying to follow himself
        if following_user.id == followed_user.id:
            raise ValidationError("You cannot follow yourself")
        # Add user
        following_user.follow(followed_user)

        serialize = self.serializer_class(
            followed_user, context={'request': request})
        data = {
            'user': username,
            'follow-detail': serialize.data
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def delete(self, request, username):
        """
        This method handles unfollowing a user
        """
        # get current user
        following_user = check_user_profile(request)

        # check if the user to unfollowed be exists
        followed_user = followed_user_profile(username, 'unfollow')

        # Check if user trying to unfollow him/herself
        if following_user.id == followed_user.id:
            raise ValidationError("You cannot unfollow yourself")

        # unfollow user
        following_user.unfollow(followed_user)

        serialize = self.serializer_class(
            followed_user, context={'request': request})
        data = {
            'user': username,
            'unfollow-detail': serialize.data
        }
        return Response(data, status=status.HTTP_200_OK)


class Following(RetrieveAPIView):
    """
    Get all the users a user follows
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    renderer_classes = (FollowingFollowrsJsonRenderer,)

    def get(self, request, username):
        """Following"""

        following_user = current_user_profile(request)
        try:
            followed_user = followed_user_profile(username)
        except Exception:
            raise NotFound(
                'No such user found,please check the username again')
        following = following_user.list_following(followed_user)

        serializer = self.serializer_class(
            following, many=True, context={'request': request})
        data = {
            'user': username,
            'following-detail': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)


class FollowedBy(RetrieveAPIView):
    """
    Get all the users who follow a user
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    renderer_classes = (FollowingFollowrsJsonRenderer,)

    def get(self, request, username):
        """Followers"""

        following_user = check_user_profile(request)
        try:
            followed_user = followed_user_profile(username)
        except Exception:
            raise NotFound(
                'No such user found,please check the username again')

        follower = following_user.list_followers(followed_user)

        serializer = self.serializer_class(
            follower, many=True, context={'request': request})
        data = {
            'user': username,
            'followers-detail': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
