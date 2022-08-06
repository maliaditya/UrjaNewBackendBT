from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from company.models import Company
from products.models import FavouriteProduct, Products, Review, ProductEnquiries
from products.serializers import FavouriteProductSerializer
from .models import Address, UserAccount,FAQ,Reports
from products.models import FavouriteProduct, Products, Review, ProductEnquiries
from products.serializers import FavouriteProductSerializer
from chain_marketing_app.serializers import MemberAccountSerializer,MemberAccountListSerializer,BankDetailsSerializer
from app_data.serializers import ActiveUserSerializer
from .models import Address, UserAccount,FAQ,Reports
User = get_user_model()
User = get_user_model()


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields ='__all__'



class ReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        fields ='__all__'



class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields ='__all__'



class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields =['id', 'email','first_name','last_name','phone']


class ProductEnquiriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductEnquiries
        fields ='__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields ='__all__'



class CompanyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields ='__all__'

class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields ='__all__'

class ProductsSerializer(serializers.ModelSerializer):
    reviews = ReviewsSerializer(many=True,required=False,read_only=True)
    class Meta:
        model = Products
        fields = [  'id','name','in_stock','details','price','front_image','back_image','extra_image','discount',
                    'created_by','reviews','category','rating','total_ratings',
                    'product_type','company', 'get_created_at','get_updated_at'  ]

# class ProductFavouritesSerializer(serializers.ModelSerializer):
#     product = ProductsSerializer()
#     class Meta:
#         model = FavouriteProduct
#         fields =['product','FavouriteProductSerializer']      


class UserCreateSerializer(UserCreateSerializer):
    user_bankdetails = BankDetailsSerializer(many=True, read_only=True)
    product_enquires = ProductEnquiriesSerializer(many=True, read_only=True)
    company_details = CompanyUserSerializer(many=True, read_only=True)
    user_favourites = FavouriteProductSerializer(many=True, read_only=True)
    address = AddressSerializer(many=True, read_only=True)
    user_products = ProductsSerializer(many=True, read_only=True)
    seller_account = MemberAccountListSerializer(many=True, read_only=True)
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['id', 'email','first_name','address','last_name','phone','news_letter','seller_account','user_bankdetails', 'company_details','user_favourites','product_enquires','user_products'] 


class SellerAcountRegisterSerializer(UserCreateSerializer):
    seller_account = MemberAccountSerializer()
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['id', 'email','first_name','address','last_name','phone','password','re_password','seller_account'] 