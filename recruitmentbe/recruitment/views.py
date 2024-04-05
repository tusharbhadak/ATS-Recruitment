from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Candidate
from .serializers import CandidateSerializer, CandidateViewSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import permissions
from django.http import Http404 

class IsUserRole(permissions.BasePermission):
    """
    Custom permission to allow only users with 'User' role to create candidates.
    """
    def has_permission(self, request, view):
        # Check if the user has the 'User' role
        return request.user.role == 'User'


class IsRecruiter(permissions.BasePermission):
    """
    Custom permission to allow only users with 'Recruiter' role to edit the 'status' field of the application.
    """
    def has_permission(self, request, view):
        return request.user.role == 'Recruiter'
    

class CreateCandidateAPIView(APIView):
    permission_classes = [IsUserRole]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request, format=None):
        serializer = CandidateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 1,
                'message': 'Candidate registered successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 0,
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    

class CandidateDetailAPIView(APIView):
    permission_classes = [IsRecruiter]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_object(self, pk):
        try:
            return Candidate.objects.get(pk=pk)
        except Candidate.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        candidate = self.get_object(pk)
        serializer = CandidateSerializer(candidate)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        candidate = self.get_object(pk)
        serializer = CandidateSerializer(candidate, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 1,
                'message': 'Candidate Status Updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 0,
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)