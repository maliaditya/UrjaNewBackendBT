from .imports import *  # NOQA




class StockTransferViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = []
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) 
        if serializer.is_valid():
            member = MemberAccount.objects.get(member_id=request.data.get('ordered_from'))
            member_orders = Order.objects.filter(orded_by=member)
            for order in member_orders:
                productdetail = OrderDetails.objects.filter(order=order.order_no).get(product_id=request.data.get('order_detail')[0].get('product_id'))
                if productdetail.quantity_delivered+productdetail.generated+productdetail.transfer_in-productdetail.quantity_sold-productdetail.transfer_out>0:
                    productdetail.transfer_out +=1
                    productdetail.save()
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'message':'product not in stock'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'Invalid details please fill correct details'}, status=status.HTTP_400_BAD_REQUEST)