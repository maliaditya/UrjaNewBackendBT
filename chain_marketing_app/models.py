from pyexpat import model
from django.db import models
import random
import calendar
from datetime import datetime

from django.db.models.base import Model


class Test(models.Model):
    name = models.CharField(max_length=233)
    
def unique_rand():
    while True:
        code = "URJA" + ''.join(random.choice('0123456789ABCDEF') for i in range(6))
        if not MemberAccount.objects.filter(member_id=code).exists():
            return code

def unique_order():
    while True:
        code =  ''.join(random.choice('0123456789ABCDEF') for i in range(6))
        if not Order.objects.filter(order_no=code).exists():
            return code

def unique_memberid():
    while True:
        code = "URJA" + ''.join(random.choice('0123456789ABCDEF') for i in range(12))
        if not MemberActivationKey.objects.filter(key=code).exists():
            return code

class MemberAccount(models.Model):
    user = models.ForeignKey('account.UserAccount',related_name='seller_account', on_delete=models.CASCADE)
    sponser_id = models.CharField(max_length=50, blank=True,null=True)
    member_id  = models.CharField(max_length=100, blank=True, primary_key=True, unique=True, default=unique_rand)
    taluka = models.CharField(max_length=255,blank=True,null=True, default='Haveli')
    district = models.CharField(max_length=255,blank=True,null=True, default='Pune')
    city = models.CharField(max_length=255,blank=True,null=True, default='Pune')
    pin_code = models.IntegerField( blank=True,null=True, default='411044')
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    left = models.BooleanField(default=False)
    right = models.BooleanField(default=False)
    
    
    @property
    def get_created_at(self):
        datetime_object = datetime.strptime(str(self.created_at), "%Y-%m-%d %H:%M:%S.%f%z")
        return '{} {} {}'.format(datetime_object.day,calendar.month_name[datetime_object.month],datetime_object.year)

    @property
    def get_updated_at(self):
        datetime_object = datetime.strptime(str(self.updated_at), "%Y-%m-%d %H:%M:%S.%f%z")
        return '{} {} {}'.format(datetime_object.day,calendar.month_name[datetime_object.month],datetime_object.year)

    def __str__(self):
        return str(self.user.first_name + " " + self.user.last_name + " ("+ self.member_id+")")

    @property
    def get_user_name(self):
        return  self.user.first_name + " " + self.user.last_name

    @property
    def active_taluka(self):
        return self.active_taluka.is_active
    

    @property
    def active_city(self):
        return self.active_city.is_active
    

    @property
    def active_district(self):
        return self.active_district.is_active
    

    @property
    def active_seller(self):
        return self.active_seller.is_active
    

    @property
    def get_active_member(self):
        return self.active_member.is_active
    

    class Meta:
        verbose_name = ("Member Account")
        verbose_name_plural = ("Member Accounts")

class BinaryTree(models.Model):
    member = models.OneToOneField(MemberAccount,related_name='binary_tree', on_delete=models.CASCADE)
    parent = models.ForeignKey(MemberAccount,related_name='parent_binary_tree', on_delete=models.CASCADE,null=True)
    is_active = models.BooleanField(default=False) 
    is_sponser_active = models.BooleanField(default=False) 
    is_admin = models.BooleanField(default=False)
    is_valid = models.BooleanField(default=False) # this field will be true once the user has passed 2:1 or 1:2 criteria
    left =models.ForeignKey(MemberAccount,related_name='left_binary_tree', on_delete=models.CASCADE, null=True)
    right = models.ForeignKey(MemberAccount,related_name='right_binary_tree', on_delete=models.CASCADE, null=True)
    position = models.CharField(max_length=255,default='Right')
    left_points = models.IntegerField( blank=True,null=True, default=0)
    right_points =  models.IntegerField( blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.member)

    def save(self, *args, **kwargs):
        if  self.is_sponser_active==True:
            self.updated_at = datetime.now()
        super().save(*args, **kwargs)
    
    @property
    def days(self):
        d0 = datetime.now().date()
        d1 = self.updated_at.date()
        delta = d0 - d1
        return delta.days

class MemberIsValidSponser(models.Model):
    btmember =models.OneToOneField(BinaryTree,related_name='binary_tree', on_delete=models.CASCADE)
    is_sponser_active = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        pass

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'MemberIsValidSponser'
        verbose_name_plural = 'MemberIsValidSponsers'

class ActiveDistrictDistibuter(models.Model):
    distributer = models.ForeignKey(MemberAccount,related_name='active_district', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_created_at(self):
        datetime_object = datetime.strptime(str(self.created_at), "%Y-%m-%d %H:%M:%S.%f%z")
        return '{} {} {}'.format(datetime_object.day,calendar.month_name[datetime_object.month],datetime_object.year)

    @property
    def get_updated_at(self):
        datetime_object = datetime.strptime(str(self.updated_at), "%Y-%m-%d %H:%M:%S.%f%z")
        return '{} {} {}'.format(datetime_object.day,calendar.month_name[datetime_object.month],datetime_object.year)

    def get_updated(self):
        return self.updated_at
        
    class Meta:
        verbose_name = ("Active DistrictDistibuter")
        verbose_name_plural = ("Active DistrictDistibuter")

    # def __str__(self):
    #     return self.name

class ActiveTalukaDistibuter(models.Model):
    distributer = models.ForeignKey(MemberAccount,related_name='active_taluka', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def get_created_at(self):
        datetime_object = datetime.strptime(str(self.created_at), "%Y-%m-%d %H:%M:%S.%f%z")
        return '{} {} {}'.format(datetime_object.day,calendar.month_name[datetime_object.month],datetime_object.year)

    @property
    def get_updated_at(self):
        datetime_object = datetime.strptime(str(self.updated_at), "%Y-%m-%d %H:%M:%S.%f%z")
        return '{} {} {}'.format(datetime_object.day,calendar.month_name[datetime_object.month],datetime_object.year)

    def get_updated(self):
        return self.updated_at
        
    class Meta:
        verbose_name = ("Active TalukaDistibuter")
        verbose_name_plural = ("Active TalukaDistibuter")

    # def __str__(self):
    #     return self.name


class ActiveCityDistibuter(models.Model):
    distributer = models.ForeignKey(MemberAccount,related_name='active_city', on_delete=models.CASCADE)
    city = models.CharField(max_length=255,blank=True,null=True)
    pin_code = models.IntegerField( blank=True,null=True, default='411044')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if  self.is_active==True:
            self.updated_at = datetime.now()
        super().save(*args, **kwargs)

    @property
    def get_created_at(self):
        datetime_object = datetime.strptime(str(self.created_at), "%Y-%m-%d %H:%M:%S.%f%z")
        return '{} {} {}'.format(datetime_object.day,calendar.month_name[datetime_object.month],datetime_object.year)


    @property
    def get_updated_at(self):
        datetime_object = datetime.strptime(str(self.updated_at), "%Y-%m-%d %H:%M:%S.%f%z")
        return '{} {} {}'.format(datetime_object.day,calendar.month_name[datetime_object.month],datetime_object.year)

    def get_updated(self):
        return self.updated_at

    class Meta:
        verbose_name = ("Active City Distibuter")
        verbose_name_plural = ("Active City Distibuter")

    # def __str__(self):
    #     return self.name
    
    @property
    def days(self):
        d0 = datetime.now().date()
        d1 = self.updated_at.date()
        delta = d0 - d1
        return delta.days

            
class ActiveSeller(models.Model):
    seller = models.ForeignKey(MemberAccount,related_name='active_seller', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    bonus_points = models.IntegerField(default=0)
    subproduct_bonus_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
            
    
    def save(self, *args, **kwargs):
        if  self.is_active==False:
            self.updated_at = datetime.now()
        super().save(*args, **kwargs)
        
    @property
    def get_created_at(self):
        datetime_object = datetime.strptime(str(self.created_at), "%Y-%m-%d %H:%M:%S.%f%z")
        return '{} {} {}'.format(datetime_object.day,calendar.month_name[datetime_object.month],datetime_object.year)


    @property
    def get_updated_at(self):
        datetime_object = datetime.strptime(str(self.updated_at), "%Y-%m-%d %H:%M:%S.%f%z")
        return '{} {} {}'.format(datetime_object.day,calendar.month_name[datetime_object.month],datetime_object.year)
    
    def get_updated(self):
        return self.updated_at

    class Meta:
        verbose_name = ("Active Seller")
        verbose_name_plural = ("Active Sellers")

    
    @property
    def days(self):
        d0 = datetime.now().date()
        d1 = self.updated_at.date()
        delta = d0 - d1
        return delta.days
    # def __str__(self):
    #     return self.name


class MemberActivationKey(models.Model):
    key  = models.CharField(max_length=100, blank=True, primary_key=True, unique=True, default=unique_memberid)
    is_active = models.BooleanField(default=False)
    allocated_to = models.ForeignKey(MemberAccount, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = ("Member Activation Key")
        verbose_name_plural = ("Member Activation Keys")

    def __str__(self):
        return str(self.key)


class ActiveMember(models.Model):
    member = models.ForeignKey(MemberAccount,related_name='active_member', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if  self.is_active==True:
            self.updated_at = datetime.now()
        super().save(*args, **kwargs)
    @property
    def get_created_at(self):
        datetime_object = datetime.strptime(str(self.created_at), "%Y-%m-%d %H:%M:%S.%f%z")
        return '{} {} {}'.format(datetime_object.day,calendar.month_name[datetime_object.month],datetime_object.year)


    @property
    def get_updated_at(self):
        datetime_object = datetime.strptime(str(self.updated_at), "%Y-%m-%d %H:%M:%S.%f%z")
        return '{} {} {}'.format(datetime_object.day,calendar.month_name[datetime_object.month],datetime_object.year)
    
    def get_updated(self):
        return self.updated_at

    @property
    def days(self):
        d0 = datetime.now().date()
        d1 = self.updated_at.date()
        delta = d0 - d1
        return delta.days

    class Meta:
        verbose_name = ("Active Member")
        verbose_name_plural = ("Active Members")

    # def __str__(self):
    #     return self.name


class AddProduct(models.Model):
    name = models.CharField(max_length=50, blank=True,null=True)
    created_by = models.ForeignKey('account.UserAccount',related_name='user_product', on_delete=models.CASCADE)
    category = models.CharField(max_length=50, blank=True,null=True)
    description = models.CharField(max_length=500, blank=True,null=True)
    is_published = models.BooleanField(default=False)
    has_key = models.BooleanField(default=False)
    is_package_product = models.BooleanField(default=False)
    is_package = models.BooleanField(default=False)
    add_package_product =  models.IntegerField( blank=True,null=True)
    quantity =  models.IntegerField( blank=True,null=True)
    max_payout =  models.IntegerField( blank=True,null=True)
    points_to_city_distributer = models.IntegerField( blank=True,null=True)
    active25_bonus = models.IntegerField( blank=True,null=True)
    seller_bonus = models.IntegerField( blank=True,null=True)
    points_to_taluka_distributer= models.IntegerField( blank=True,null=True)
    points_to_district_distributer= models.IntegerField( blank=True,null=True)
    points_to_buyer = models.IntegerField( blank=True,null=True)
    Price = models.IntegerField( blank=True,null=True)
    product_type = models.CharField(max_length=50, blank=True,null=True)
    MRP = models.IntegerField( blank=True,null=True)
    std_deduction = models.IntegerField(default=10, blank=True,null=True)
    tds = models.IntegerField(default=0, blank=True,null=True)
    
    @property
    def levels(self):
        return self.levels.all()
    
    @property
    def product_image(self):
        return self.product_image.all()
    
    class Meta:
        verbose_name = ("Add Product")
        verbose_name_plural = ("Add Products") 

    def __str__(self):
        return str(self.name)

class Level(models.Model):
    product = models.ForeignKey(AddProduct,related_name='levels', on_delete=models.CASCADE)
    level = models.IntegerField()
    points = models.IntegerField()

    class Meta:
        verbose_name = ("Level")
        verbose_name_plural = ("Levels")
        unique_together = (('product', 'level'),)
    # def __str__(self):
    #     return self.product

class Image(models.Model):
    product = models.ForeignKey(AddProduct,related_name='product_image', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='chain_product/',blank=True, null=True)  

    class Meta:
        verbose_name = ("Image")
        verbose_name_plural = ("Image")


class Order(models.Model):
    order_no  = models.CharField(max_length=100, blank=True, primary_key=True, unique=True, default=unique_order)
    ordered_from = models.ForeignKey(MemberAccount,related_name='ordered_from', on_delete=models.CASCADE)
    orded_by = models.ForeignKey(MemberAccount,related_name='ordered_by', on_delete=models.CASCADE)
    total_amount = models.IntegerField( blank=True,null=True)
    is_generated = models.BooleanField(default=False)
    is_transfer = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField( default="unpaid",max_length=255, blank=True,null=True)
    delivery =models.CharField(default="no delivery yet", max_length=255, blank=True,null=True)

    @property
    def get_created_at(self):
        datetime_object = datetime.strptime(str(self.created_at), "%Y-%m-%d %H:%M:%S.%f%z")
        return '{} {} {}'.format(datetime_object.day,calendar.month_name[datetime_object.month],datetime_object.year)


    @property
    def get_updated_at(self):
        datetime_object = datetime.strptime(str(self.updated_at), "%Y-%m-%d %H:%M:%S.%f%z")
        return '{} {} {}'.format(datetime_object.day,calendar.month_name[datetime_object.month],datetime_object.year)

    @property
    def order_detail(self):
        return self.order_detail.all()


    
    class Meta:
        ordering = ['-created_at']
        verbose_name = ("Order")
        verbose_name_plural = ("Orders")

    def __str__(self):
        return str(self.order_no)


class OrderDetails(models.Model):
    order = models.ForeignKey(Order,related_name='order_detail', on_delete=models.CASCADE)
    product = models.CharField( max_length=255, blank=True,null=True)
    product_id = models.IntegerField(default=1 ,blank=True,null=True)
    quantity = models.IntegerField( blank=True,null=True)
    is_generated = models.BooleanField(default=False)
    is_transfer = models.BooleanField(default=False)
    price = models.IntegerField( blank=True,null=True)
    generated = models.IntegerField(default=0, blank=True,null=True)
    transfer_in = models.IntegerField(default=0, blank=True,null=True)
    transfer_out = models.IntegerField(default=0, blank=True,null=True)
    order_by = models.ForeignKey(MemberAccount,related_name='member_account', on_delete=models.CASCADE)
    quantity_delivered = models.IntegerField(default=0)
    quantity_undelivered = models.IntegerField(default=0, blank=True,null=True)
    quantity_sold = models.IntegerField(default=0, blank=True,null=True)

    class Meta:
        verbose_name = ("Order Details")
        verbose_name_plural = ("Order Details")
        
    def __str__(self):
        return str(self.order)




class Payout(models.Model):
    member =  models.ForeignKey(MemberAccount,on_delete=models.CASCADE ,related_name='payout_member')
    from_member = models.ForeignKey(MemberAccount,on_delete=models.CASCADE ,related_name='payout_from_member')
    type = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True,null=True)
    points = models.DecimalField( default=0,max_digits = 19, decimal_places = 2)
    tds = models.IntegerField(default=0, blank=True,null=True)
    std_deduction = models.IntegerField( blank=True,null=True)
    payment = models.DecimalField(default=0, max_digits = 19, decimal_places = 2)
    payout = models.DecimalField(default=0, max_digits = 19, decimal_places = 2)
    description = models.TextField(blank=True,null=True)
    declared = models.BooleanField(default=False, blank=True,null=True)
    
    class Meta:
        verbose_name = ("Payout")
        verbose_name_plural = ("Payout")

    @property
    def get_created_at(self):
        datetime_object = datetime.strptime(str(self.created_at), "%Y-%m-%d %H:%M:%S.%f%z")
        return '{} {} {}'.format(datetime_object.day,calendar.month_name[datetime_object.month],datetime_object.year)


    @property
    def get_updated_at(self):
        datetime_object = datetime.strptime(str(self.updated_at), "%Y-%m-%d %H:%M:%S.%f%z")
        return '{} {} {}'.format(datetime_object.day,calendar.month_name[datetime_object.month],datetime_object.year)

    @property
    def days(self):
        d0 = datetime.now().date()
        d1 = self.created_at.date()
        delta = d0 - d1
        return delta.days

class Sale(models.Model):
    seller = models.ForeignKey(MemberAccount,related_name='seller_member', on_delete=models.CASCADE)
    member = models.ForeignKey(MemberAccount,related_name='sale_member', on_delete=models.CASCADE)
    product = models.ForeignKey(AddProduct,related_name='sale_product', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True,null=True)  
    
    @property
    def get_created_at(self):
        datetime_object = datetime.strptime(str(self.created_at), "%Y-%m-%d %H:%M:%S.%f%z")
        return '{} {} {}'.format(datetime_object.day,calendar.month_name[datetime_object.month],datetime_object.year)

    @property
    def get_updated_at(self):
        datetime_object = datetime.strptime(str(self.updated_at), "%Y-%m-%d %H:%M:%S.%f%z")
        return '{} {} {}'.format(datetime_object.day,calendar.month_name[datetime_object.month],datetime_object.year)


class BankDetails(models.Model):
    user = models.ForeignKey('account.UserAccount',related_name='user_bankdetails', on_delete=models.CASCADE)
    member = models.ForeignKey(MemberAccount,related_name='member_bankdetails', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True,null=True)  
    upi= models.CharField( max_length=255, blank=True,null=True)
    bank_name= models.CharField( max_length=255, blank=True,null=True)
    bank_branch= models.CharField( max_length=255, blank=True,null=True)
    bank_account= models.CharField( max_length=255, blank=True,null=True)
    bank_ifsc= models.CharField( max_length=255, blank=True,null=True)
    nominee= models.CharField( max_length=255, blank=True,null=True)
    
     
     
    @property  
    def get_created_at(self):
        datetime_object = datetime.strptime(str(self.created_at), "%Y-%m-%d %H:%M:%S.%f%z")
        return '{} {} {}'.format(datetime_object.day,calendar.month_name[datetime_object.month],datetime_object.year)
        
    @property   
    def get_updated_at(self):
        datetime_object = datetime.strptime(str(self.updated_at), "%Y-%m-%d %H:%M:%S.%f%z")
        return '{} {} {}'.format(datetime_object.day,calendar.month_name[datetime_object.month],datetime_object.year)


class Introducer(models.Model):
    introducer = models.ForeignKey(MemberAccount,related_name='introducer_details',on_delete=models.CASCADE )
    distributer = models.OneToOneField(MemberAccount,related_name='distributer',on_delete=models.CASCADE )
    # introducer = models.CharField( max_length=255, blank=True,null=True)
    # distributer = models.CharField( max_length=255, blank=True,null=True)
    class Meta:
        verbose_name = ("Introducer")
        verbose_name_plural = ("Introducers")

    # def __str__(self):
    #     return self.name

    @property
    def get_introducer(self):
        intro = str(self.introducer).split(' ')
        get_id = intro[2].split('(')
        get_id = get_id[1].split(')')
        return get_id[0]

    @property
    def get_distributer(self):
        intro = str(self.distributer).split(' ')
        get_id = intro[2].split('(')
        get_id = get_id[1].split(')')
        return get_id[0]

def get_pin_code(distributer):
    print(distributer)

class IntroducerRequests(models.Model):
    introducer = models.ForeignKey(MemberAccount,related_name='introducer_1details',on_delete=models.CASCADE )
    distributer = models.ForeignKey(MemberAccount,related_name='distributer1',on_delete=models.CASCADE )
    pin_code = models.IntegerField( blank=True,null=True,default= get_pin_code(distributer)) 
    status = models.BooleanField(default=False, blank=True,null=True)
    active_status = models.BooleanField(default=False, blank=True,null=True)
    # introducer = models.CharField( max_length=255, blank=True,null=True)
    # distributer = models.CharField( max_length=255, blank=True,null=True)
    class Meta:
        verbose_name = ("Introducer Requests")
        verbose_name_plural = ("Introducer Requests")

   
    # def __str__(self):
    #     return self.name

class IntroducerRequest(models.Model):
    introducer = models.ForeignKey(MemberAccount,related_name='introducer1_1details',on_delete=models.CASCADE )
    distributer = models.ForeignKey(MemberAccount,related_name='distributer11',on_delete=models.CASCADE )
    pin_code = models.IntegerField( blank=True,null=True,default= get_pin_code(distributer))
    status = models.BooleanField(default=False, blank=True,null=True)
    active_status = models.BooleanField(default=False, blank=True,null=True)
    # introducer = models.CharField( max_length=255, blank=True,null=True)
    # distributer = models.CharField( max_length=255, blank=True,null=True)
    class Meta:
        verbose_name = ("Introducer-Requests")
        verbose_name_plural = ("Introducer-Requests")



class CommonFields(models.Model):
    seller_bonus =models.IntegerField( blank=True,null=True)
    introducer_bonus =models.IntegerField( blank=True,null=True)
    is_active =models.BooleanField( blank=True,null=True)
    # introducer = models.CharField( max_length=255, blank=True,null=True)
    # distributer = models.CharField( max_length=255, blank=True,null=True)
    class Meta:
        verbose_name = ("Common Fields")
        verbose_name_plural = ("Common Fields")

    # def __str__(self):
    #     return self.name


class District(models.Model):
    district = models.CharField( max_length=255, blank=True,null=True)
    
    def __str__(self):
        return self.district

    
    @property
    def district_taluka(self):
        return self.district_taluka
    


    class Meta:
        managed = True
        verbose_name = 'District'
        verbose_name_plural = 'Districts'

class Taluka(models.Model):
    district = models.ForeignKey(District,related_name='district_taluka',on_delete=models.CASCADE )
    taluka = models.CharField( max_length=255, blank=True,null=True)

    @property
    def taluka_city(self):
        return self.taluka_city

    def __str__(self):
        return self.taluka

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Taluka'
        verbose_name_plural = 'Talukas'

class City(models.Model):
    taluka = models.ForeignKey(Taluka,related_name='taluka_city',on_delete=models.CASCADE )
    city = models.CharField( max_length=255, blank=True,null=True)
    

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"


class AdminAccounts(models.Model):
    total_payout  = models.FloatField()
    balance_after_deduction = models.FloatField()
    distributed_payout = models.FloatField()
    tds = models.FloatField()
    std = models.FloatField()
    total_balance = models.FloatField()
    dp = models.FloatField()
    bonus = models.FloatField()
    difference= models.FloatField()

    class Meta:
        verbose_name = 'Admin Accounts'
        verbose_name_plural = 'Admin Acounts'


class SubProductsStock(models.Model):
    member = models.ForeignKey(MemberAccount,related_name='member_details',on_delete=models.CASCADE )
    product = models.ForeignKey(AddProduct,related_name='sub_product', on_delete=models.CASCADE)
    quantity = models.IntegerField( blank=True,null=True)
    class Meta:
        verbose_name = 'SubProductsStock'
        verbose_name_plural = 'Sub Products Stocks'


class SubProductsSale(models.Model):
    from_member = models.ForeignKey(MemberAccount,related_name='from_member_details',on_delete=models.CASCADE )
    to_member = models.ForeignKey(MemberAccount,related_name='to_member_details',on_delete=models.CASCADE )
    Key = models.CharField(max_length=100, blank=True, primary_key=True, unique=True, default=unique_rand)
    class Meta:
        verbose_name = 'SubProducts Sale'
        verbose_name_plural = 'SubProducts Sale'

class AllMembersProductStock(models.Model):
    member = models.ForeignKey(MemberAccount,related_name='member_details1',on_delete=models.CASCADE )
    product_id = models.ForeignKey(AddProduct,related_name='sub_product1', on_delete=models.CASCADE)
    product_type = models.CharField(max_length=50, blank=True,null=True)
    product_name = models.CharField(max_length=50, blank=True,null=True)
    ordered = models.IntegerField( blank=True,null=True)
    delivered = models.IntegerField( blank=True,null=True)
    undelivered = models.IntegerField( blank=True,null=True)
    generated = models.IntegerField( blank=True,null=True)
    transfer_in = models.IntegerField( blank=True,null=True)
    transfer_out = models.IntegerField( blank=True,null=True)
    sold = models.IntegerField( blank=True,null=True)
    stock = models.IntegerField( blank=True,null=True)

    class Meta:
        verbose_name = ("AllMembersProductStock")
        verbose_name_plural = ("AllMembersProductStock")



class MemberLevelInfo(models.Model):
    member = models.ForeignKey(MemberAccount, on_delete=models.CASCADE)
    level = models.IntegerField(blank=True,null=True)
    total = models.IntegerField(blank=True,null=True)

    def __str__(self):
        pass

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'MemberLevelInfo'
        verbose_name_plural = 'MemberLevelInfos'

class BinaryPayoutAttrs(models.Model):
    one_pair = models.IntegerField(blank=True,null=True)
    payable_pairs = models.IntegerField(blank=True,null=True)
    one_pair_value = models.FloatField(blank=True,null=True)
    is_active = models.BooleanField()

    

    class Meta:
        verbose_name = ("BinaryPayoutAttrs")
        verbose_name_plural = ("BinaryPayoutAttrss")




