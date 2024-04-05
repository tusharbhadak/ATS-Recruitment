from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Candidate
from .serializers import CandidateSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import permissions

class IsUserRole(permissions.BasePermission):
    """
    Custom permission to allow only users with 'User' role to create candidates.
    """
    def has_permission(self, request, view):
        # Check if the user has the 'User' role
        return request.user.role == 'User'

# Create your views here.
class CreateCandidateAPIView(APIView):
    permission_classes = [IsUserRole]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request, format=None):
        serializer = CandidateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 1,
                'message': 'User registered successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 0,
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)