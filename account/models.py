from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserAccountManager(BaseUserManager):
    def create_user(self, email, first_name,last_name, phone,password=None):
        if not email:
            raise ValueError('user must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name,phone=phone )
        user.set_password(password)
        user.save()
        return user
        
    def create_superuser(self, email, first_name,last_name, phone,password=None):
        user = self.create_user( email, first_name,last_name, phone,password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
        

class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, default='user')
    last_name = models.CharField(max_length=255,default='user')
    phone = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','phone']
    @property
    def seller_account(self):
        return self.seller_account.all() 
    @property
    def active_user(self):
        return self.active_user.all()     
    @property
    def user_favourites(self):
        return self.user_favourites.all() 
    
    @property
    def user_products(self):
        return self.user_data.all() 


    @property
    def product_enquires(self):
        return self.user_ProductEnquiries.all() 

    @property
    def news_letter(self):
        return self.news_letter.all() 


    @property
    def company_details(self):
        return self.user_company.all() 
    
    @property
    def address(self):
        return self.user_address.all() 
    
    @property
    def user_bankdetails(self):
        return self.user_bankdetails.all() 

    @property
    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name) 
    
    

    def get_short_name(self):
        return '{}'.format(self.first_name) 


    def __str__(self):
        return self.email


class Address(models.Model):
    user = models.ForeignKey(UserAccount,related_name='user_address', on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=50,blank=True, null=True)
    address_line2 = models.CharField(max_length=50,blank=True, null=True)
    city = models.CharField(max_length=50,blank=True, null=True)
    state = models.CharField(max_length=50,blank=True, null=True)
    pin_code = models.CharField(max_length=50,blank=True, null=True)
    

    class Meta:
        verbose_name = ("Address")
        verbose_name_plural = ("Address")

    def __str__(self):
        return self.city


class FAQ(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    question = models.TextField(blank=True, null=True)
    answer = models.TextField(blank=True, null=True)
  

    class Meta:
        verbose_name = ("FAQ")
        verbose_name_plural = ("FAQ's")

    def __str__(self):
        return self.question


class Reports(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    complaint = models.TextField(blank=True, null=True)
  

    class Meta:
        verbose_name = ("Report")
        verbose_name_plural = ("Reports")

    def __str__(self):
        return self.complaint

