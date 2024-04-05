from django.urls import path
from .views import CreateCandidateAPIView

urlpatterns = [
    path('create/', CreateCandidateAPIView.as_view(), name='create_candidate'),
]
