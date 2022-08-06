from django.views.generic.detail import DetailView   
from django.http import FileResponse
from django.db import models
from rest_framework import serializers
from rest_framework import mixins, status, viewsets,filters
from rest_framework.response import Response

class APK(models.Model):

    apk = models.FileField(upload_to='apk/',blank=True, null=True)

    class Meta:
        verbose_name = ("APK")
        verbose_name_plural =("APK")
    
    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        return super().delete(using=using, keep_parents=keep_parents)



class BaseFileDownloadView(DetailView):
  def get(self, request, *args, **kwargs):
    filename=self.kwargs.get('filename', None)
    if filename is None:
      raise ValueError("Found empty filename")
    some_file = self.model.objects.get(imported_file=filename)
    response = FileResponse(some_file.imported_file, content_type="text/csv")
    # https://docs.djangoproject.com/en/1.11/howto/outputting-csv/#streaming-large-csv-files
    response['Content-Disposition'] = 'attachment; filename="%s"'%filename
    return response

class SomeFileDownloadView(BaseFileDownloadView):
    model = APK
