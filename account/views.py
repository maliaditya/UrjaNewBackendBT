from django.shortcuts import render
# Create your views here.
from .models import Address, UserAccount, FAQ, Reports
from .serializers import AddressSerializer, UserAccountSerializer, FAQSerializer, ReportsSerializer,UserCreateSerializer,SellerAcountRegisterSerializer,UserDetailSerializer
from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import IsAuthenticated, BasePermission,AllowAny, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import filters, status
from rest_framework.decorators import permission_classes,action
import requests
import json
class AddressViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Address.objects.all()
    serializer_class =   AddressSerializer
    


class FAQViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = FAQ.objects.all()
    serializer_class =   FAQSerializer
    


class ReportsViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Reports.objects.all()
    serializer_class =   ReportsSerializer
    



class UserAccountViewSet(viewsets.GenericViewSet,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin, 
                    mixins.CreateModelMixin,):
    authentication_classes = []
    permission_classes = []
    queryset = UserAccount.objects.all()
    serializer_class =   UserAccountSerializer

    def create(self, request):
        serializer = UserAccountSerializer(data=request.data)
        if serializer.is_valid():
            print("in serializer valid")
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            phone = request.data.get('phone')
            email = request.data.get('email')
            password = request.data.get('password')
            re_password = request.data.get('password')
            body ={
                    "first_name": first_name,
                    "last_name": last_name,
                    "phone":phone,
                    "email": email,
                    "password": password,
                    "re_password": password,
                }
            print(body)
            headers = {'Content-Type': 'application/json'}

            create_user_api = 'https://urjacommercials.com/auth/users/'
            response = requests.post(create_user_api, data =body)

            return Response( response.json(), status=status.HTTP_201_CREATED)
        email = serializer.errors.get('email')
        password = serializer.errors.get('password') or "Valid"
        if password == 'Valid':
           errdata = [email[0]]
        else:
            # errdata = {"email": email[0],"password":password[0]}
            errdata = [email[0], password[0]]
       
        return Response({"message":  errdata,"status":status.HTTP_400_BAD_REQUEST})
    


class IsAppActiveViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = UserAccount.objects.all()
    serializer_class =   SellerAcountRegisterSerializer



class UserInfoViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = UserAccount.objects.all()
    serializer_class =   UserAccountSerializer

    def list(self, request):
        # self.permission_classes = []
        queryset = UserAccount.objects.all()
        serializer = UserDetailSerializer(queryset)
        email = self.request.query_params.get('email',)
        try:
            queryset = queryset.filter(email__icontains=email)
            serializer = UserDetailSerializer(queryset, many=True)
            data = serializer.data[0]
            return Response({"data":data,"status":'success'},status=status.HTTP_200_OK)
        except:
            return Response({"error":"invalid email","status":'failure'},status=status.HTTP_400_BAD_REQUEST)


