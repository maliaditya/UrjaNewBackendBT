from rest_framework import serializers
from .models import Products, Categories, ProductType, Review, FavouriteProduct, ProductEnquiries
from company.models import Company
from account.models import UserAccount

       
       

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [ "id","company_name","get_short_address", "company_details", 
                    "leading_seller", "verified_seller" ,
                ]

                  
class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


                  
class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'



                  
class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = [ 'get_full_name']


                  
class ReviewSerializer(serializers.ModelSerializer):
    user = UserAccountSerializer(required=False)
    class Meta:
        model = Review
        fields = [ 'user','review','rating', 'get_created_at','get_updated_at']
        depth = 1



class ProductSerializer(serializers.ModelSerializer):
    # company = CompanySerializer()
    # created_by = UserAccountSerializer()
    # category = CategorieSerializer()
    # product_type = ProductTypeSerializer()
    # reviews = ReviewSerializer(many=True,required=False,read_only=True)
    class Meta:
        model = Products
        fields = [  'id','name','in_stock','details','price','front_image','back_image','extra_image','discount',
                    'created_by','reviews','category','rating','total_ratings',
                    'product_type','company', 'get_created_at','get_updated_at','approved'
                    ]
        # depth = 1


class ProductDetailSerializer(serializers.ModelSerializer):
    company = CompanySerializer(required=False,read_only=True)
    created_by = UserAccountSerializer(required=False,read_only=True)
    category = CategorieSerializer(required=False,read_only=True)
    product_type = ProductTypeSerializer(required=False,read_only=True)
    reviews = ReviewSerializer(many=True,required=False,read_only=True)
    class Meta:
        model = Products
        fields = [  'id','name','in_stock','details','price','front_image','back_image','extra_image','discount',
                    'created_by','reviews','category','rating','total_ratings',
                    'product_type','company', 'get_created_at','get_updated_at', 'approved'
                    ]
    
class ProductFavouriteDetailSerializer(serializers.ModelSerializer):
    created_by = UserAccountSerializer(required=False,read_only=True)
    category = CategorieSerializer(required=False,read_only=True)
    product_type = ProductTypeSerializer(required=False,read_only=True)
    reviews = ReviewSerializer(many=True,required=False,read_only=True)
    
    class Meta:
        model = Products
        fields = [  'id','name','in_stock','details','price','front_image','back_image','extra_image','discount',
                    'created_by','reviews','category','rating','total_ratings',
                    'product_type','company', 'get_created_at','get_updated_at', 'approved'
                    ]
      
     
class FavouriteProductSerializer(serializers.ModelSerializer):
    product = ProductFavouriteDetailSerializer(read_only=True)
    class Meta:
        model = FavouriteProduct
        fields = [ 'id', 'user', 'product']
    
class FavouriteProductAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteProduct
        fields = [ 'id', 'user', 'product']


   
class ProductEnquiriesSerializer(serializers.ModelSerializer):
    product = ProductFavouriteDetailSerializer(read_only=True)
    class Meta:
        model = ProductEnquiries
        fields = [ 'user','product','customer_name','phone_number','email','product_name','enquiry_for','state','city','paid',]
        


   
class ProductEnquirieFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductEnquiries
        fields = [ 'user','product','customer_name','phone_number','email','product_name','enquiry_for','state','city','paid',]
        

                  
class ProductTypeWiseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['product_type','product_data']
        depth = 2



    
class ProductNamesListSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Products
        fields = [ 'id','name']
      