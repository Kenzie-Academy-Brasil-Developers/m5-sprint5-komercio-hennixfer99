from rest_framework import serializers
from accounts.models import Accounts

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only = True)
    password = serializers.CharField(write_only = True)

class AccountSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = Accounts
        fields = ['id','username','first_name','password','last_name','is_seller','date_joined','is_superuser','is_active']
        read_only_fields = ['date_joined','is_superuser','is_active']
        extra_kwargs = {'password': {'write_only': True}}
    

    def create(self, validated_data):

        return Accounts.objects.create_user(**validated_data)
       
class AccountsDetails(serializers.ModelSerializer):
    class Meta():
        model = Accounts
        fields = ['id','username','first_name','last_name','is_seller','date_joined','is_active','is_superuser']


    def create(self, validated_data):

        return Accounts.objects.create_user(**validated_data)

class UpdateStatus(serializers.ModelSerializer):
    class Meta():
        model = Accounts
        fields = ['is_active']
