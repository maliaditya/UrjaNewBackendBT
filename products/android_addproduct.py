from django.shortcuts import render

from account.models import UserAccount
from company.models import Company

# Create your views here.
from .models import Products, Categories, ProductType, Review, FavouriteProduct, ProductEnquiries
from .serializers import (ProductSerializer,CategorieSerializer, ProductTypeSerializer,FavouriteProductAddSerializer,
ReviewSerializer,ProductDetailSerializer, FavouriteProductSerializer, ProductEnquiriesSerializer,ProductEnquirieFormSerializer,

ProductTypeWiseCategorySerializer, ProductNamesListSerializer)
from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import IsAuthenticated, BasePermission,AllowAny, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import filters, status
from rest_framework.decorators import permission_classes,action
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser


class BaseViewset( viewsets.GenericViewSet,
                    mixins.ListModelMixin, 
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin):

    authentication_classes = [JWTAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)

class AddProductsViewset(BaseViewset,PageNumberPagination):
    queryset = Products.objects.all()
    serializer_class =   ProductSerializer
    parser_classes = (JSONParser, MultiPartParser, FormParser,)
    permission_classes = []


    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        
        if serializer.is_valid():
            print("in prod")
     
            Products(
                name=request.data['name'],
                in_stock=True,
                details=request.data['details'],
                price=request.data['price'],
                front_image=request.FILES['front_image'],
                back_image=request.FILES['back_image'],
                extra_image=request.FILES['extra_image'],
                discount=request.data['discount'],
                created_by=UserAccount.objects.get(id=request.data['created_by']),
                category=Categories.objects.get(id=request.data['category']),
                rating=0,
                total_ratings=0,
                product_type=ProductType.objects.get(id=request.data['product_type']),
                company=Company.objects.get(id=request.data['company']),
                approved='Pending' ).save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        



    
    # def get_permissions(self):
    #     try:
    #         # return permission_classes depending on `action` 
    #         return [permission() for permission in self.permission_classes_by_action[self.action]]
    #     except KeyError: 
    #         # action is not set return default permission_classes
    #         return [permission() for permission in self.permission_classes]
