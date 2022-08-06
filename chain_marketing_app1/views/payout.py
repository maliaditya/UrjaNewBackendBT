from datetime import datetime
from .imports import *
# {
#     "member": "URJAD5938F",
#     "payment_amount": 100
# }
class PayoutViewset(viewsets.ModelViewSet):
    #variable declarations
    queryset = Payout.objects.all()
    serializer_class = PayoutSerializer
    authentication_classes = []
    permission_classes = []
    filter_backends = [filters.SearchFilter,DjangoFilterBackend]
    filterset_fields = [ 'member', 'created_at', 'id']
    search_fields = ['member', 'created_at', 'id']
    
    #********* Make Payment **************
    @action(detail=False, methods=['post'])
    def make_payment(self, request):

        #variable declarations
        total_payment_amount = int(request.data['payment_amount']) # Fetch payment amount form request body 
        description = request.data['description'] # Fetch payment amount form request body 
        member = MemberAccount.objects.get(member_id=request.data['member']) # Fetch member data from database
        all_payouts = Payout.objects.filter(member=member) # Fetch all payout of that member_id

        #********* Make Payment Logic **************
        for payout in all_payouts:
            if payout.declared and total_payment_amount>0:
                if payout.payout == payout.payment:
                    continue
                elif payout.payment == 0 and total_payment_amount >payout.payout:
                    payout.payment = payout.payout
                    payout.description = description
                    total_payment_amount -= payout.payout
                    payout.save()
                elif payout.payment < payout.payout and total_payment_amount!=0:
                    if total_payment_amount>payout.payout:
                        payout.payment += payout.payout - payout.payment
                        payout.description = description
                        total_payment_amount -=  payout.payout - payout.payment
                        payout.save()
                    elif total_payment_amount<payout.payout:
                        payout.payment += total_payment_amount
                        payout.description = description
                        total_payment_amount -=  total_payment_amount
                        payout.save()
                    elif total_payment_amount==payout.payout:
                        payout.payment = payout.payout
                        payout.description = description
                        total_payment_amount -= payout.payout
                        payout.save()
                        print("inelse total_payment_amount",total_payment_amount,payout.payout)
        return Response({"msg":"success"}, status=status.HTTP_201_CREATED)


    #********* declare Payout **************
    @action(detail=False, methods=['patch'])
    def dclr_pending_pyt(self, request):
        date = request.query_params.get('date')
        if date is None:
            return Response(status=status.Http_400_BAD_REQUEST)
        else:
            payouts = Payout.objects.filter(created_at__gte = date)
            serializer_class = PayoutSerializer(payouts,many=True)
            for payout in payouts:
                if payout.declared == False and str(payout.created_at).split(' ')[0] == date:
                    payout.declared = True
                    payout.save()
            return Response(serializer_class.data, status=status.HTTP_200_OK)

    @action(detail=False,methods=['get'])
    def admin_payout(self, request):
        queryset = Payout.objects.all()
        self.pagination_class = PageNumberPagination
        p = self.paginate_queryset(queryset)
        serializer_class = PayoutSerializer(p, many=True)
        return self.get_paginated_response(serializer_class.data)

    
    @action(detail=False,methods=['get'])
    def pending_payouts(self, request):
        pending_payouts=[]
        payouts = Payout.objects.all()
        for i in payouts:
            if i.declared==False :
                member = str(i.member)
                from_member = str(i.from_member)
                payment = {
                                "id": i.id,
                                "member":member,
                                "points": i.points,
                                "tds": i.tds,
                                "std_deduction": i.std_deduction,
                                "payout": i.payout,
                                "from_member": from_member,
                                "type": i.type,
                                "payment":i.payment,
                                "description":i.description,
                                "declared": i.declared,
                                "get_created_at": i.get_created_at,
                                "get_updated_at":i.get_updated_at,
                                "created_at": i.created_at
                            }
                pending_payouts.append(payment)
        return Response(pending_payouts,status=status.HTTP_200_OK)