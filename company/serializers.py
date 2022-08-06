from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [ 'id', 'company_name','user','get_full_address','company_details',
                    'leading_seller','verified_seller','get_short_address',
                    'address_line1','address_line2','city','pin_code','state'
                    ]
        