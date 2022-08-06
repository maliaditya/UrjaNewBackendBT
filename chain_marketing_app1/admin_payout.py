
from  .imports import  *

class AdminPayoutViewset(viewsets.ModelViewSet):
    queryset =Payout.objects.all()
    serializer_class = PayoutSerializer
    authentication_classes = []
    permission_classes = []


    def list(self, request):
        pending_payments=[]
        payouts = Payout.objects.all()
        for i in payouts:
            if i.payment==0 and i.declared==True :
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
                pending_payments.append(payment)
        return Response(pending_payments,status=status.HTTP_200_OK)
