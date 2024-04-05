from rest_framework import serializers
from .models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'mobile_number', 'password', 'confirm_password', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'required': False}  # Allow 'role' to be optional during user creation
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        role = validated_data.pop('role', 'User')

        # Create the user object with the extracted data
        user = User.objects.create_user(**validated_data, role=role)
        return user

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'role', 'email', 'mobile_number', 'name', 'is_active']
