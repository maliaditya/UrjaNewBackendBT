from django.db import models
from rest_framework import serializers
from rest_framework import mixins, status, viewsets,filters
class Image(models.Model):

    image = models.ImageField(upload_to='category/',blank=True, null=True)

    class Meta:
        verbose_name = ("Image")
        verbose_name_plural =("Images")

             
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'



class ImageViewset(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class =   ImageSerializer
    authentication_classes = []
    permission_classes = []
