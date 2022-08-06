import re
from app_data.models import ActivationKeys
from app_data.serializers import ActivationKeysSerializer
from .imports import *
from django.core import serializers
import json
from account.models import UserAccount
from .stock import StockViewset

class ActivationKeysViewset(viewsets.ModelViewSet):
    queryset = ActivationKeys.objects.all()
    serializer_class = ActivationKeysSerializer
    authentication_classes = []
    permission_classes = []
    # lookup_field = 'user'

    def create(self, request, *args, **kwargs):
            queryset = SubProductsStock.objects.filter(member=request.data.get('allocated_by'))
            member = MemberAccount.objects.get(member_id=request.data.get('allocated_to'))
            allocated_by = MemberAccount.objects.get(member_id=request.data.get('allocated_by'))
            if member.is_admin:
                ActivationKeys(allocated_to=member).save()
                return Response({"message":"OK"}, status=status.HTTP_201_CREATED,)
            else:
                for i in queryset:
                    if i.quantity > 0:
                        i.quantity = i.quantity -1
                        i.save()
                        ActivationKeys(allocated_to=member,allocated_by=allocated_by).save()
                        break
                    else:
                        continue
                return Response({"message":"OK"}, status=status.HTTP_201_CREATED,)
    
    @action(detail=False, methods=['post'])
    def subproduct_update(self, request):
        queryset = SubProductsStock.objects.filter(member=request.data.get('member_id'))
        member_id = MemberAccount.objects.get(member_id=request.data.get('member_id'))
        seller = ActiveSeller.objects.get(seller=member_id)
        # update product quantity and bonus_points
        print("in  partial_update")
        for i in queryset:
                    if i.quantity > 0:
                        i.quantity = i.quantity + 1
                        if seller.subproduct_bonus_points > 200 :
                            seller.subproduct_bonus_points -= 200
                            seller.save()
                            i.save()
                        else:
                            return Response({"message":"insufficent Bonus Points"}, status=status.HTTP_412_PRECONDITION_FAILED,)
                        break
                    else:
                        continue
        return Response({"message":"OK"}, status=status.HTTP_201_CREATED,)
    
    @action(detail=False, methods=['get'])
    def get_subproduct_bonus_points(self, request):
        member = request.query_params.get('member',)
        if member is not None:
            member_id = MemberAccount.objects.get(member_id=request.query_params.get('member'))
            seller = ActiveSeller.objects.get(seller=member_id)
            return Response({"sub_product_bonus_points":seller.subproduct_bonus_points}, status=status.HTTP_200_OK)
        else:
            return Response({"message":"Bad request"}, status=status.HTTP_400_BAD_REQUEST)


        

    def list(self, request):
        # self.permission_classes = []
        member = request.query_params.get('member',)
        seller = request.query_params.get('seller',)
        if member is not None:
            queryset = ActivationKeys.objects.filter(allocated_to=member)
            serializer_class = ActivationKeysSerializer(queryset, many=True)
            return Response(serializer_class.data)
        elif seller is not None:
            print("in seller ")
            queryset = ActivationKeys.objects.filter(allocated_by=seller)
            serializer_class = ActivationKeysSerializer(queryset, many=True)
            return Response(serializer_class.data)
        else:
            queryset = ActivationKeys.objects.all()
            serializer_class = ActivationKeysSerializer(queryset, many=True)
            return Response(serializer_class.data)

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class DistrictViewset(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    authentication_classes = []
    permission_classes = []

class SubProductsSaleViewset(viewsets.ModelViewSet):
    queryset = SubProductsSale.objects.all()
    serializer_class = SubProductsSaleSerializer
    authentication_classes = []
    permission_classes = []



class TalukaViewset(viewsets.ModelViewSet):
    queryset = Taluka.objects.all()
    serializer_class =TalukaSerializer
    authentication_classes = []
    permission_classes = []

class CityViewset(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    authentication_classes = []
    permission_classes = []



class BankDetailsViewset(viewsets.ModelViewSet):
    queryset = BankDetails.objects.all()
    serializer_class = BankDetailsSerializer
    authentication_classes = []
    permission_classes = []


    def list(self, request):
        member = request.query_params.get('member')
        if member is None:
            queryset = BankDetails.objects.all()
            serializer_class = BankDetailsSerializer(queryset, many=True)
            return Response(serializer_class.data)
        else:
            queryset = BankDetails.objects.get(member=member)
            serializer_class = BankDetailsSerializer(queryset)
            return Response(serializer_class.data)




class OrderDetailsViewset(viewsets.ModelViewSet):
    queryset = OrderDetails.objects.all()
    serializer_class = OrderDetailsSerializer
    authentication_classes = []
    permission_classes = []
    # filter_backends = [filters.SearchFilter,DjangoFilterBackend]
    # filterset_fields = [ 'member']
    # search_fields = ['member']
    
    # def partial_update(self, request, pk):
    #     serializer = self.get_serializer(data=request.data)
    #     id = request.data.get('id')
    #     q = OrderDetails.objects.get(id=id)
    #     print(q.order)
    #     q.quantity_delivered = 
    #     print(q.quantity)
    #     quantity_delivered = request.data.get('quantity_delivered')
    #     return Response({"data": request.data, "pk":pk})

class LevelViewset(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    authentication_classes = []
    permission_classes = []

    def list(self, request):
        print(Level.objects.get(id=1).points)
        queryset = Level.objects.all()
        serializer_class = LevelSerializer(queryset, many=True)
        return Response(serializer_class.data)

class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = []
    permission_classes = []
    # lookup_field = 'orded_by'
    
    def list(self, request):
        # self.permission_classes = []
        queryset = Order.objects.all()
        orded_by = self.request.query_params.get('member',)
        self.pagination_class = PageNumberPagination

        if orded_by  is not None:
            queryset = queryset.filter(orded_by=orded_by)
            
        p = self.paginate_queryset(queryset)
        serializer_class = OrderListSerializer(p, many=True)

        return self.get_paginated_response(serializer_class.data)

    
class ImageViewset(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    authentication_classes = []
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

class AddProductViewset(viewsets.ModelViewSet):
    queryset = AddProduct.objects.all()
    serializer_class = AddProductSerializer
    authentication_classes = []
    permission_classes = []
    # pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter,DjangoFilterBackend]
    filterset_fields = [ 'is_package_product', 'is_package']
    search_fields = ['is_package_product', 'is_package']
        
class MemberAccountViewset(viewsets.GenericViewSet,mixins.CreateModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin):
    queryset = MemberAccount.objects.all()
    serializer_class = MemberAccountSerializer
    authentication_classes = []
    permission_classes = []

    def list(self, request):
        queryset = MemberAccount.objects.all()
        serializer_class = MemberAccountListSerializer(queryset, many=True)
        return Response(serializer_class.data,status=status.HTTP_400_BAD_REQUEST)

class ActiveMemberViewset(viewsets.ModelViewSet):
    queryset = ActiveMember.objects.all()
    serializer_class = ActiveMemberSerializer
    authentication_classes = []
    permission_classes = []
    # lookup_field = 'user'

class BinaryTreeViewset(viewsets.ModelViewSet):
    queryset = BinaryTree.objects.all()
    serializer_class = BinaryTreeSerializer
    authentication_classes = []
    permission_classes = []

class SubProductsStockViewset(viewsets.ModelViewSet):
    queryset = SubProductsStock.objects.all()
    serializer_class = SubProductsStockSerializer
    authentication_classes = []
    permission_classes = []
    # lookup_field = 'user'
    def list(self, request):
        # self.permission_classes = []
        member = request.query_params.get('member',)
        if member is None:
            queryset = SubProductsStock.objects.all()
            serializer_class = SubProductsStockSerializer(queryset, many=True)
            return Response(serializer_class.data)
        else:
            queryset = SubProductsStock.objects.filter(member=member)
            serializer_class = SubProductsStockSerializer(queryset, many=True)
            return Response(serializer_class.data)

class IntroducerViewset(viewsets.ModelViewSet):
    queryset = Introducer.objects.all()
    serializer_class = IntroducerSerializer
    authentication_classes = []
    permission_classes = []
    lookup_field = 'user'
    def list(self, request):
        queryset = Introducer.objects.all()
        serializer_class = IntroducerListSerializer(queryset, many=True)
        return Response(serializer_class.data)
    def create(self, request):
        introducer=request.data.get('introducer')
        distributer=request.data.get('distributer')
        try:
            introducer = MemberAccount.objects.get(member_id=introducer)
            distributer =MemberAccount.objects.get(member_id=distributer)
            IntroducerRequests(introducer=introducer, distributer=distributer,pin_code=distributer.pin_code).save()
            return Response({"message":"Your request is success full sent"},status=status.HTTP_200_OK)
        except:
            return Response({"message":"invalid request distributer id already exists"},status=status.HTTP_409_CONFLICT)

@api_view(['GET'])
@permission_classes([])
def count(request):

    if request.method == 'GET':
        members = MemberAccount.objects.all().count()
        active_members = ActiveMember.objects.filter(is_active=True).count()
        distributers = ActiveCityDistibuter.objects.filter(is_active=True).count()
        sellers =ActiveSeller.objects.filter(is_active=True).count()
        body = {
            "members":members,
            "active_members":active_members,
            "distributers":distributers,
            "sellers":sellers
        }
        return Response(body)



@api_view(['GET'])
@permission_classes([])
def admin(request):

    if request.method == 'GET':
        admin = MemberAccount.objects.get(is_admin=True)
        body = {
            "admin":admin.member_id,
        }
        return Response(body)   


@api_view(['GET'])
@permission_classes([])
def member(request):

    if request.method == 'GET':
        member_id = request.query_params.get('member')
        try:
            member = MemberAccount.objects.filter(member_id__icontains=member_id)
            print(member.count())
            if member.count() == 1:
                body = {
                    "member_name":member[0].get_user_name,
                    "member_id":member[0].member_id,
                }
                return Response(body,status=status.HTTP_200_OK) 
            else:
                body = {
                "message":"member does not exists"
                     }
                return Response(body,status=status.HTTP_404_NOT_FOUND)   
            
        except:
            body = {
                "message":"member does not exists"
            }
            return Response(body,status=status.HTTP_404_NOT_FOUND)   



@api_view(['GET'])
@permission_classes([])
def mbw_user_details(request):

    if request.method == 'GET':
        member_id = request.query_params.get('member')
        try:
            member = MemberAccount.objects.get(member_id=member_id)
            user = UserAccount.objects.get(email=member.user)
            seller = ActiveSeller.objects.get(seller=member)
            activemember = ActiveMember.objects.get(member=member)
            distributer = ActiveCityDistibuter.objects.get(distributer=member)
            try:
                bank = BankDetails.objects.get(member=member)
                body = {
                    "member_name": user.first_name +" "+  user.last_name ,
                    "email":user.email,
                    "phone":user.phone,
                    "distributer":distributer.is_active,
                    "seller":seller.is_active,
                    "member":activemember.is_active,
                    "member_id":member.member_id,
                    "bank_details":{
                        "bank_name":bank.bank_name,
                        "bank_branch":bank.bank_branch,
                        "bank_account":bank.bank_account,
                        "upi":bank.upi,
                        "bank_ifsc": bank.bank_ifsc,
                        "nominee":bank.nominee,
                    }
                }
            except: body = {
                    "member_name": user.first_name +" "+  user.last_name ,
                    "email":user.email,
                    "phone":user.phone,
                    "distributer":distributer.is_active,
                    "seller":seller.is_active,
                    "member":activemember.is_active,
                    "member_id":member.member_id,
                    "bank_details":False}
            return Response(body,status=status.HTTP_200_OK) 
        except:
            body = {
                "message":"member does not exists"
            }
            return Response(body,status=status.HTTP_404_NOT_FOUND)   


@api_view(['GET'])
@permission_classes([])
def member_info(request):

    if request.method == 'GET':
        user = request.query_params.get('user')
        try:
            member = MemberAccount.objects.get(user=user)
            is_Active = ActiveMember.objects.get(member=member).is_active
            body = {
                "member_name":member.get_user_name,
                "member_id":member.member_id,
                "is_active":is_Active
            }
            return Response(body,status=status.HTTP_200_OK)   
        except:
            body = {
                "message":"member does not exists"
            }
            return Response(body,status=status.HTTP_404_NOT_FOUND)   



@api_view(['GET'])
@permission_classes([])
def seller_dashboard(request):

    if request.method == 'GET':
        user = request.query_params.get('user')
        try:
            mysales = Sale.objects.filter(seller=user).count()
            my_driect = MemberAccount.objects.filter(sponser_id=user).count()
            member = MemberAccount.objects.filter(sponser_id=user)
            seller = ActiveSeller.objects.get(seller=user)
            activedistributer  =  ActiveCityDistibuter.objects.get(distributer=user)
            activemember  =  ActiveMember.objects.get(member=user)
            body = {
                                "bonus_points":seller.bonus_points,
                                "mysales": mysales,
                                "my_driect":my_driect,
                                "activedistributer":365-activedistributer.days,
                                "activemember":365-activemember.days,
                                "activeseller":30-seller.days,
                            }   
          
            if(365-activedistributer.days<0 and 365-activemember.days<0 and 30-seller.days<0):
                seller = ActiveSeller.objects.get(seller=user)
                seller.is_active = False
                seller.save()

                activedistributer  =  ActiveCityDistibuter.objects.get(distributer=user)
                activedistributer.is_active = False
                activedistributer.save()

                activemember  =  ActiveMember.objects.get(member=user)
                activemember.is_active = False
                activemember.save()
                body = {
                                "bonus_points":seller.bonus_points,
                                "mysales": mysales,
                                "my_driect":my_driect,
                                "activedistributer":365-activedistributer.days,
                                "activemember":365-activemember.days,
                                "activeseller":30-seller.days,
                            }   
                return Response(body)   
            elif(365-activedistributer.days<0 and 365-activemember.days<0 ):
                
                activedistributer  =  ActiveCityDistibuter.objects.get(distributer=user)
                activedistributer.is_active = False
                activedistributer.save()

                activemember  =  ActiveMember.objects.get(member=user)
                activemember.is_active = False
                activemember.save()
                body = {
                                "bonus_points":seller.bonus_points,
                                "mysales": mysales,
                                "my_driect":my_driect,
                                "activedistributer":365-activedistributer.days,
                                "activemember":365-activemember.days,
                                "activeseller":30-seller.days,
                            }   
                return Response(body)   

            elif(365-activedistributer.days<0 and  30-seller.days<0):
                
                seller = ActiveSeller.objects.get(seller=user)
                seller.is_active = False
                seller.save()

                activedistributer  =  ActiveCityDistibuter.objects.get(distributer=user)
                activedistributer.is_active = False
                activedistributer.save()
                body = {
                                "bonus_points":seller.bonus_points,
                                "mysales": mysales,
                                "my_driect":my_driect,
                                "activedistributer":365-activedistributer.days,
                                "activemember":365-activemember.days,
                                "activeseller":30-seller.days,
                            }   
                return Response(body)   

            elif(365-activemember.days<0 and  30-seller.days<0):
                
                seller = ActiveSeller.objects.get(seller=user)
                seller.is_active = False
                seller.save()

                activemember  =  ActiveMember.objects.get(member=user)
                activemember.is_active = False
                activemember.save()
                body = {
                                "bonus_points":seller.bonus_points,
                                "mysales": mysales,
                                "my_driect":my_driect,
                                "activedistributer":365-activedistributer.days,
                                "activemember":365-activemember.days,
                                "activeseller":30-seller.days,
                            }   
                return Response(body)   

            elif(365-activedistributer.days<0):
                
                activedistributer  =  ActiveCityDistibuter.objects.get(distributer=user)
                activedistributer.is_active = False
                activedistributer.save()
                body = {
                                "bonus_points":seller.bonus_points,
                                "mysales": mysales,
                                "my_driect":my_driect,
                                "activedistributer":365-activedistributer.days,
                                "activemember":365-activemember.days,
                                "activeseller":30-seller.days,
                            }   
                return Response(body)  
            elif( 365-activemember.days<0):

                activemember  =  ActiveMember.objects.get(member=user)
                activemember.is_active = False
                activemember.save()
                body = {
                                "bonus_points":seller.bonus_points,
                                "mysales": mysales,
                                "my_driect":my_driect,
                                "activedistributer":365-activedistributer.days,
                                "activemember":365-activemember.days,
                                "activeseller":30-seller.days,
                            }   
                return Response(body)    

            elif( 30-seller.days<0):
                
                seller = ActiveSeller.objects.get(seller=user)
                seller.is_active = False
                seller.save()
                body = {
                                "bonus_points":seller.bonus_points,
                                "mysales": mysales,
                                "my_driect":my_driect,
                                "activedistributer":365-activedistributer.days,
                                "activemember":365-activemember.days,
                                "activeseller":30-seller.days,
                            }   
                return Response(body)  
        except:
            body = {
                "message":"member does not exists"
            }
        return Response(body)  
       

class ActiveSellerViewset(viewsets.ModelViewSet):
    queryset = ActiveSeller.objects.all()
    serializer_class = ActiveSellerSerializer
    authentication_classes = []
    permission_classes = []
    lookup_field = 'seller'

@api_view(['GET'])
@permission_classes([])
def direct_members(request):
    if request.method == 'GET':
        user = request.query_params.get('user')
        try:
            my_list = []
            all_direct_members = MemberAccount.objects.filter(sponser_id=user)
            for i in all_direct_members:
                member = ActiveMember.objects.get(member =MemberAccount.objects.get(member_id=i.member_id))
                my_list.append({"member_id": i.member_id,"is_active_member":member.is_active,"name":i.get_user_name})
            my_direct = serializers.serialize('json', list(MemberAccount.objects.filter(sponser_id=user))) 
            my_direct = json.loads(my_direct)
            body = {
                "my_direct":my_list
            }   
        except:
            body = {
                "message":"member does not exists"
            }
        return Response(body)   





@api_view(['GET'])
@permission_classes([])
def get_introducer(request):
    if request.method == 'GET':
        member_id = request.query_params.get('member')
        try:
            m = MemberAccount.objects.get(member_id=member_id)
            member = Introducer.objects.get(distributer=m)
            introducer = MemberAccount.objects.get(member_id=str(member.get_introducer))
            body = {
                    "introducer": introducer.get_user_name
                }
            return Response(body,status=status.HTTP_200_OK) 
        except:
            body = {
                "message":"member does not exists"
            }
            return Response(body,status=status.HTTP_404_NOT_FOUND)   







@api_view(['GET'])
@permission_classes([])
def get_distributers(request):
    if request.method == 'GET':
        member_id = request.query_params.get('member')
        try:
            m = MemberAccount.objects.get(member_id=member_id)
            members = Introducer.objects.filter(introducer=m)
            my_list = []
            for i in members:
                distributer = MemberAccount.objects.get(member_id=str(i.get_distributer))
                is_Active = ActiveCityDistibuter.objects.get(distributer=distributer)
                print(is_Active.is_active)
                my_list.append({"name":distributer.get_user_name,"is_Active": is_Active.is_active})
            body = {
                    "distributers":my_list,
                    
                    
                }
            return Response(body,status=status.HTTP_200_OK) 
        except:
            body = {
                "message":"member does not exists"
            }
            return Response(body,status=status.HTTP_404_NOT_FOUND)   



