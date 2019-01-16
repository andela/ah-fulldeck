from rest_framework import generics
from rest_framework.response import Response
# Create your views here.


class HomeView(generics.ListAPIView):
    """class to access the home route"""

    def get(self, request, format=None):
        return Response("Welcome to fulldeck Authors Haven API")
