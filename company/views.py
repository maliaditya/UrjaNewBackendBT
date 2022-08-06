from django.shortcuts import render
from rest_framework.response import Response

# Create your views here.
from .models import Company
from .serializers import CompanySerializer
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes


class CompanyViewset(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    authentication_classes = [JWTAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]


@api_view(['GET'])
@permission_classes([])
def company(request):
    if request.method == 'GET':
            user = request.query_params.get('user')
            company = Company.objects.filter(user=user)
            body = [] 
            for company in company:
                    comp = {
                                "id":company.id,
                                'company_name':company.company_name,
                                'address_line1':company.address_line1,
                                'address_line2':company.address_line2,
                                'city':company.city,
                                'state':company.state,
                                'pin_code':company.pin_code,
                                'company_details':company.company_details,
                                'leading_seller':company.leading_seller,
                                'verified_seller':company.verified_seller
                            }
                    body.append(comp)

        

            if len(body) != 0:
                return Response(body)   
            else:
                return Response({
                "message":"company does not exists",
                }) 