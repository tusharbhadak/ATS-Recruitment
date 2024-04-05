from django.urls import path
from .views import CreateCandidateAPIView, CandidateDetailAPIView

urlpatterns = [
    path('create/', CreateCandidateAPIView.as_view(), name='create_candidate'),
    path('candidatesstatus/<int:pk>/', CandidateDetailAPIView.as_view(), name='candidate-detail'),
]
