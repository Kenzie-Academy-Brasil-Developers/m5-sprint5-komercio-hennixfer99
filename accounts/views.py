from rest_framework.views import APIView, Response, status
from accounts.ModelSerializers import LoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from .ModelSerializers import AccountSerializer
from .models import Accounts
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from accounts.permissions import OwnerPerm

class LoginView(APIView):
      def post(self, request):
            serializer = LoginSerializer(data = request.data)
            serializer.is_valid(raise_exception = True)

            user = authenticate(
                  username = serializer.validated_data["username"],
                  password = serializer.validated_data["password"],
            )
 
            if user:
                  token, _ = Token.objects.get_or_create(user=user)

                  return Response({'token': token.key})

            return Response({"detail": 'invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)


class AccountView(generics.ListCreateAPIView):
      queryset = Accounts.objects.all()
      serializer_class = AccountSerializer

class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
      queryset = Accounts.objects.all()
      serializer_class = AccountSerializer
      def get_queryset(self):
            num = self.kwargs['num']
            return self.queryset.order_by('-date_joined')[0:num]

class AccountUpdate(generics.RetrieveUpdateAPIView):
      authentication_classes = [TokenAuthentication]
      permission_classes = [OwnerPerm, IsAuthenticated]

      queryset = Accounts.objects.all()
      serializer_class = AccountSerializer

class UpdateStatus(generics.RetrieveUpdateAPIView):
      authentication_classes = [TokenAuthentication]
      permission_classes = [IsAdminUser]

      queryset = Accounts.objects.all()
      serializer_class = AccountSerializer
      def perform_update(self, serializer):
            
            for key, value in self.request.data.itens():
                  if key == 'is_active':
                        return serializer.save(is_active = value)