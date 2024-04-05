from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Candidate
from .serializers import CandidateSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import permissions
from django.http import Http404 
from django.db.models import Q
from itertools import combinations
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 5   
    page_size_query_param = 'page_size'
    max_page_size = 100

class IsRecruiter(permissions.BasePermission):
    """
    Custom permission to allow only users with 'Recruiter' role to edit the 'status' field of the application.
    """
    def has_permission(self, request, view):
        return request.user.role == 'Recruiter'
    

class CreateCandidateAPIView(APIView):
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
    

class CandidateSearchAPIView(APIView):
    pagination_class = CustomPagination

    def get(self, request, format=None):
        # Get query parameters
        expected_salary_min = request.query_params.get('expected_salary_min')
        expected_salary_max = request.query_params.get('expected_salary_max')
        age_min = request.query_params.get('age_min')
        age_max = request.query_params.get('age_max')
        years_of_exp_min = request.query_params.get('years_of_exp_min')
        phone_number = request.query_params.get('phone_number')
        email = request.query_params.get('email')
        name = request.query_params.get('name')

        # Filter candidates based on query parameters
        candidates = Candidate.objects.all()

        if expected_salary_min:
            candidates = candidates.filter(expected_salary__gte=expected_salary_min)
        if expected_salary_max:
            candidates = candidates.filter(expected_salary__lte=expected_salary_max)
        if age_min:
            candidates = candidates.filter(age__gte=age_min)
        if age_max:
            candidates = candidates.filter(age__lte=age_max)
        if years_of_exp_min:
            candidates = candidates.filter(years_of_exp__gte=years_of_exp_min)
        if phone_number:
            candidates = candidates.filter(phone_number=phone_number)
        if email:
            candidates = candidates.filter(email=email)
        if name:
            candidates = candidates.filter(name=name)  # Assuming name is the username of the user


        # Order the queryset by creation date in descending order
        candidates = candidates.order_by('-created_at')

        # Paginate the queryset
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(candidates, request)

        # Serialize and return the paginated results
        serializer = CandidateSerializer(page, many=True)

        # Check if no records found
        if not serializer.data:
            return Response({
                'status': 0,
                'message': 'No records found'
            }, status=status.HTTP_404_NOT_FOUND)

        return paginator.get_paginated_response({
            'status': 1,
            'message': 'Candidates data fetched successfully',
            'data': serializer.data
        })
  

class NameSearchAPIView(APIView):
    pagination_class = CustomPagination

    def get(self, request, format=None):
        query = request.query_params.get('query', '')

        # Split the query into individual words
        query_words = query.lower().split()

        # Filter candidates based on name containing any of the query words
        candidates = Candidate.objects.all()

        for word in query_words:
            candidates = candidates.filter(name__icontains=word)

        # Sort the candidates by relevance (number of overlapping words)
        candidates = sorted(candidates, key=lambda candidate: self.relevance_sort(candidate, query_words), reverse=True)

        # Paginate the results
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(candidates, request)

        # Serialize and return the paginated results
        serializer = CandidateSerializer(page, many=True)

        # Check if no records found
        if not serializer.data:
            return Response({
                'status': 0,
                'message': 'No records found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        return paginator.get_paginated_response({
            'status': 1,
            'message': 'Candidates data fetched successfully',
            'data': serializer.data
        })

    def relevance_sort(self, candidate, query_words):
        # Count the number of overlapping words in the candidate's name
        candidate_name_words = candidate.name.lower().split()
        overlapping_words = [word for word in query_words if word in candidate_name_words]

        # Return the count of overlapping words
        return len(overlapping_words)