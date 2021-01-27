from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='role.role')
    class Meta:
        model = User
        fields = ('id','fname','lname','email','mobile_no', 'device_id', 'is_active', 'role')

class UserRequestSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='role.role')
    class Meta:
        model = User
        fields = ('id','fname','lname','email','mobile_no','datetime_of_request', 'datetime_of_activation', 'is_approved', 'is_active', 'role')

class UserRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoles
        fields = '__all__'