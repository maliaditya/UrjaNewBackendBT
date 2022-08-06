
from app_data.models import ActivationKeys
from chain_marketing_app.models import ActiveCityDistibuter, Level
from chain_marketing_app.models import AddProduct, MemberAccount,ActiveMember,ActiveSeller,OrderDetails,AdminAccounts
from chain_marketing_app.models import  Sale,Payout
from chain_marketing_app.serializers import (SaleSerializer, LevelSerializer, SaleListSerializer)
from rest_framework import mixins, status, viewsets,filters
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import json
from django.core import serializers
from django_filters.rest_framework import DjangoFilterBackend
from .imports import *

class SaleViewset(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    authentication_classes = []
    permission_classes = []

    MAX_PAYOUT = 0
    DISTRIBUTED_PAYOUT = 0
    OUTSANTDING = 0
    BONUS = 0
    TDS = 0
    STD = 0
    PRODUCT = 0

    # def allocate_binary_tree_points(self, member,product):
    #     btmember = BinaryTree.objects.get(member=member)
    #     btmember.is_active = True
    #     btmember.save()
    #     # btmember = BinaryTree.objects.get(member=btmember.parent)
    #     while btmember.is_admin != True:
    #         # print(btmember.parent)
    #         temp = btmember
    #         btmember = BinaryTree.objects.get(member=btmember.parent)
    #         print("Left = ",btmember.left, "Right = ",btmember.right,temp) 
            
    #         if str(btmember.left) == str(temp):
    #             mem = BinaryTree.objects.get(member=btmember.left)
    #             if mem.is_active:
    #                 mem.left_points += product.points_to_buyer
    #                 mem.save()
    #         if str(btmember.right) == str(temp):
    #             mem = BinaryTree.objects.get(member=btmember.right)
    #             if  mem.is_active:
    #                 mem.right_points += product.points_to_buyer
    #                 mem.save()

    def allocate_binary_tree_points(self, member,product):
        btmember = BinaryTree.objects.get(member=member)
        btmember.is_active = True
        btmember.save()
        btmember_parent = BinaryTree.objects.get(member=btmember.parent)
        while btmember_parent.is_admin != True:
            # print(btmember.parent)
            # print("btmember_parent = ",btmember_parent,"Left = ",btmember_parent.left," : ",str(btmember_parent.left) == str(btmember), "Right = ",btmember_parent.right," : ",str(btmember_parent.right)  == str(btmember)," btmember = " , btmember)
            if str(btmember_parent.left) == str(btmember):
                mem = BinaryTree.objects.get(member=btmember.parent)
                if mem.is_active:
                    mem.left_points += product.points_to_buyer
                    mem.save()
            if str(btmember_parent.right) == str(btmember):
                mem = BinaryTree.objects.get(member=btmember.parent)
                if  mem.is_active:
                    mem.right_points += product.points_to_buyer
                    mem.save()
            btmember = btmember_parent
            btmember_parent = BinaryTree.objects.get(member=btmember_parent.parent)
            


        # print(member, product)
        
    def is_active_distributer(self,member):
        activedistributer  =  ActiveCityDistibuter.objects.get(distributer=member.distributer.member_id)
        if activedistributer.is_active and activedistributer.days  > 365:
            activedistributer.is_active = False
            return False
        elif activedistributer.is_active and activedistributer.days  < 365:
            return True
        else:
            return False

    def is_active_seller(self,member):
        activeseller  =  ActiveSeller.objects.get(seller=member.member_id)
        if activeseller.is_active and activeseller.days > 30:
            activeseller.is_active = False
            return False
        elif activeseller.is_active and activeseller.days < 30:
            return True
        else:
            return False

    def is_active_member(self,member):
        activemember  =  ActiveMember.objects.get(member=member.member_id)
        if activemember.is_active  and activemember.days > 365:
            activemember.is_active = False
            return False
        elif activemember.is_active and activemember.days  < 365:
            return True
        else:
            return False

    def generate_distributers_payout(self,member,points,tds,std_deduction):
        try:
            queryset = ActiveCityDistibuter.objects.filter(pin_code=member.pin_code).get(is_active=True)
            if self.is_active_distributer(queryset):
                if queryset:
                    distributer = MemberAccount.objects.get(member_id=queryset.distributer.member_id)
                    tds_payout = points*tds/100
                    std_payout =points*std_deduction/100
                    payout = points - tds_payout - std_payout
                    self.DISTRIBUTED_PAYOUT += points
                    self.OUTSANTDING -= points
                    self.TDS += points -( points - tds_payout) 
                    self.STD += points - (points - std_payout)
                    Payout( member=distributer,
                            from_member =distributer,
                            type = 'service office',
                            name=distributer.get_user_name,
                            points=points,
                            tds=tds,
                            std_deduction=std_deduction,
                            payout=payout
                            ).save()
                    try:
                        introducera = Introducer.objects.get(distributer=distributer.member_id)
                    except:
                        return
                    introducermem = MemberAccount.objects.get(member_id=introducera.get_introducer)
                    introducer = ActiveCityDistibuter.objects.get(distributer=introducera.get_introducer).is_active
                    if introducer:
                        tds_payout = points*tds/100
                        std_payout =points*std_deduction/100
                        payout = points - tds_payout - std_payout
                        self.DISTRIBUTED_PAYOUT += points
                        self.OUTSANTDING -= points
                        self.TDS += points -( points - tds_payout) 
                        self.STD += points - (points - std_payout)
                        Payout( member=introducermem,
                                from_member =distributer,
                                type = 'introducer',
                                name=introducermem.get_user_name,
                                points=points,
                                tds=tds,
                                std_deduction=std_deduction,
                                payout=payout
                                ).save()
                    else:
                            tds_payout = points*tds/100
                            std_payout =points*std_deduction/100
                            payout = points - tds_payout - std_payout
                            introducer_payout = payout*25/100
                            if self.is_active_member(introducermem):
                                self.DISTRIBUTED_PAYOUT += points
                                self.OUTSANTDING -= points
                                self.TDS += points -( points - tds_payout) 
                                self.STD += points - (points - std_payout)
                                Payout( member=introducermem,
                                    from_member =distributer,
                                    type = 'introducer',
                                    name=introducermem.get_user_name,
                                    points=points*25/100,
                                    tds=tds,
                                    std_deduction=std_deduction,
                                    payout=introducer_payout
                                    ).save()        
            else:
                    return

        except ActiveCityDistibuter.DoesNotExist:
            distributer = MemberAccount.objects.get(is_admin=True)
            tds_payout = points*tds/100
            std_payout =points*std_deduction/100
            payout = points - tds_payout - std_payout
            # self.DISTRIBUTED_PAYOUT += points
            # self.OUTSANTDING -= points
            # self.TDS += points - tds_payout 
            # self.STD += points - std_payout
            
    def activate_ditributer(self,member):
        #get member id of the member
        #update is active to true in city ditributer Class
        queryset = ActiveCityDistibuter.objects.get(distributer=member.member_id)
        queryset.is_active = True
        queryset.save()

    def allot_bonus_points_to_sponser_seller(self,member_id,product):
        sponser = MemberAccount.objects.get(member_id=member_id)
        sponser_is_active = ActiveSeller.objects.get(seller=sponser.member_id).is_active

        if sponser_is_active:
            sponser_is_active = ActiveSeller.objects.get(seller=sponser.member_id) 
            sponser_is_active.bonus_points += product.seller_bonus
            self.BONUS += product.seller_bonus
            sponser_is_active.save()
        else:
            while  sponser_is_active != True :
                if sponser.is_admin:
                    break
                sponser = MemberAccount.objects.get(member_id=sponser.sponser_id)
                sponser_is_active = ActiveSeller.objects.get(seller=sponser.member_id).is_active
            sponser_is_active = ActiveSeller.objects.get(seller=sponser.member_id)
            sponser_is_active.bonus_points +=  product.seller_bonus
            self.BONUS += product.seller_bonus
            sponser_is_active.save()
    
    def activate_seller(self,member,product):
        #get member id of the member
        #update is active to true in ActiveSeller Class
        queryset = ActiveSeller.objects.get(seller=member.member_id)
        queryset.is_active = True
        queryset.subproduct_bonus_points = 650
        queryset.save()
        self.allot_bonus_points_to_sponser_seller(member.sponser_id,product)

    def activate_member(self,member):
        #get member id of the member
        #update is active to true in ActiveMember Class
        queryset = ActiveMember.objects.get(member=member.member_id)
        queryset.is_active = True
        queryset.save()

    def check_product_type(self, product,member):
        # code
        if product.product_type == 'seller':
            self.activate_seller(member,product)
        elif product.product_type == 'member':
            self.activate_member(member)
        elif product.product_type  == 'distributer':
            self.activate_ditributer(member)

    def generate_seller_payout(self,member,product_id,levels,tds,std_deduction):
        # code
        sponser = MemberAccount.objects.get(member_id=member.sponser_id)
        sponser_is_active =self.is_active_seller(sponser)
        counter = 0
        while(counter<levels):
            if sponser.is_admin:
                points = self.get_level_points(product_id,counter+1).points
                tds_payout = points*tds/100
                std_payout =points*std_deduction/100
                payout = points - tds_payout - std_payout
                # self.DISTRIBUTED_PAYOUT += points
                # self.OUTSANTDING -= points
                # self.TDS += points - tds_payout 
                # self.STD += points - std_payout
                counter += 1
                continue
            elif sponser_is_active == True:
                points = self.get_level_points(product_id,counter+1).points
                tds_payout = points*tds/100
                std_payout =points*std_deduction/100
                payout = points - tds_payout - std_payout
                self.DISTRIBUTED_PAYOUT += points
                self.OUTSANTDING -= points
                self.TDS += points -( points - tds_payout) 
                self.STD += points - (points - std_payout)
                if sponser_is_active:
                    Payout( member=sponser,
                            from_member =member,
                            type = 'leadership',
                            name=sponser.get_user_name,
                            points=points,
                            tds=tds, 
                            std_deduction=std_deduction,
                            payout=payout
                            ).save()
                    sponser = MemberAccount.objects.get(member_id=sponser.sponser_id)
                    sponser_is_active = self.is_active_seller(sponser)
                    counter += 1

            elif not sponser_is_active:
                points = self.get_level_points(product_id,counter+1).points
                while  sponser_is_active != True :
                    if sponser.is_admin:
                        break
                    else:
                        sponser = MemberAccount.objects.get(member_id=sponser.sponser_id)
                        sponser_is_active = self.is_active_seller(sponser)
                if sponser_is_active:
                    tds_payout = points*tds/100
                    std_payout =points*std_deduction/100
                    payout = points - tds_payout - std_payout
                   
                    if sponser_is_active:
                        self.DISTRIBUTED_PAYOUT += points
                        self.OUTSANTDING -= points
                        self.TDS += points -( points - tds_payout) 
                        self.STD += points - (points - std_payout)
                        Payout( member=sponser,
                                from_member =member,
                                type = 'leadership',
                                name=sponser.get_user_name,
                                points=points,
                                tds=tds, 
                                std_deduction=std_deduction,
                                payout=payout
                                ).save()
                        sponser = MemberAccount.objects.get(member_id=sponser.sponser_id)
                        sponser_is_active = self.is_active_seller(sponser)
                        counter += 1
#************************************************************************************************
#*************** GET Total Active Direct ******************************
#**********************************************************************************************************
    def get_total_active_direct(self, sponser):
        count = 0 # Count of all direct members set to zero
        all_direct_members = MemberAccount.objects.filter(sponser_id=sponser.member_id)  # Get all direct members of sponser
        if MemberAccount.objects.filter(sponser_id=sponser.member_id).count()>=3:
            for i in all_direct_members :
                if ActiveMember.objects.get(member =MemberAccount.objects.get(member_id=i.member_id)).is_active:
                    count = count + 1    #Increase count if direct is active
        return count

#************************************************************************************************
#       *********************************** 25 Active Bonus ********************************
#************************************************************************************************

    def generate_sponser_bonus_payout(self,member,tds,std_deduction,product):
        # code
        sponser = MemberAccount.objects.get(member_id=member.sponser_id) # Get Sponser of member
        sponser_is_active = self.is_active_member(member=sponser) # Check sponser is Active Member
        sponser_is_active = self.is_active_seller(member=sponser) # function call to check sponser is Active Seller
        
        if sponser_is_active and self.get_total_active_direct(sponser) >= 25:
            tds_payout = product.active25_bonus*tds/100
            std_payout =product.active25_bonus*std_deduction/100
            payout = product.active25_bonus - tds_payout - std_payout
            self.DISTRIBUTED_PAYOUT += product.active25_bonus
            self.OUTSANTDING -= product.active25_bonus
            self.TDS +=product.active25_bonus-(product.active25_bonus - tds_payout) 
            self.STD += product.active25_bonus-( product.active25_bonus - std_payout)
            Payout( member=sponser,
                            name=sponser.get_user_name,
                            from_member =member,
                            type = ' 25 active member bonus payout',
                            points=product.active25_bonus,
                            tds=tds, 
                            std_deduction=std_deduction,
                            payout=payout
                            ).save()
        else:
            sponser_is_active = False
            while  sponser_is_active != True :
                if sponser.is_admin:
                    break
                sponser = MemberAccount.objects.get(member_id=sponser.sponser_id)
                sponser_is_active = self.is_active_member(member=sponser) # Check sponser is Active Member
                sponser_is_active = self.is_active_seller(member=sponser) # check sponser is Acitve Seller
                if sponser_is_active:
                    if self.get_total_active_direct(sponser) < 25:
                         sponser_is_active = False
                    else: 
                        tds_payout = product.active25_bonus*tds/100
                        std_payout =product.active25_bonus*std_deduction/100
                        payout = product.active25_bonus - tds_payout - std_payout
                        self.DISTRIBUTED_PAYOUT += product.active25_bonus
                        self.OUTSANTDING -= product.active25_bonus
                        self.TDS +=product.active25_bonus-(product.active25_bonus - tds_payout) 
                        self.STD += product.active25_bonus-( product.active25_bonus - std_payout)
                        Payout( member=sponser,
                                name=sponser.get_user_name,
                                from_member =member,
                                type = ' 25 active member bonus payout',
                                points=product.active25_bonus,
                                tds=tds, 
                                std_deduction=std_deduction,
                                payout=payout
                                ).save()                                              

    def generate_sponser_payout(self,member, points,tds,std_deduction):
        # code
        try:
            sponser = MemberAccount.objects.get(member_id=member.sponser_id)
            sponser_is_active = self.is_active_member(member=sponser)
            if sponser_is_active: 
                
                tds_payout = points*tds/100
                std_payout =points*std_deduction/100
                payout = points - tds_payout - std_payout
                self.DISTRIBUTED_PAYOUT += points
                self.OUTSANTDING -= points
                self.TDS += points - (points - tds_payout)  
                self.STD += points - (points - std_payout)  
                Payout( member=sponser,
                        name=sponser.get_user_name,
                        from_member =member,
                        type = 'direct',
                        points=points,
                        tds=tds, 
                        std_deduction=std_deduction,
                        payout=payout
                        ).save()
            else:
                while  sponser_is_active != True :
                    sponser = MemberAccount.objects.get(member_id=sponser.sponser_id)
                    sponser_is_active = self.is_active_member(member=sponser)
                    
                tds_payout = points*tds/100
                std_payout =points*std_deduction/100
                payout = points - tds_payout - std_payout
                self.DISTRIBUTED_PAYOUT += points
                self.OUTSANTDING -= points
                self.TDS += points - (points - tds_payout)  
                self.STD += points - (points - std_payout)  
                Payout( member=sponser,
                        from_member =member,
                        type = 'direct',
                        name=sponser.get_user_name,
                        points=points,
                        tds=tds, 
                        std_deduction=std_deduction,
                        payout=payout
                        ).save()
        except:
            sponser = MemberAccount.objects.get(member_id=member.sponser_id)
        
    def get_member(self, member_id):
        # code
        return MemberAccount.objects.get(member_id=member_id)

    def get_seller(self, seller_id):
        # code
        return MemberAccount.objects.get(member_id=seller_id)

    def get_product(self, product_id):
        # code
        return AddProduct.objects.get(id=product_id)

    def get_product(self, product_id):
        # code
        return AddProduct.objects.get(id=product_id)


    def get_order_details(self,seller):
        # code
        return OrderDetails.objects.filter(order_by = seller)

    def check_products_available_in_stock(self,orders,product_id):
        # code
        if orders.count() == 0:
            return False
        else:
            for i in orders:
                if (i.quantity_delivered+i.generated+i.transfer_in-i.quantity_sold-i.transfer_out>0) and i.product_id == product_id:
                    i.quantity_sold += 1
                    i.save()
                    self.PRODUCT = i.id
                    return True
            return False

    def get_level_points(self, product_id, level):
        # code
        return Level.objects.filter(product=product_id).get(level=level)

    def get_num_of_levels(self, product_id):
        # code
        return Level.objects.filter(product=product_id).count()

    def create(self, request, *args, **kwargs):
        # code
        # initializing serializer
        serializer = self.get_serializer(data=request.data) 

        if serializer.is_valid():

            # local variables
            member_id = request.data.get('member')
            seller_id = request.data.get('seller')
            product_id = request.data.get('product')

            # fetching data from data base 
            member = self.get_member(member_id)
            product = self.get_product(product_id)
            seller = self.get_seller(seller_id)
            orders = self.get_order_details(seller_id)
            total_levels = self.get_num_of_levels(product_id)
            if self.is_active_member(member) == False and( product.product_type == 'seller' or product.product_type == 'distributer'):
                return Response({"message":"User not Active Member"}, status=status.HTTP_412_PRECONDITION_FAILED)
            if self.is_active_member(member) == False and( product.product_type == 'bt_product'):
                return Response({"message":"User not Active Member"}, status=status.HTTP_412_PRECONDITION_FAILED)
            if self.is_active_seller(member) == True and( product.product_type == 'seller'):
                return Response({"message":"User is Active Seller"}, status=status.HTTP_412_PRECONDITION_FAILED)
            self.MAX_PAYOUT += product.max_payout 
            self.OUTSANTDING += product.max_payout 
            if product.is_package:
                pkg_product = self.get_product(product.add_package_product)
                if pkg_product.has_key:
                    SubProductsStock(member=member, product=pkg_product,quantity=product.quantity).save()
            if(product.product_type == 'distributer'):
                is_request_status_false = True
                for d in IntroducerRequest.objects.filter(distributer=member):
                    if d.status == True:
                        is_request_status_false = False # prevent from exiting because of request status false

                if is_request_status_false:
                    return Response({"message":"Distributer request not accepted by admin"}, status=status.HTTP_412_PRECONDITION_FAILED)
                querysetDistibuter = ActiveCityDistibuter.objects.get(distributer=member)
                querysetDistibuterarr = ActiveCityDistibuter.objects.filter(pin_code=querysetDistibuter.pin_code)
                for i in querysetDistibuterarr:
                    if i.is_active:
                        return Response({"message":"Already a distributer"}, status=status.HTTP_412_PRECONDITION_FAILED)
            if self.check_products_available_in_stock(orders,product_id):
                    if   product.product_type == 'bt_product':
                        self.allocate_binary_tree_points(member=member,product=product)
                    else:
                        self.generate_sponser_payout(member=member,points=product.points_to_buyer, tds=product.tds, std_deduction=product.std_deduction)
                        self.generate_seller_payout(member=member,product_id=product_id , levels=total_levels,tds=product.tds, std_deduction=product.std_deduction)
                        self.generate_sponser_bonus_payout(member=member,tds=product.tds, std_deduction=product.std_deduction, product=product)
                        self.check_product_type(product=product,member=member)
                        self.generate_distributers_payout(member=member,points=product.points_to_city_distributer,tds=product.tds, std_deduction=product.std_deduction)
                    AdminAccounts(  total_payout=self.MAX_PAYOUT,
                                    distributed_payout=self.DISTRIBUTED_PAYOUT, 
                                    balance_after_deduction=self.OUTSANTDING, 
                                    tds=self.TDS,
                                    std=self.STD,
                                    total_balance=self.OUTSANTDING+self.TDS+self.STD+(product.Price-self.MAX_PAYOUT ),
                                    dp=product.Price,
                                    bonus=self.BONUS,
                                    difference=product.Price-self.MAX_PAYOUT 
                                    ).save()
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"message":"No Products in Stock"}, status=status.HTTP_412_PRECONDITION_FAILED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MySalesViewset(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleListSerializer
    authentication_classes = []
    permission_classes = []
    filter_backends = [filters.SearchFilter,DjangoFilterBackend]
    filterset_fields = [ 'seller','member']
    search_fields = ['seller','member']

    
    @action(detail=False, methods=['get'])
    def purchase(self, request):
        try:
            member = request.query_params.get("member")
            product = AddProduct.objects.get(has_key=True)
            member = MemberAccount.objects.get(member_id=member)
            orders =Sale.objects.filter(member=member).filter(product=product)
            if int(orders.count())>0:
                if int(ActivationKeys.objects.filter(allocated_to=member).count())<int(orders.count()):
                    for i in range(int(orders.count())-int(ActivationKeys.objects.filter(allocated_to=member).count())):
                        ActivationKeys(allocated_to=member).save()
                query = ActivationKeys.objects.filter(allocated_to=member)
                qs_json = serializers.serialize('json', query)
                return Response({'acitivation_product_exists':True,'activation_keys':json.loads(qs_json)}, status=status.HTTP_200_OK)
            else:
                return Response({'acitivation_product_exists':False}, status=status.HTTP_200_OK)
        except:
            return Response({'message':'invalid member id'}, status=status.HTTP_404_NOT_FOUND)

      
class GetMembersViewset(viewsets.GenericViewSet,mixins.CreateModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin):
    queryset = MemberAccount.objects.all()
    serializer_class = MemberAccountSerializer
    authentication_classes = []
    permission_classes = []
    filter_backends = [filters.SearchFilter,DjangoFilterBackend]
    filterset_fields = ['member_id']
    search_fields = ['member_id']
    # def list(self, request):
    #     member_id = request.query_params.get('member')
    #     if member_id is not None:
    #         queryset = Sale.objects.filter(member=member_id)
    #     else:
    #         queryset = Sale.objects.all()

    #     serializer_class = SaleListSerializer(queryset, many=True)
    #     return Response(serializer_class.data,status=status.HTTP_400_BAD_REQUEST)
