from django.urls import path
from .views import (
    AssignmentCreateView,
    AssignmentListView,
    AssignmentSubmissionView,
    AssignmentMarkView,
)

urlpatterns = [
    path('create/', AssignmentCreateView.as_view(), name='assignment-create'),
    path('list/', AssignmentListView.as_view(), name='assignment-list'),
    path('submit/', AssignmentSubmissionView.as_view(), name='assignment-submit'),
    path('mark/', AssignmentMarkView.as_view(), name='assignment-mark'),
]
