from django.contrib.auth import models
from .models import Employee, Notifications, User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        extra_kwargs = {'password': {'write_only': True}}
        fields = ['id', 'email', 'name', 'isAdmin','isRegistered']

    def get_id(self, obj):
        return obj.id

    def get_isRegistered(self, obj):
        return obj.is_registered

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_name(self, obj):
        name = obj.name
        if name == '':
            name = obj.email

        return name


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        extra_kwargs = {'password': {'write_only': True}}
        fields = '__all__'

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)




class EmployeeSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="employee:getEmployees")
    class Meta:
        model = Employee
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="employee:getEmployees")
    class Meta:
        model = Notifications
        fields = '__all__'