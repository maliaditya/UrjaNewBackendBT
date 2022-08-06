from rest_framework import serializers
from .models import NewsLetter

class NewsLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsLetter
        fields = '__all__'
        