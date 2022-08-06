
from chain_marketing_app.models import Level
from chain_marketing_app.models import AddProduct, MemberAccount,ActiveMember,OrderDetails
from chain_marketing_app.models import  Sale,Payout
from chain_marketing_app.serializers import (SaleSerializer, StockSerializer)
from rest_framework import fields, mixins, serializers, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core import serializers
import json

class MyStock(dict):
    def __init__(self, order,product,product_id,product_type,quantity,price, delivered, undelivered,stock,sold, total, transfer_in,transfer_out, generated):
        super().__init__()
        self.__dict__ = self
        self.order = order
        self.product = product
        self.product_id = product_id
        self.product_type=product_type
        self.quantity = quantity
        self.price = price
        self.delivered = delivered
        self.undelivered = undelivered
        self.stock = stock
        self.sold = sold
        self.transfer_in = transfer_in
        self.transfer_out = transfer_out
        self.generated = generated
        self.total = total


class StockViewset(viewsets.ModelViewSet):
    queryset = OrderDetails.objects.all()
    serializer_class = StockSerializer
    authentication_classes = []
    permission_classes = []

    my_stock_list = []

    
    def get_index(self,list,id):
        for i in list:
            if i.product == id:
                return list.index(i)

    def if_exists(self,list,id):
        for i in list:
            if i.product == id:
                return True
        return False


    def create_stock(self,q,member):
       
        for i in q:
            print("i=", i)
            if len(self.my_stock_list) ==0:
                product_type = AddProduct.objects.get(id=i.product_id).product_type
                
                self.my_stock_list.append(MyStock(  order=str(i.order),
                                                    product= i.product,
                                                    product_id=i.product_id,
                                                    product_type=product_type,
                                                    quantity= i.quantity,
                                                    price= i.price,
                                                    delivered= i.quantity_delivered, 
                                                    undelivered=i.quantity- i.quantity_delivered,
                                                    stock= i.quantity_delivered+i.generated+i.transfer_in-i.quantity_sold-i.transfer_out,
                                                    sold = Sale.objects.filter(seller=member).filter(product=i.product_id).count(), 
                                                    total=i.quantity * i.price,
                                                    transfer_in=i.transfer_in,
                                                    transfer_out=i.transfer_out,
                                                    generated= i.generated,
                                                    ))

            elif self.if_exists(self.my_stock_list, i.product):
                index =self.get_index(self.my_stock_list, i.product)
                self.my_stock_list[index].quantity += i.quantity
                self.my_stock_list[index].delivered += i.quantity_delivered
                self.my_stock_list[index].generated += i.generated
                self.my_stock_list[index].transfer_in += i.transfer_in
                self.my_stock_list[index].transfer_out += i.transfer_out
                self.my_stock_list[index].undelivered +=( i.quantity- i.quantity_delivered)
                self.my_stock_list[index].stock += i.quantity_delivered+i.generated+i.transfer_in-i.quantity_sold-i.transfer_out
                self.my_stock_list[index].total +=(i.quantity * i.price)

            elif not self.if_exists(self.my_stock_list, i.product):
                product_type = AddProduct.objects.get(id=i.product_id).product_type
                self.my_stock_list.append(MyStock(  order=str(i.order),
                                                    product= i.product,
                                                    product_id=i.product_id,
                                                    product_type=product_type,
                                                    quantity= i.quantity,
                                                    price= i.price,
                                                    delivered= i.quantity_delivered, 
                                                    undelivered=i.quantity- i.quantity_delivered,
                                                    stock=   i.quantity_delivered+i.generated+i.transfer_in-i.quantity_sold-i.transfer_out,
                                                    sold = Sale.objects.filter(seller=member).filter(product=i.product_id).count(), 
                                                    total=i.quantity * i.price,
                                                    transfer_in=i.transfer_in,
                                                    transfer_out=i.transfer_out,
                                                    generated= i.generated,))
        
        return (self.my_stock_list)

    def get_all_orders(self, user):
        return OrderDetails.objects.filter(order_by = user)

    def list(self,request):
        self.my_stock_list.clear()
        user = request.query_params.get("member")
        objectQuerySet =  self.get_all_orders(user)
        jsonstr = json.dumps(self.create_stock(objectQuerySet,user), indent=2)
        # data = serializers.serialize('json', list(objectQuerySet))
        # dataa = json.loads(data)
        return Response(json.loads(jsonstr),status=status.HTTP_200_OK)