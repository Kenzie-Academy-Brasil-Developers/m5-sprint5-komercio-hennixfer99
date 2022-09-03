from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS



class OwnerPerm(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id
    
class AdminPerm(permissions.BasePermission):
    def has_permission(self, request, view):        
        return request.user.is_superuser