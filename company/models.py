from django.db import models
from account.models import UserAccount


class Company(models.Model):
    user = models.ForeignKey(UserAccount,related_name='user_company', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    pin_code = models.IntegerField(blank=True, null=True)
    company_details = models.TextField(max_length=255, blank=True, null=True)
    leading_seller = models.BooleanField(default=False)
    verified_seller = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name

    @property
    def get_short_address(self):
        return '{}, {}'.format(self.city, self.state)

    @property
    def get_full_address(self):
        if self.address_line2 == None:
            return '{}, {}, {}, {}'.format(self.address_line1, self.city, self.state, self.pin_code)
        else:
            return '{}, {}, {}, {}'.format(self.address_line1, self.address_line2, self.city, self.state, self.pin_code)


    class Meta:
        managed = True
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'