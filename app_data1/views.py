from django.shortcuts import render
from .models import ActiveUser,SOS,ActivationKeys
from .serializers import ActiveUserSerializer,SOSSerializer
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
import requests
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from chain_marketing_app.models import MemberAccount
from chain_marketing_app.serializers import MemberAccountSerializer
from django.core import serializers
from account.models import UserAccount
import json




class ActiveUserViewset(viewsets.ModelViewSet):
    queryset = ActiveUser.objects.all()
    serializer_class = ActiveUserSerializer
    authentication_classes = []
    permission_classes = []
    lookup_field = 'user'

    def create(self, request):
        serializer = ActiveUserSerializer(data=request.data)
        if serializer.is_valid():
            data=request.data

            print(data['activation_key'])
            queryset = ActivationKeys.objects.all()
            if queryset.filter(activation_key=data['activation_key']).exists():
                get_key = ActivationKeys.objects.get(activation_key=data['activation_key'])
                if get_key.is_active:
                    return Response({'errors':'activation key already used',"status":'failure'},status=status.HTTP_200_OK)
                else:
                    get_key.is_active = True
                    get_key.save()
                    serializer.save()
                    return Response({"data":serializer.data,"status":'success'},status=status.HTTP_200_OK)
            elif data['activation_key']=='12345678':
                try:
                    existing_user = ActiveUser.objects.get(user=data['user'])
                    existing_user.free_service_balance = 2
                    existing_user.paid_service_balance = 0
                    existing_user.save()
                except:    
                    ActiveUser(activation_key= data['activation_key'],is_active=True,paid_service_balance=0,free_service_balance=2,user=UserAccount.objects.get(id=data['user'])).save()
                return Response({"data":serializer.data,"status":'success'},status=status.HTTP_200_OK)          
            else:
                return Response({'errors':'invalid activation key',"status":'failure'},status=status.HTTP_400_BAD_REQUEST)
        
            
    # def retrieve(self, request, pk=None):
    #     queryset = Products.objects.all()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = ProductDetailSerializer(user)
    #     return Response(serializer.data)


class SMSViewset(viewsets.ModelViewSet):
    queryset = SOS.objects.all()
    serializer_class = SOSSerializer
    authentication_classes = []
    permission_classes = []

    def create(self, request):
        serializer = SOSSerializer(data=request.data)
        data = request.data
        sms_type = request.data.get('acctype')
        user_queryset = ActiveUser.objects.get(user=data['user'])
        data = request.data
        user_queryset = ActiveUser.objects.get(user=data['user'])
        if user_queryset.days < 356:
            q = UserAccount.objects.get(id=data['user'])
            user_queryset1 = ActiveUser.objects.all()
            user_active_info =serializers.serialize('json', list(user_queryset1.filter(user=data['user'])))
            user_data = json.loads(user_active_info)
            user_data = user_data[0]
            user_filter_data = user_data['fields']

            if sms_type == 'demo' and user_queryset.free_service_balance != 0 :
                user_queryset.free_service_balance -= 1
                user_queryset.save()
                print("my data is",request.data)
                listToStr = data['receivernumber']
                longitude = f",{data['longitude']}"
                message = f"Alert, your friend {q.first_name} could be in trouble. Please assist {q.first_name} by checking in at his/her live location http://www.google.com/maps/place/{data['latitude']}{longitude} and assist him. Urja Commercials Team."
                url = f"https://sms.visionhlt.com/api/mt/SendSMS?apikey=hVDIBiOyuEWsCcKTn5i50g&senderid=URJAEC&channel=Trans&DCS=0&flashsms=0&number={listToStr}&text={message}"
                response = requests.request("GET", url)
                data = response.json()
                return Response({'response':data,"status":"success"},status=status.HTTP_200_OK)

            elif sms_type == 'activate' and user_queryset.paid_service_balance != 0 :
                user_queryset.paid_service_balance -= 1
                user_queryset.save()
                print("my data is",request.data)
                listToStr = data['receivernumber']
                longitude = f",{data['longitude']}"
                message = f"Alert, your friend {q.first_name} could be in trouble. Please assist {q.first_name} by checking in at his/her live location http://www.google.com/maps/place/{data['latitude']}{longitude} and assist him. Urja Commercials Team."
                url = f"https://sms.visionhlt.com/api/mt/SendSMS?apikey=hVDIBiOyuEWsCcKTn5i50g&senderid=URJAEC&channel=Trans&DCS=0&flashsms=0&number={listToStr}&text={message}"
                response = requests.request("GET", url)
                data = response.json()
                # return Response({'numbers':listToStr,'response':data,'user_data':user_filter_data,'message':message,"status":"success"})
                return Response({'response':data,"status":"success"},status=status.HTTP_200_OK)
            else:
                return Response({'message':"Insufficient SMS Balance","status":"failure"},status=status.HTTP_200_OK)
        else:
            return Response({'message':"User Activation Expired","status":"failure"},status=status.HTTP_200_OK)




        



        
