from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
class UserRegisterView(APIView):
    def post(self, request):
        ser_data = UserRegisterSerializer(data=request.data)
        if ser_data.is_valid():
            user=ser_data.create(ser_data.validated_data)
            token = Token.objects.create(user=user)
            return Response(data=token.key, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

class UserActivationView(APIView):
    permission_classes=[IsAdminUser]
    def setup(self, request, *args, **kwargs):
        self.user=get_object_or_404(User,pk=kwargs['user_id'])
        return super().setup(request, *args, **kwargs)

    def get(self,request,user_id):
        if self.user.is_active==False:
            self.user.is_active = True
            self.user.save()
            return Response({'message':'user activated'},status=status.HTTP_202_ACCEPTED)
        return Response({'user is already activated.'},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,user_id):
        if self.user.is_active:
            self.user.is_active = False
            self.user.save()
            return Response({'message':'user deactivated'},status=status.HTTP_202_ACCEPTED)
        return Response({'user is already deactivated.'},status=status.HTTP_400_BAD_REQUEST)
