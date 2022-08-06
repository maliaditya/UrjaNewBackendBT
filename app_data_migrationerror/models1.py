from django.db import models
from chain_marketing_app.models import MemberAccount
import random
from datetime import datetime
def unique_rand():
    while True:
        code = "URJA" + ''.join(random.choice('0123456789ABCDEF') for i in range(12))
        if not ActivationKeys.objects.filter(activation_key=code).exists():
            return code



class ActivationKeys(models.Model):
    activation_key  = models.CharField(max_length=100, blank=True, primary_key=True, unique=True, default=unique_rand)
    is_active = models.BooleanField(default=False)
    allocated_to = models.ForeignKey(MemberAccount, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = ("Activation Keys")
        verbose_name_plural = ("Activation Keys")
    
   
    # def __str__(self):
    #     return self.sponser_id


class ActiveUser(models.Model):
    user = models.ForeignKey('account.UserAccount',related_name='active_user', on_delete=models.CASCADE)
    activation_key  = models.CharField('ActivationKeys', max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    paid_service_balance = models.IntegerField(default=5)
    free_service_balance = models.IntegerField(default=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # sponser_id = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = ("Android App Users")
        verbose_name_plural = ("Android App Users")

    # def __str__(self):
    #     return self.sponser_id
    
    @property
    def days(self):
        d0 = datetime.now().date()
        d1 = self.updated_at.date()
        delta = d0 - d1
        return delta.days



class SOS(models.Model):
    user = models.ForeignKey('account.UserAccount',related_name='sms_user', on_delete=models.CASCADE)
    receivernumber  = models.CharField( max_length=50, null=True, blank=True)
    sendername  = models.CharField( max_length=50, null=True, blank=True)
    receivername  = models.CharField( max_length=50, null=True, blank=True)
    longitude  = models.CharField( max_length=50, null=True, blank=True)
    latitude  = models.CharField( max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = ("SOS")
        verbose_name_plural = ("SOSs")

    # def __str__(self):
    #     return self.name
