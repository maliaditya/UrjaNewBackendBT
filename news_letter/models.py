from django.db import models
from account.models import UserAccount
# Create your models here.
class NewsLetter(models.Model):
    user = models.ForeignKey('account.UserAccount',related_name='news_letter', on_delete=models.CASCADE)
    email = models.CharField(max_length=50)

    class Meta:
        verbose_name =("News Letter")
        verbose_name_plural = ("News Letter")

    def __str__(self):
        return self.email
