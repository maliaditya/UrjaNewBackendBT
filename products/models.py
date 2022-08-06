from django.db import models
from datetime import datetime
# Create your models here.
from account.models import UserAccount
from company.models import Company
import calendar


class ProductType(models.Model):
    product_type = models.CharField(max_length=255,blank=True, null=True)
    image = models.ImageField(upload_to='category/',blank=True, null=True)
    
    def __str__(self):
        return str(self.product_type)

    @property
    def product_data(self):
        return self.product_data.all()
    
    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        return super().delete(using=using, keep_parents=keep_parents)

    class Meta:
        managed = True
        verbose_name = 'Seller Type'
        verbose_name_plural = 'Seller Type'
        ordering = ['id']



class Categories(models.Model):
    category_name = models.CharField(max_length=255,blank=True, null=True)
   
    def __str__(self):
        return self.category_name

    class Meta:
        managed = True
        verbose_name = 'Categories'
        verbose_name_plural = 'Categories'
        ordering = ['category_name']


class Products(models.Model):
    STATUS = (
       ('Pending', 'Pending'),
       ('Approved ', 'Approved '),
       ('Rejected', 'Rejected'),
   )
    created_by = models.ForeignKey(UserAccount,related_name='user_data', on_delete=models.CASCADE)
    company = models.ForeignKey(Company,related_name='company_data', on_delete=models.CASCADE)
    category = models.ForeignKey(Categories,related_name='Categories_data', on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType,related_name='product_data', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    details = models.TextField()
    price = models.CharField(max_length=255)
    discount = models.CharField(max_length=255)
    rating = models.FloatField(default=0)
    in_stock = models.BooleanField(default=False)
    total_ratings = models.IntegerField(default=0)
    front_image = models.ImageField(upload_to='product/',blank=True, null=True)
    back_image = models.ImageField(upload_to='product/',blank=True, null=True)
    approved = models.CharField(max_length=255,choices=STATUS ,default='Pending')
    extra_image = models.ImageField(upload_to='product/',blank=True, null=True)
    # extra_2 = models.ImageField(blank=True, null=True)
    def delete(self, using=None, keep_parents=False):
        self.front_image.delete()
        self.back_image.delete()
        return super().delete(using=using, keep_parents=keep_parents)
    def __str__(self):
        return self.name
     
    @property
    def get_created_at(self):
        datetime_object = datetime.strptime(str(self.created_at), "%Y-%m-%d %H:%M:%S.%f%z")
        return '{} {} {}'.format(datetime_object.day,calendar.month_name[datetime_object.month],datetime_object.year)


    @property
    def get_updated_at(self):
        datetime_object = datetime.strptime(str(self.updated_at), "%Y-%m-%d %H:%M:%S.%f%z")
        return '{} {} {}'.format(datetime_object.day,calendar.month_name[datetime_object.month],datetime_object.year)
 

    @property
    def reviews(self):
        return self.product_review_data.all()
  
    class Meta:
        managed = True
        verbose_name = 'Products'
        verbose_name_plural = 'Products'
        ordering = ['-id']



class Review(models.Model):
    user = models.ForeignKey(UserAccount,related_name='user_review_data', on_delete=models.CASCADE)
    product = models.ForeignKey(Products,related_name='product_review_data', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    review = models.TextField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
      
    
    @property
    def get_created_at(self):
        datetime_object = datetime.strptime(str(self.created_at), "%Y-%m-%d %H:%M:%S.%f%z")
        return '{} {} {}'.format(datetime_object.day,calendar.month_name[datetime_object.month],datetime_object.year)


    @property
    def get_updated_at(self):
        datetime_object = datetime.strptime(str(self.updated_at), "%Y-%m-%d %H:%M:%S.%f%z")
        return '{} {} {}'.format(datetime_object.day,calendar.month_name[datetime_object.month],datetime_object.year)
 
    def __str__(self):
        return self.user.first_name 

    class Meta:
        managed = True
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'




class FavouriteProduct(models.Model):
    user = models.ForeignKey('account.UserAccount', related_name='user_favourites', on_delete=models.CASCADE)
    product = models.ForeignKey('Products', related_name='favourite_products', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Favourite Product'
        verbose_name_plural = 'Favourite Products'


class ProductEnquiries(models.Model):
    user = models.ForeignKey('account.UserAccount', related_name='user_ProductEnquiries', on_delete=models.CASCADE)
    product = models.ForeignKey('Products', related_name='product_enquires', on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255,blank=True, null=True)
    phone_number = models.CharField(max_length=255,blank=True, null=True)
    email = models.CharField(max_length=255,blank=True, null=True)
    product_name =  models.CharField(max_length=255,blank=True, null=True)
    enquiry_for =  models.CharField(max_length=255,blank=True, null=True)
    state =  models.CharField(max_length=255,blank=True, null=True)
    city =  models.CharField(max_length=255,blank=True, null=True)
    paid = models.BooleanField(default=False)

    class Meta:
        managed = True
        verbose_name = 'Product Enquiry'
        verbose_name_plural = 'Product Enquiries'
        ordering = ['-id']
