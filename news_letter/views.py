from django.shortcuts import render

# Create your views here.
from .models import NewsLetter
from .serializers import NewsLetterSerializer
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication


class NewsLetterViewset(viewsets.ModelViewSet):
    queryset = NewsLetter.objects.all()
    serializer_class = NewsLetterSerializer
    authentication_classes = [JWTAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
