from rest_framework import serializers
from .models import User




class UserRegisterSerializer(serializers.ModelSerializer):
	password2 = serializers.CharField(write_only=True, required=True)
	
	class Meta:
		model = User
		fields = ('email','full_name', 'is_author','password', 'password2')
		extra_kwargs = {
			'password': {'write_only':True},
			'password2': {'write_only':True},
		}

	def create(self, validated_data):
		user = User(email=validated_data['email'],full_name=validated_data['full_name'])
		user.is_author=validated_data['is_author']
		user.set_password(validated_data['password'])

		user.save()
		return user

	def validate(self, data):
		if data['password'] != data['password2']:
			raise serializers.ValidationError("passwords must match")
		return data


class UserLoginSerializer(serializers.Serializer):	
	email=serializers.EmailField(required=True)
	password=serializers.CharField(required=True,write_only=True)