from django.urls import path
from .views import CreateCandidateAPIView, CandidateDetailAPIView, CandidateSearchAPIView, NameSearchAPIView

urlpatterns = [
    path('create/', CreateCandidateAPIView.as_view(), name='create_candidate'),
    path('candidatesstatus/<int:pk>/', CandidateDetailAPIView.as_view(), name='candidate-detail'),
    path('candidates/search/', CandidateSearchAPIView.as_view(), name='candidate-search'),
    path('candidates/name-search/', NameSearchAPIView.as_view(), name='name-search'),
]
