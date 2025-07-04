from django.urls import path
from .views import ResumeMatcherView, UserMatchHistoryView, DeleteMatchView

urlpatterns = [
    path('match/', ResumeMatcherView.as_view(), name='resume_match'),
    path('match/history/', UserMatchHistoryView.as_view(), name='user_match_history'),
    path('match/delete/<int:pk>/', DeleteMatchView.as_view(), name='delete_match'),
]   