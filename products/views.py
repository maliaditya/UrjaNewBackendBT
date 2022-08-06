from django.shortcuts import render

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
class ProductsPagination(PageNumberPagination):
    page_size = 1
    max_page_size = 10


class BaseViewset( viewsets.GenericViewSet,
                    mixins.ListModelMixin, 
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin):

    authentication_classes = [JWTAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)


class PorductNameListViewset(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Products.objects.all()
    serializer_class =   ProductNamesListSerializer
    authentication_classes = []
    permission_classes = []
    


class ProductTypeWiseCategoryViewset(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = ProductType.objects.all()
    serializer_class =   ProductTypeWiseCategorySerializer
    authentication_classes = []
    permission_classes = []




class SearchProductViewset(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Products.objects.all()
    serializer_class =   ProductDetailSerializer
    authentication_classes = []
    permission_classes = []
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter,DjangoFilterBackend]
    filterset_fields = [ 'category__category_name','product_type','name','price','in_stock','total_ratings']
    search_fields = ['name','category__category_name', 'product_type__product_type', 'details']


class ProductsViewset(BaseViewset,PageNumberPagination):
    queryset = Products.objects.all()
    serializer_class =   ProductSerializer
    # permission_classes = [IsAuthenticated]
    parser_classes = (JSONParser, MultiPartParser, FormParser,)
    permission_classes_by_action = {'create': [IsAuthenticated],
                                    'list': [AllowAny],
                                    'retrive': [AllowAny],
                                    'update': [IsAuthenticated],
                                    'delete':[IsAuthenticated]}
    # filter_backends = [filters.SearchFilter,DjangoFilterBackend]
    # filterset_fields = [ 'category','product_type','name','price','in_stock','total_ratings']
    # search_fields = ['name','category__category_name', 'product_type__product_type', 'details']

    def list(self, request):
        # self.permission_classes = []
        queryset = Products.objects.all()
        name = self.request.query_params.get('name',)
        rating = self.request.query_params.get('rating')
        self.pagination_class = PageNumberPagination
    
        # self.pagination_class.page_size = 30
        category = self.request.query_params.get('category')
        product_type = self.request.query_params.get('product_type')
        verified_seller = self.request.query_params.get('verified')
        leading_seller = self.request.query_params.get('leading')

        if name is not None and rating is not None and category  is not None:
            queryset = queryset.filter(name__icontains=name).filter(category__category_name=category).filter(rating=rating)

        elif product_type is not None and category is not None :
            queryset = queryset.filter(product_type__product_type=product_type).filter(category__category_name=category)

        elif leading_seller  is not None :
            queryset = queryset.filter(company__leading_seller=leading_seller )

        elif verified_seller  is not None :
            queryset = queryset.filter(company__verified_seller=verified_seller )

        elif product_type  is not None:
            queryset = queryset.filter(product_type__product_type=product_type)

        elif category  is not None:
            print(category)
            queryset = queryset.filter(category__category_name=category)

        elif rating  is not None:
            queryset = queryset.filter(rating=rating)

        elif name  is not None:
            queryset = queryset.filter(name__icontains=name)
            
        p = self.paginate_queryset(queryset)
        serializer_class = ProductDetailSerializer(p, many=True)

        return self.get_paginated_response(serializer_class.data)
    
    def retrieve(self, request, pk=None):
        queryset = Products.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ProductDetailSerializer(user)
        return Response(serializer.data)

    
    def get_permissions(self):
        try:
            # return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
    # def create(self, request):
    #     serializer = ProductSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


    # def update(self, request, pk=None):
    #     serializer = ProductSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoriesViewset(BaseViewset):
    queryset = Categories.objects.all()
    serializer_class = CategorieSerializer
    permission_classes_by_action = {'create': [IsAuthenticated],
                                    'list': [AllowAny],
                                    'retrive': [AllowAny],
                                    'update': [IsAuthenticated],
                                    'delete':[IsAuthenticated]}

    def list(self, request):
        queryset = Categories.objects.all()
        serializer_class = CategorieSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

   
class ProductTypeViewset(BaseViewset):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    permission_classes_by_action = {'create': [IsAuthenticated],
                                    'list': [AllowAny],
                                    'retrive': [AllowAny],
                                    'update': [IsAuthenticated],
                                    'delete':[IsAuthenticated]}

    def list(self, request):
        queryset = ProductType.objects.all()
        serializer_class = ProductTypeSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

   
class ReviewViewset(BaseViewset):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class FavouriteProductViewset(BaseViewset):
    queryset = FavouriteProduct.objects.all()
    serializer_class =   FavouriteProductAddSerializer
    permission_classes_by_action = {'create': [IsAuthenticated],
                                    'list': [AllowAny],
                                    'retrive': [AllowAny],
                                    'update': [IsAuthenticated],
                                    'delete':[IsAuthenticated]}

    def list(self, request):
        queryset = FavouriteProduct.objects.all()
        serializer_class = FavouriteProductSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]


class ProductEnquiriesViewset(BaseViewset):
    queryset = ProductEnquiries.objects.all()
    serializer_class =   ProductEnquirieFormSerializer
    permission_classes_by_action = {'create': [IsAuthenticated],
                                    'list': [AllowAny],
                                    'retrive': [AllowAny],
                                    'update': [IsAuthenticated],
                                    'delete':[IsAuthenticated]}

    def list(self, request):
        queryset = ProductEnquiries.objects.all()
        serializer_class = ProductEnquiriesSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
