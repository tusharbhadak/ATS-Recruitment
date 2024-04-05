from rest_framework import serializers
from .models import Candidate
from account.serializers import UserSerializer

class CandidateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Candidate
        fields = ['name', 'age', 'gender', 'years_of_exp', 'email', 'phone_number', 'current_salary', 'expected_salary', 'status', 'created_at'] 
