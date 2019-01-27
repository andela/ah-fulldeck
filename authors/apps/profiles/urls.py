from django.urls import path

from . import views

app_name = 'profiles'

urlpatterns = [
    path('users/<str:username>',
         views.ProfileRetrieveAPIView.as_view(), name='user_profile'),
    path('users/<username>/follow/', views.FollowUnfollow.as_view(), name='follow'),
    path('users/<username>/following/',
         views.Following.as_view(), name='following'),
    path('users/<username>/followers/', views.FollowedBy.as_view(), name='followers')

]
