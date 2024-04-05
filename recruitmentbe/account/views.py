from django.shortcuts import render
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import filters
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from django.db.models import Q
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated


# Register API
class SignupView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        email = request.data.get('email')
        mobile_number = request.data.get('mobile_number')

        # Check if email or mobile number already exists in User table
        if User.objects.filter(Q(email=email) | Q(mobile_number=mobile_number)).exists():
            return Response({
                'status': 0,
                'error': 'Email or mobile number already exists.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Create serializer instance with request data
        serializer = UserRegisterSerializer(data=request.data)

        # Validate serializer data
        if serializer.is_valid():
            # Save validated data to create user
            user = serializer.save()

            return Response({
                'status': 1,
                'message': 'User registered successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 0,
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

   
# Login API
class LoginView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Check if the user exists with the provided email or username
        user = User.objects.filter(Q(email=username) | Q(mobile_number=username)).first()
        
        if user is None:
            return Response({
                'status': 0,
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)

        # Check if the provided password is correct
        if not user.check_password(password):
            return Response({
                'status': 0,
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        return Response({
            'status': 1,
            'message': "User Logged In Successfully",
            'data': {
                'token': str(refresh.access_token),
                'user': UserSerializer(user, context={'request': request}).data
            }
        }, status=status.HTTP_200_OK)


# Logged in User Profile
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve the current user
        user = request.user
        # Serialize the user data
        serializer = UserSerializer(user)
        # Return the serialized user data in the response
        return Response({
            'status': 1,
            'message': 'User Profile fetched successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)