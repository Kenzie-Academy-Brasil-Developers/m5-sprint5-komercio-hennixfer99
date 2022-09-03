from rest_framework import serializers
from products.models import Products
from accounts.ModelSerializers import AccountsDetails


class ProductSerializer(serializers.ModelSerializer):

    
    class Meta():
        model = Products
        fields = ['id','description','price','quantity','is_active','seller_id']

class ProductSerializerOwner(serializers.ModelSerializer):

    seller = AccountsDetails(read_only = True)
    class Meta():
        model = Products
        fields = ['id', 'seller','description','price','quantity','is_active']
        read_only_fields = ['seller', 'seller_id', 'is_active']