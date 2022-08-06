from rest_framework import serializers
from .models import ActiveUser,SOS,ActivationKeys

class ActiveUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveUser
        fields = '__all__'


class SOSSerializer(serializers.ModelSerializer):
    class Meta:
        model = SOS
        fields = '__all__'
        
class ActivationKeysSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivationKeys
        fields = '__all__'
        
