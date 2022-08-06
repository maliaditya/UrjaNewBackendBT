from django.contrib import admin
from .models import Products, Categories, ProductType, Review, FavouriteProduct, ProductEnquiries


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name','created_by','company','category','product_type','price','approved')
    list_filter = ('approved','product_type','company')



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user','product','created_at','updated_at','review','rating')




@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('category_name',)



@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('product_type',)



@admin.register(FavouriteProduct)
class FavouriteProductAdmin(admin.ModelAdmin):
    list_display = ('user','product')
    list_filter = ('user',)




@admin.register(ProductEnquiries)
class ProductEnquiriesAdmin(admin.ModelAdmin):
    list_display = ('user','product','customer_name','phone_number','email','product_name','enquiry_for','paid',)
    list_filter = ('product',)


