from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer,UserLoginSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .models import User
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
class UserLoginView(APIView):
    def post(self, request):
        ser_data = UserLoginSerializer(data=request.data)
        if ser_data.is_valid():
            user=get_object_or_404(User,email=ser_data.validated_data['email'])
            if user.check_password(ser_data.validated_data['password']):
                if user.need_new_token():
                    token = Token.objects.create(user=user)
                else:
                    token=get_object_or_404(Token,user=user)
                return Response(data=token.key, status=status.HTTP_202_ACCEPTED)
            return Response({"message":"email and password doesn't match"},status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(ser_data.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
class UserLogoutView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        token=get_object_or_404(Token,user=request.user)
        token.delete()
        return Response(data={'message':'user logged out successfylly'},status=status.HTTP_202_ACCEPTED)

class UserActivationView(APIView):
    permission_classes=[IsAdminUser]
    def setup(self, request, *args, **kwargs):
        self.user=get_object_or_404(User,pk=kwargs['user_id'])
        return super().setup(request, *args, **kwargs)

    def get(self,request,user_id):
        if not self.user.is_active:
            self.user.is_active = True
            self.user.save()
            print('='*90)
            print('get is working')
            return Response({'message':'user activated'},status=status.HTTP_202_ACCEPTED)
        return Response({'message':'user is already activated.'},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,user_id):
        print('='*90)
        print('delete is working')
        if self.user.is_active:
            self.user.is_active = False
            self.user.save()
            return Response({'message':'user deactivated'},status=status.HTTP_202_ACCEPTED)
        return Response({'message':'user is already deactivated.'},status=status.HTTP_400_BAD_REQUEST)
