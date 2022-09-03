from django.shortcuts import render
from rest_framework import generics
from products.ModelSerializers import ProductSerializer, ProductSerializerOwner
from products.mixins import ProductMixinSerializer
from products.models import Products
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import SellerOrNotSellerPerm, SellerOwnerOrNotSeller
import ipdb

class ProductView(ProductMixinSerializer,generics.ListCreateAPIView):
   
    authentication_classes = [TokenAuthentication]
    permission_classes = [SellerOrNotSellerPerm, IsAuthenticatedOrReadOnly]
   
    queryset = Products.objects.all()
    serializer_map = {
        'GET': ProductSerializer,
        'POST': ProductSerializerOwner,
    }

    def perform_create(self, serializer):
        return serializer.save(seller=self.request.user)

class ProductDetailView(ProductMixinSerializer, generics.RetrieveUpdateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [SellerOwnerOrNotSeller, IsAuthenticatedOrReadOnly]
    
    queryset = Products.objects.all()
    serializer_map = {
        'GET': ProductSerializer,
        'PATCH': ProductSerializerOwner,
    }