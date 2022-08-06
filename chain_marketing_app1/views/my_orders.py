from imports import *


class MyOrders(dict):
    def __init__(self, order,product,product_id,quantity,price, delivered, undelivered,stock,sold, total):
        super().__init__()
        self.__dict__ = self
        self.order = order
        self.product = product
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
        self.delivered = delivered
        self.undelivered = undelivered
        self.stock = stock
        self.sold = sold
        self.total = total


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
